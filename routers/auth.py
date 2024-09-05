from typing import Annotated
from fastapi import APIRouter, Depends, Path
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from pytest import Session

from models.users import User, UserRequest
from session import get_db


router = APIRouter(tags=["Auth"])
db_dependency = Annotated[Session, Depends(get_db)]
user_id_dependency = Annotated[int, Path(description="The id of the user", gt=0)]


@router.get("/api/users", tags=["Admin"])
async def get_users(db: db_dependency) -> list[User]:
    return User.get_by_query(db=db)  # type: ignore


@router.post("/api/auth/sign-in", status_code=201)
async def create_user(user: UserRequest, db: db_dependency) -> None:
    user.create(db=db)  # type: ignore


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/api/auth/login")
async def log_in(login: OAuth2PasswordRequestForm):
    access_token = User.create_token(login.username, login.password)

    return Token(
        access_token=access_token,
        token_type="Bearer"
    )


@router.get("/api/users/{user_id}")
async def get_user(
    db: db_dependency,
    user_id: user_id_dependency,
) -> User:
    return User.get_by_id(db=db, id=user_id)  # type: ignore


@router.put("/api/user/{user_id}", status_code=204)
async def update_user(
    db: db_dependency, user_id: user_id_dependency, user: UserRequest
) -> None:
    model_user = User(**user.model_dump(), id=user_id)

    model_user.update(db)  # type: ignore


@router.delete("/api/users/{user_id}", status_code=204)
async def delete_user(db: db_dependency, user_id: user_id_dependency) -> None:
    user = User.get_by_id(db=db, id=user_id)  # type: ignore

    user.delete(db=db)  # type:ignore
