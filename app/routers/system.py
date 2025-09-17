from fastapi import APIRouter, Depends, HTTPException
from ._auth_dep import auth_guard_factory
from store import STORE, Mode, now_utc

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/mode", dependencies=[Depends(auth_guard_factory("GET", "/api/system/mode"))])
def get_mode():
    return {"mode": int(STORE["mode"]), "mode_version": STORE["mode_version"], "at": now_utc()}

@router.post("/mode", dependencies=[Depends(auth_guard_factory("POST", "/api/system/mode"))])
def set_mode(body: dict):
    try:
        mode = int(body.get("mode"))
    except Exception:
        raise HTTPException(status_code=422, detail="invalid_mode")
    if mode not in (1, 2, 3, 4):
        raise HTTPException(status_code=422, detail="invalid_mode")
    STORE["mode"] = Mode(mode)
    STORE["mode_version"] += 1
    return {"mode": int(STORE["mode"]), "mode_version": STORE["mode_version"], "at": now_utc()}

@router.post("/presence", dependencies=[Depends(auth_guard_factory("POST", "/api/system/presence"))])
def presence(body: dict):
    automaton_id = body.get("automaton_id")
    status = bool(body.get("status", False))
    if not automaton_id:
        raise HTTPException(status_code=422, detail="missing_automaton_id")
    STORE["presence"][automaton_id] = status
    if status:
        STORE["mode"] = Mode.DIRECT_ONLY
        STORE["mode_version"] += 1
    return {"automaton_id": automaton_id, "status": status, "mode": int(STORE["mode"])}
