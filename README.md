# FastAPI Task Manager

A simple asynchronous task manager API built with FastAPI, SQLAlchemy, Celery, and Redis. Supports user registration, authentication, task CRUD operations, and automatic cleanup of expired tasks.

## Features

- User registration and authentication (JWT)
- Create, read, update, complete, and delete tasks
- Task filtering and pagination
- Automatic deletion of expired tasks (Celery + Redis)
- Async database operations (SQLAlchemy)
- Pydantic schemas for validation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy (async)
- Celery
- Redis
- SQLite (default, can be changed)
- Pydantic

## Getting Started

### Prerequisites

- Python 3.10+
- Redis server running locally (`localhost:6379`)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run database migrations (if any).

### Running the App

1. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```

2. Start the Celery worker:
    ```sh
    celery -A celery_worker.celery_app worker --beat --loglevel=info
    ```

### API Endpoints

#### Auth

- `POST /auth/register` — Register a new user
- `POST /auth/login` — Login and get JWT token

#### Tasks

- `GET /tasks/` — List tasks (with filters, pagination)
- `POST /tasks/` — Create a new task
- `GET /tasks/{task_id}` — Get task by ID
- `PATCH /tasks/{task_id}` — Update task
- `PATCH /tasks/{task_id}/complete` — Mark task as completed
- `DELETE /tasks/{task_id}` — Delete task

## Environment Variables

- `DATABASE_URL` — Database connection string (default: SQLite)
- `REDIS_URL` — Redis connection string (default: `redis://localhost:6379/0`)

