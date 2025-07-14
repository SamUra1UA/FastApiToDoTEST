from fastapi import FastAPI
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from app.admin_views import UserAdmin, TaskAdmin
from app.database import engine
from app.models import User, Task
from app.routers import auth, todo
from fastapi import Form
from fastapi.responses import HTMLResponse, Response
from starlette.requests import Request
app = FastAPI()

admin = Admin(
    app,
    engine,
    authentication_backend=None  # Вимикаємо аутентифікацію
)

admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)

app.include_router(auth.router, prefix="/auth")
app.include_router(todo.router, prefix="/tasks")

@app.get("/")
async def root():
    return {"message": "Hello from ToDo App"}
