import hashlib
import hmac
import os

def verify_headers(auth: str, timestamp: str, nonce: str, signature: str, method: str, path: str, body: bytes) -> tuple[bool, str]:
    if not auth.startswith("Bearer "):
        return False, "invalid_auth"
    token = auth.split(" ")[1]
    if token != os.getenv("BRIDGE_TOKEN"):
        return False, "invalid_token"
    body_hash = hashlib.sha256(body).hexdigest()
    base_string = f"{method}\n{path}\n{body_hash}\n{timestamp}\n{nonce}"
    secret = os.getenv("BRIDGE_SECRET").encode()
    expected = hmac.new(secret, base_string.encode(), hashlib.sha256).hexdigest()
    if signature != expected:
        return False, "invalid_signature"
    # To-Do: Add Zeitfenster (±300s) und Nonce-Replay (z. B. DB-Check)
    return True, ""