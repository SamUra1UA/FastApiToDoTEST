from sqladmin import ModelView
from app.models import User, Task


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.role, User.created_at]
    column_searchable_list = [User.email]
    column_sortable_list = [User.id, User.email, User.created_at]
    form_excluded_columns = [User.tasks]  # не показувати список задач в формі

    name = "User"
    name_plural = "Users"


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.title, Task.status, Task.owner_id, Task.created_at, Task.deadline]
    column_searchable_list = [Task.title]
    column_sortable_list = [Task.id, Task.created_at, Task.deadline]

    form_columns = [Task.title, Task.description, Task.status, Task.deadline, Task.owner_id]

    name = "Task"
    name_plural = "Tasks"
