from fastapi import APIRouter, Depends, HTTPException
from ._auth_dep import auth_guard_factory
from starlette.requests import Request

router = APIRouter()

@router.get("/mode")
def get_mode(
    request: Request,
    auth = Depends(auth_guard_factory("GET", "/api/system/mode"))
):
    # Logik für Mode abrufen (aus DB oder State)
    mode = 1  # Platzhalter – erweitere mit DB
    return {"mode": mode, "mode_version": 1, "at": "2025-09-20T12:00:00Z"}

@router.post("/mode")
def set_mode(
    body: dict,
    request: Request,
    auth = Depends(auth_guard_factory("POST", "/api/system/mode"))
):
    mode = body.get("mode")
    if mode is None:
        raise HTTPException(status_code=400, detail="Missing mode")
    # Logik für Mode setzen (DB-Update)
    return {"mode": mode, "message": "Set"}