from fastapi import APIRouter, Depends, HTTPException
from ._auth_dep import auth_guard_factory
from store import STORE

router = APIRouter(prefix="/api/payment", tags=["payment"])

@router.post("/charge", dependencies=[Depends(auth_guard_factory("POST", "/api/payment/charge"))])
def payment_charge(body: dict):
    order_id = body.get("order_id")
    status = body.get("status", "paid")
    o = STORE["orders"].get(order_id)
    if not o:
        raise HTTPException(status_code=404, detail="order_not_found")
    if status not in ("paid", "not_paid"):
        raise HTTPException(status_code=422, detail="invalid_status")
    o["payment"] = status
    return {"order_id": order_id, "payment": status}
