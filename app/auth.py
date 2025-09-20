import hmac
import hashlib
import os
from typing import Union
import time

SECRET = os.getenv("BRIDGE_SECRET", "replace-with-strong-secret").encode()
EXPECTED_TOKEN = os.getenv("BRIDGE_TOKEN", "demo-token")  # nur der reine Token ohne "Bearer "
ALLOWED_SKEW = 300  # seconds

def _extract_bearer(authorization: Union[str, None]) -> Union[str, None]:
    if not authorization:
        return None
    scheme, _, token = authorization.strip().partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token.strip()

def verify_headers(authorization: str, x_timestamp: str, x_nonce: str,
                   x_signature: str, method: str, path: str, body: bytes):
    token = _extract_bearer(authorization)
    if not token:
        return False, "missing_token"
    if token != EXPECTED_TOKEN:
        return False, "invalid_token"

    # Zeitfenster prüfen
    try:
        timestamp = int(x_timestamp)
        if abs(time.time() - timestamp) > ALLOWED_SKEW:
            return False, "timestamp_out_of_window"
    except ValueError:
        return False, "invalid_timestamp"

    # Signatur prüfen
    if x_signature:
        body_hash = hashlib.sha256(body or b"").hexdigest()
        base = f"{method}\n{path}\n{body_hash}\n{x_timestamp}\n{x_nonce}".encode()
        calc = hmac.new(SECRET, base, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calc, x_signature):
            return False, "bad_signature"

    return True, ""