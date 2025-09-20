from fastapi import Depends, HTTPException, Header, Request
from typing import Union
from ..auth import verify_headers  # Import aus app/auth.py
from sqlalchemy.orm import Session
from ..database import get_db  # Fix: .. für app/database.py

def auth_guard_factory(method: str, path: str):
    def auth_guard(
        request: Request,  # Fix: Request als erster, auto-injiziert
        authorization: Union[str, None] = Header(None),
        x_timestamp: Union[str, None] = Header(None, alias="X-Timestamp"),
        x_nonce: Union[str, None] = Header(None, alias="X-Nonce"),
        x_signature: Union[str, None] = Header(None, alias="X-Signature"),
        db: Session = Depends(get_db)
    ):
        body = request.body()
        is_valid, detail = verify_headers(
            authorization or "",
            x_timestamp or "",
            x_nonce or "",
            x_signature or "",
            method, path, body
        )
        if not is_valid:
            raise HTTPException(status_code=401, detail=detail)
        return True
    return auth_guard