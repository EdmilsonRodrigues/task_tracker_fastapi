from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from pytest import Session

from models.users import User, UserRequest, UserResponse
from session import get_db


router = APIRouter(tags=["Auth"])
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def authenticate_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    user = User.validate_token(token=token, db=db)  # type: ignore
    return user


current_user = Annotated[User, Depends(authenticate_user)]


@router.get("/api/users", tags=["Admin"])
async def get_users(db: db_dependency) -> list[UserResponse]:
    users: list[User] = User.get_by_query(db=db)  # type: ignore
    return [UserResponse(**user.model_dump()) for user in users]


@router.post("/api/auth/sign-in", status_code=201)
async def create_user(user: UserRequest, db: db_dependency) -> None:
    user.create(db=db)  # type: ignore


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/api/auth/login")
async def log_in(login: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    access_token = User.create_token(login.username, login.password)

    return Token(access_token=access_token, token_type="Bearer")


@router.get("/api/users/me")
async def get_user(
    current_user: current_user
) -> UserResponse:
    return UserResponse(**current_user.model_dump())


@router.put("/api/user/me", status_code=204)
async def update_user(
    db: db_dependency, user: UserRequest, current_user: current_user
) -> None:
    model_user = User(**user.model_dump(), id=current_user.id)

    model_user.update(db)  # type: ignore


@router.delete("/api/users/me", status_code=204)
async def delete_user(db: db_dependency, current_user: current_user) -> None:
    user = User.get_by_id(db=db, id=current_user.id)  # type: ignore

    user.delete(db=db)  # type:ignore
