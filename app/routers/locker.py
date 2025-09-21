from fastapi import APIRouter, Depends, HTTPException
from ._auth_dep import auth_guard_factory
from ..store import STORE  # Fix: Relativer Import!

router = APIRouter(prefix="/api/locker", tags=["locker"])

@router.post("/open", dependencies=[Depends(auth_guard_factory("POST", "/api/locker/open"))])
def locker_open(body: dict):
    code = body.get("pickup_code")
    if not code:
        raise HTTPException(status_code=422, detail="missing_pickup_code")
    for o in STORE["orders"].values():
        if o["pickup_code"] == code:
            o["locker_opened"] = True
            return {"status": "opened"}
    raise HTTPException(status_code=404, detail="invalid_code")

@router.post("/label", dependencies=[Depends(auth_guard_factory("POST", "/api/locker/label"))])
def locker_label(body: dict):
    code = body.get("pickup_code")
    text = body.get("label_text", "")
    if not code:
        raise HTTPException(status_code=422, detail="missing_pickup_code")
    STORE["labels"][code] = text
    return {"pickup_code": code, "label": text}

@router.post("/pickup/confirm", dependencies=[Depends(auth_guard_factory("POST", "/api/locker/pickup/confirm"))])
def pickup_confirm(body: dict):
    code = body.get("pickup_code")
    if not code:
        raise HTTPException(status_code=422, detail="missing_pickup_code")
    for o in STORE["orders"].values():
        if o["pickup_code"] == code:
            o["status"] = "completed"
            return {"status": "completed"}
    raise HTTPException(status_code=404, detail="invalid_code")