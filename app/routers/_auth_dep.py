from fastapi import Header, HTTPException, Request
from auth import verify_headers

DEV_BYPASS_AUTH = True  # <<< NUR LOKAL/DEV!

def auth_guard_factory(method: str, path_pattern: str):
    async def _guard(
        request: Request,
        authorization: str = Header(None, alias="Authorization"),
        x_timestamp: str = Header(None, alias="X-Timestamp"),
        x_nonce: str = Header(None, alias="X-Nonce"),
        x_signature: str | None = Header(None, alias="X-Signature"),
    ):
        if DEV_BYPASS_AUTH:
            return True

        body = await request.body()
        ok, err = verify_headers(
            authorization=authorization or "",
            x_timestamp=x_timestamp or "",
            x_nonce=x_nonce or "",
            x_signature=x_signature or "",
            method=method,
            path=path_pattern,
            body=body or b"",
        )
        if not ok:
            raise HTTPException(status_code=401, detail=err)
        return True
    return _guard
