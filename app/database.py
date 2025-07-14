from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# SQLite URI (async)
DATABASE_URL = "sqlite+aiosqlite:///./todo.db"

# Створення async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async сесія
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

# Declarative Base
class Base(DeclarativeBase):
    pass
