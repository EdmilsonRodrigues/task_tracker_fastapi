from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from models.tasks import DBTask, Task, TaskRequest
from session import get_db


router = APIRouter()


@router.get("/api/tasks")
async def get_tasks(db: Annotated[Session, Depends(get_db)]) -> Task:
    return await Task.get_by_query(db=db)


@router.post("/api/tasks")
async def create_task(task: TaskRequest):
    pass
