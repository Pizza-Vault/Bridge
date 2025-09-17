from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import Session
from ..models import InventoryItem

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.post("/items")
async def create_item(body: dict):
    sku = body["sku"]
    async with Session() as s:
        exists = (await s.execute(select(InventoryItem).where(InventoryItem.sku==sku))).scalar_one_or_none()
        if exists:
            raise HTTPException(409, "sku_exists")
        item = InventoryItem(**body)
        s.add(item)
        await s.commit()
        await s.refresh(item)
        return {"id": item.id, "sku": item.sku, "name": item.name, "qty": item.qty, "warn_level": item.warn_level}

@router.get("/items")
async def list_items():
    async with Session() as s:
        res = await s.execute(select(InventoryItem))
        rows = res.scalars().all()
        return [{"id": i.id, "sku": i.sku, "name": i.name, "qty": i.qty, "warn_level": i.warn_level} for i in rows]
