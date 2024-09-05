from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from models.general import BaseMixin
from sqlalchemy import Enum
from sqlalchemy.orm import Session

from models.models import Tasks


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


class Task(BaseMixin, TaskRequest):
    pass
