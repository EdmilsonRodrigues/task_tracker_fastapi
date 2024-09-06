from typing import Annotated
from fastapi import Depends, HTTPException, Path
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from models.tasks import Task, TaskRequest
from session import get_db
from routers.auth import current_user


router = APIRouter(tags=["Tasks"])

db_dependency = Annotated[Session, Depends(get_db)]
task_id_dependency = Annotated[int, Path(description="The id of the task", gt=0)]


@router.get("/api/tasks")
async def get_tasks(db: db_dependency, current_user: current_user) -> list[Task]:
    tasks: list[Task] = Task.get_by_query(db=db)
    return [task for task in tasks if task.user_id == current_user.id]


@router.post("/api/tasks", status_code=201)
async def create_task(task: TaskRequest, db: db_dependency, current_user: current_user) -> None:
    task = Task(**task.model_dump(), user_id=current_user.id)
    task.create(db=db)


@router.get("/api/tasks/{task_id}")
async def get_task(
    db: db_dependency, current_user: current_user,
    task_id: task_id_dependency,
) -> Task:
    task = Task.get_by_id(db=db, id=task_id)
    if task.user_id != current_user.id:
        raise HTTPException(404, "Task not found")
    return task


@router.put("/api/taks/{task_id}", status_code=204)
async def update_task(
    db: db_dependency, current_user: current_user, task_id: task_id_dependency, task: TaskRequest
) -> None:
    model_task = Task(**task.model_dump(), id=task_id, user_id=current_user.id)

    model_task.update(db)


@router.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(db: db_dependency, current_user: current_user, task_id: task_id_dependency) -> None:
    task = Task.get_by_id(db=db, id=task_id)
    if task.user_id != current_user.id:
        raise HTTPException(404, "Task not found")

    task.delete(db=db)
