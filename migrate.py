import asyncio
from db import ENGINE
from models import Base

async def main():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(main())
