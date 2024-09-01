from typing import Annotated
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field
from session import Base
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import Session


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(String)

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
        }


class Status(str, Enum):
    work_in_progress = "wip"
    todo = "todo"
    done = "done"


class TaskRequest(BaseModel):
    title: Annotated[str, Field(description="The title of the taks")]
    description: Annotated[str, Field(description="The description of the taks")]
    priority: Annotated[int, Field(description="The priority of the task", gt=0, le=5)]
    status: Annotated[
        str,
        Field(
            description="The status of the taks: [todo, wip or done].",
            examples=["todo", "wip", "done"],
        ),
    ]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def create(self, db: Session):
        task = Tasks(**self.model_dump())

        db.add(task)
        db.commit()


class Task(TaskRequest):
    id: Annotated[int, Field(description="The id of the task", gt=0)]

    @classmethod
    def get_by_id(cls, db: Session, id: int) -> "Task":
        result = db.query(Tasks).filter(Tasks.id == id).first()
        if result:
            return cls(**result.dict())
        raise HTTPException(status_code=404, detail="Task not found")

    @classmethod
    def get_by_query(cls, db: Session, **kwargs) -> list["Task"]:
        tasks = db.query(Tasks).all()
        validated_tasks = []
        for task in tasks:
            validated_tasks.append(cls(**task.dict()))
        return validated_tasks

    def update(self, db: Session):
        task = Tasks(**self.model_dump())

        db.add(task)
        db.commit()

    def delete(self, db: Session):
        db.query(Tasks).filter(Tasks.id == self.id).delete()

        db.commit()
