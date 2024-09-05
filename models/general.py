from typing import Annotated
from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from session import Base


class BaseMixin(BaseModel):
    id: Annotated[int, Field(description="The id of the task", gt=0)]

    @classmethod
    def get_db_name(cls):
        return cls.__name__.lower() + "s"

    @classmethod
    def get_db_class(cls) -> Base:  # type: ignore
        return globals().get(cls.get_db_name())

    @classmethod
    def get_by_id(cls, db: Session, id: int):
        database = cls.get_db_class()
        result = db.query(database).filter(database.id == id).first()
        if result:
            return cls(**result.dict())
        raise HTTPException(status_code=404, detail="Task not found")

    @classmethod
    def get_by_query(cls, db: Session, **kwargs):
        database = cls.get_db_class()
        list_of_queries = [
            getattr(database, argument) == kwargs.get(argument) for argument in kwargs
        ]
        tasks = db.query(database).filter(*list_of_queries).all()
        validated_tasks = []
        for task in tasks:
            validated_tasks.append(cls(**task.dict()))
        return validated_tasks

    def update(self, db: Session):
        database = self.get_db_class()
        task = database(**self.model_dump())

        db.add(task)
        db.commit()

    def delete(self, db: Session):
        database = self.get_db_class()
        db.query(database).filter(database.id == self.id).delete()

        db.commit()
