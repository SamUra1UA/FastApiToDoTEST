from celery import shared_task
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete
import asyncio
from datetime import datetime

from app.models import Task, TaskStatus

DATABASE_URL = "sqlite+aiosqlite:///./todo.db"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@shared_task
def delete_expired_tasks():
    asyncio.run(_delete_expired())

async def _delete_expired():
    async with AsyncSessionLocal() as session:
        now = datetime.utcnow()
        # Видаляємо завдання зі статусом pending, у яких deadline в минулому
        stmt = delete(Task).where(
            Task.status == TaskStatus.pending,
            Task.deadline < now
        )
        result = await session.execute(stmt)
        await session.commit()
        return f"Deleted {result.rowcount} expired tasks"
