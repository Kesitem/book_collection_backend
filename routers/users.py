from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from internal.security import get_current_active_user, get_password_hash
from models.user import UserPublic, User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"])


@router.get("/me", response_model=UserPublic)
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.post("/", response_model=UserPublic)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    hashed_password = get_password_hash(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
