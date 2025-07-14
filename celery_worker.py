from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks"]
)

celery_app.conf.task_routes = {
    "app.tasks.delete_expired_tasks": {"queue": "tasks_queue"},
}

celery_app.conf.beat_schedule = {
    "delete-expired-tasks-every-day": {
        "task": "app.tasks.delete_expired_tasks",
        "schedule": 86400.0,  # кожні 24 години
    }
}

celery_app.conf.timezone = "UTC"



if __name__ == "__main__":
    celery_app.start()
