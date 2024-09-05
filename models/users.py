from typing import Annotated
from pydantic import BaseModel, EmailStr, Field
from models.general import BaseMixin
from models.models import Users
from sqlalchemy.orm import Session


VOWELS = ["a", "e", "i", "o", "u"]


def get_consonants_of_username_doubled(username: str):
    consonants = []
    for letter in username:
        if letter not in VOWELS:
            consonants.append(letter)


class UserRequest(BaseModel):
    username: Annotated[
        str,
        Field(description="The username of the user", title="Username", min_length=4),
    ]
    password: Annotated[
        str,
        Field(description="The password of the user", title="Password", min_length=8),
    ]
    email: Annotated[
        EmailStr, Field(description="The email of the user", title="Email")
    ]

    def create(self, db: Session):
        user = Users(**self.model_dump())

        db.add(user)
        db.commit()


class User(BaseMixin, UserRequest):
    pass
