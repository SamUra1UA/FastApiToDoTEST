from fastapi import FastAPI
from app.routers import todo, auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(todo.router, prefix="/tasks")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
