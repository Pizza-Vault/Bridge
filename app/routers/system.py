from fastapi import APIRouter, Depends, HTTPException
from ._auth_dep import auth_guard_factory
from starlette.requests import Request

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/mode", dependencies=[Depends(auth_guard_factory("GET", "/api/system/mode"))])
async def get_mode():  # Async machen
    mode = 1  # Platzhalter
    return {"mode": mode, "mode_version": 1, "at": "2025-09-20T12:00:00Z"}

@router.post("/mode", dependencies=[Depends(auth_guard_factory("POST", "/api/system/mode"))])
async def set_mode(body: dict):  # Async machen
    mode = body.get("mode")
    if mode is None:
        raise HTTPException(status_code=400, detail="Missing mode")
    return {"mode": mode, "message": "Set"}