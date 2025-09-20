from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ._auth_dep import auth_guard_factory
from db import Session
from ..models import Order
from store import STORE
from utils import new_id

router = APIRouter(prefix="/api/order", tags=["order"])

async def _db() -> AsyncSession:
    async with Session() as s:
        yield s

@router.post(
    "/create",
    dependencies=[Depends(auth_guard_factory("POST", "/api/order/create"))],
)
async def create_order(
    body: dict,
    idem_key: Union[str, None] = Header(None, alias="Idempotency-Key"),  # Fix: Union für Python 3.9
    db: AsyncSession = Depends(_db),
):
    product_id = body.get("product_id")
    timeslot = body.get("timeslot")
    if not product_id or not timeslot:
        raise HTTPException(status_code=422, detail="missing_fields")

    # Idempotenz
    if idem_key and idem_key in STORE["idem"]:
        return STORE["idem"][idem_key]

    order_id = new_id("ord_")
    pickup_code = new_id("pc_")

    record = {
        "id": order_id,
        "product_id": product_id,
        "timeslot": timeslot,
        "pickup_code": pickup_code,
        "status": "pending",
        "payment": "not_paid",
    }

    # In-Memory (MVP)
    STORE["orders"][order_id] = record

    # Persistenz (SQLite via SQLAlchemy Async)
    await db.merge(
        Order(
            id=order_id,
            product_id=product_id,
            timeslot=timeslot,
            pickup_code=pickup_code,
            status="pending",
            payment="not_paid",
        )
    )
    await db.commit()

    resp = {"order_id": order_id, "pickup_code": pickup_code, "status": "pending"}
    if idem_key:
        STORE["idem"][idem_key] = resp
    return resp

@router.get(
    "/status",
    dependencies=[Depends(auth_guard_factory("GET", "/api/order/status"))],
)
def order_status(order_id: str):
    o = STORE["orders"].get(order_id)
    if not o:
        raise HTTPException(status_code=404, detail="order_not_found")
    return {"order_id": order_id, "status": o["status"], "payment": o["payment"]}

@router.post(
    "/complete",
    dependencies=[Depends(auth_guard_factory("POST", "/api/order/complete"))],
)
def order_complete(body: dict):
    order_id = body.get("order_id")
    o = STORE["orders"].get(order_id)
    if not o:
        raise HTTPException(status_code=404, detail="order_not_found")
    o["status"] = "completed"
    return {"order_id": order_id, "status": "completed"}