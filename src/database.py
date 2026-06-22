from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:////data/database.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session_maker() as session:
        yield session
