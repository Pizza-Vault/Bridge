from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

ENGINE = create_async_engine("sqlite+aiosqlite:///./bridge.db", future=True)
Session = async_sessionmaker(ENGINE, expire_on_commit=False)
