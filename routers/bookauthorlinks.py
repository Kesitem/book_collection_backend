from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from internal.security import get_current_active_user
from models.bookauthorlink import BookAuthorLink
from models.user import User

router = APIRouter(
    prefix="/bookauthorlinks",
    tags=["bookauthorlinks"])


@router.post("/", response_model=BookAuthorLink)
def create_db_book_author_link(*, session: Session = Depends(get_session),
                               current_user: Annotated[User, Depends(get_current_active_user)],
                               book_author_link: BookAuthorLink):
    statement = select(BookAuthorLink).where(BookAuthorLink.book_id == book_author_link.book_id,
                                             BookAuthorLink.author_id == book_author_link.author_id)
    db_book_author_link = session.exec(statement).first()
    if not db_book_author_link:
        session.add(book_author_link)
        session.commit()
        session.refresh(book_author_link)
    else:
        raise HTTPException(status_code=400, detail="Link between book and author already exists")
    return book_author_link


@router.delete("/")
def delete_book_author_link(*, session: Session = Depends(get_session),
                            current_user: Annotated[User, Depends(get_current_active_user)],
                            book_author_link: BookAuthorLink):
    statement = select(BookAuthorLink).where(BookAuthorLink.book_id == book_author_link.book_id,
                                             BookAuthorLink.author_id == book_author_link.author_id)
    db_book_author_link = session.exec(statement).first()
    if not db_book_author_link:
        raise HTTPException(status_code=404, detail="Link between book and author not found")
    session.delete(db_book_author_link)
    session.commit()
    return {"ok": True}
