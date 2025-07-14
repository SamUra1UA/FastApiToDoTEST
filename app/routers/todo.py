from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models import User
from app import schemas, cruds, database, models
from app.schemas.schemas import TaskCreate, TaskResponse, TaskStatus, TaskUpdate
from app.models import RoleEnum
from app.dependencies import get_current_user, require_role
router = APIRouter(tags=["Tasks"])


async def get_db() -> AsyncSession:
    async with database.AsyncSessionLocal() as session:
        yield session

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.user, RoleEnum.admin, RoleEnum.manager))
):
    return await cruds.create_task(db, task, owner_id=current_user.id)


@router.get("/", response_model=List[TaskResponse])
async def read_tasks(
    status: Optional[TaskStatus] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await cruds.get_tasks(db, owner_id=current_user.id, status=status, limit=limit, offset=offset)


@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await cruds.get_task(db, task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Завдання не знайдено")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.user, RoleEnum.admin, RoleEnum.manager)),
):
    updated_task = await cruds.update_task(db, task_id, task_data, owner_id=current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Завдання не знайдено")
    return updated_task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.user, RoleEnum.admin, RoleEnum.manager)),
):
    completed = await cruds.mark_task_completed(db, task_id, owner_id=current_user.id)
    if not completed:
        raise HTTPException(status_code=404, detail="Завдання не знайдено")
    return completed


@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin, RoleEnum.manager)),  # user не може видаляти
):
    success = await cruds.delete_task(db, task_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Завдання не знайдено")
    return {"message": "Завдання успішно видалено"}