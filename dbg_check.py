import asyncio
from db import ENGINE
async def main():
    async with ENGINE.begin() as conn:
        r = await conn.exec_driver_sql("SELECT sql FROM sqlite_master WHERE type='table' AND name='orders'")
        print(r.fetchone())
async def run(): 
    import sys
    try:
        import asyncio
        asyncio.run(main())
    except Exception as e:
        print("ERR:", e, file=sys.stderr)
run()
