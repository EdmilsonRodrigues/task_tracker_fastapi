from typing import Annotated
from pydantic import BaseModel, Field
from session import Base
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import Session


class DBTask(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(String)


class Status(Enum):
    work_in_progress = "wip"
    todo = "todo"
    done = "done"


class TaskRequest(BaseModel):
    title: Annotated[str, Field(description="The title of the taks")]
    description: Annotated[str, Field(description="The description of the taks")]
    priority: Annotated[int, Field(description="The priority of the task", gt=0, le=5)]
    status: Annotated[Status, Field(description="The title of the taks")]

    

    def create(self):
        pass


class Task(TaskRequest):
    id: Annotated[int, Field(description="The id of the task", gt=0)]

    @classmethod
    def get_by_id(cls):
        pass

    @classmethod
    def get_by_query(cls, db: Session, **kwargs):
        result = db.query(DBTask).all()
        return result
