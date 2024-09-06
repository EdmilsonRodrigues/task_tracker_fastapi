from datetime import datetime, timedelta
from hashlib import md5
from typing import Annotated
from fastapi import HTTPException
import jwt
from pydantic import BaseModel, EmailStr, Field
from models.general import BaseMixin
from models.models import Users
from sqlalchemy.orm import Session


VOWELS = ["a", "e", "i", "o", "u"]
SECRET_KEY = "8.57i29uca741w77,.dl8sz154ngcjmsnfb6r1x8r648.t8po6h7ffi6"


def get_consonants_of_username_doubled(username: str):
    consonants = []
    for letter in username:
        if letter not in VOWELS:
            consonants.append(letter)
    return "".join(consonants)


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
        self.hash_password()
        user = Users(**self.model_dump())

        db.add(user)
        db.commit()

    @staticmethod
    def hash(username: str, password: str):
        salt = get_consonants_of_username_doubled(username)

        password += salt

        return md5(string=password.encode()).hexdigest()

    def hash_password(self):
        self.password = self.hash(self.username, self.password)


class User(BaseMixin, UserRequest):
    @staticmethod
    def create_token(username: str, password: str) -> str:
        expiration = datetime.now() + timedelta(minutes=30)
        payload = {
            "sub": username,
            "password": password,
            "secret": SECRET_KEY,
            "exp": expiration,
        }

        return jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")

    @classmethod
    def validate_token(cls, db: Session, token) -> "User":
        try:
            payload = jwt.decode(token)
            user = (
                db.query(Users)
                .filter(
                    Users.username == payload["username"],
                    Users.password == cls.hash(username=payload["username"], password=payload["password"]),
                )
                .first()
            )
            if user:
                return user
            raise
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Token Invalid",
                headers={"www-authenticate": "bearer"},
            )


class UserResponse(BaseModel):
    id: Annotated[int, Field(description="The id of the task", gt=0)]
    username: Annotated[
        str,
        Field(description="The username of the user", title="Username", min_length=4),
    ]
    email: Annotated[
        EmailStr, Field(description="The email of the user", title="Email")
    ]
