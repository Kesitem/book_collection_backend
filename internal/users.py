from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.user import User


def get_user(*, session: Session = Depends(get_session), username: str):
    """
    Get user from username.
    :param session:
    :param username:
    :return:
    """
    statement = select(User).where(User.username == username)
    try:
        user = session.exec(statement).one()
    except:
        raise HTTPException(status_code=404, detail="Hero not found")

    if not user:
        raise HTTPException(status_code=404, detail="Hero not found")
    return user
