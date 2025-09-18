from fastapi import FastAPI
from .routers import system, orders, locker, payment, production
from db import ENGINE
from .models import Base

app = FastAPI(title="Bridge API", version="0.1.0")

app.include_router(system.router)
app.include_router(orders.router)
app.include_router(locker.router)
app.include_router(payment.router)
app.include_router(production.router)

@app.get("/health")
def health():
    return {"ok": True}

@app.on_event("startup")
async def _init_db():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
