from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, cruds, database
from app.cruds import auth as auth_crud
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.utils import hash_password
from datetime import timedelta
from app.auth import create_access_token

router = APIRouter(tags=["Auth"])

async def get_db() -> AsyncSession:
    async with database.AsyncSessionLocal() as session:
        yield session

@router.post("/register", response_model=UserResponse)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await cruds.auth.get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email вже використовується")
    user = await cruds.auth.create_user(db, user_create.email, user_create.password)
    return user

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await cruds.auth.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильний email або пароль")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
