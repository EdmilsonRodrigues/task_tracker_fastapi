from typing import Annotated
from fastapi import Depends, Path
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from models.tasks import Task, TaskRequest
from session import get_db


router = APIRouter(tags=["Tasks"])

db_dependency = Annotated[Session, Depends(get_db)]
task_id_dependency = Annotated[int, Path(description="The id of the task", gt=0)]


@router.get("/api/tasks")
async def get_tasks(db: db_dependency) -> list[Task]:
    return Task.get_by_query(db=db)


@router.post("/api/tasks", status_code=201)
async def create_task(task: TaskRequest, db: db_dependency) -> None:
    task.create(db=db)


@router.get("/api/tasks/{task_id}")
async def get_task(
    db: db_dependency,
    task_id: task_id_dependency,
) -> Task:
    return Task.get_by_id(db=db, id=task_id)


@router.put("/api/taks/{task_id}", response_model=204)
async def update_task(
    db: db_dependency, task_id: task_id_dependency, task: TaskRequest
) -> None:
    model_task = Task(**task.model_dump(), id=task_id)

    model_task.update(db)


@router.delete("/api/tasks/{task_id}")
async def delete_task(db: db_dependency, task_id: task_id_dependency, response_model=204) -> None:
    task = Task.get_by_id(db=db, id=task_id)

    task.delete(db=db)
