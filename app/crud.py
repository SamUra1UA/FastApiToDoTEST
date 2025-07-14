from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app import models, schemas
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskStatus

# Створення завдання з owner_id
async def create_task(db: AsyncSession, task_data: TaskCreate, owner_id: int) -> models.Task:
    new_task = models.Task(**task_data.dict(), owner_id=owner_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

# Отримати список завдань користувача з фільтрацією та пагінацією
async def get_tasks(
    db: AsyncSession,
    owner_id: int,
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[models.Task]:
    stmt = select(models.Task).where(models.Task.owner_id == owner_id).offset(offset).limit(limit)

    if status == "completed":
        stmt = stmt.where(models.Task.status == TaskStatus.completed)
    elif status == "pending":
        stmt = stmt.where(models.Task.status == TaskStatus.pending)

    result = await db.execute(stmt)
    return result.scalars().all()

# Отримати завдання по ID та owner_id (щоб завдання було користувача)
async def get_task(db: AsyncSession, task_id: int, owner_id: int) -> Optional[models.Task]:
    result = await db.execute(
        select(models.Task).where(models.Task.id == task_id, models.Task.owner_id == owner_id)
    )
    return result.scalar_one_or_none()

# Оновити завдання, тільки якщо воно належить owner_id
async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskUpdate,
    owner_id: int
) -> Optional[models.Task]:
    db_task = await get_task(db, task_id, owner_id)
    if not db_task:
        return None

    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(db_task, field, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task

# Позначити як виконане (тільки своє завдання)
async def mark_task_completed(db: AsyncSession, task_id: int, owner_id: int) -> Optional[models.Task]:
    db_task = await get_task(db, task_id, owner_id)
    if not db_task:
        return None

    db_task.status = TaskStatus.completed
    await db.commit()
    await db.refresh(db_task)
    return db_task

# Видалити завдання (тільки якщо належить користувачу)
async def delete_task(db: AsyncSession, task_id: int, owner_id: int) -> bool:
    db_task = await get_task(db, task_id, owner_id)
    if not db_task:
        return False

    await db.delete(db_task)
    await db.commit()
    return True
