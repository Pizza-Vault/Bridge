from fastapi import APIRouter, Depends, HTTPException
from ._auth_dep import auth_guard_factory
from store import STORE

router = APIRouter(prefix="/api/production", tags=["production"])

@router.get("/time", dependencies=[Depends(auth_guard_factory("GET", "/api/production/time"))])
def production_time(order_id: str):
    o = STORE["orders"].get(order_id)
    if not o:
        raise HTTPException(status_code=404, detail="order_not_found")
    return {"order_id": order_id, "estimate_sec": 180}
