from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from internal.security import get_current_active_user
from models.author import AuthorPublic, Author, AuthorCreate, AuthorUpdate
from models.book import BookPublic
from models.user import User


class AuthorPublicWithBooks(AuthorPublic):
    books: list[BookPublic] = []


router = APIRouter(
    prefix="/authors",
    tags=["authors"])


@router.get("/", response_model=list[AuthorPublic])
async def get_all_author(*, session: Session = Depends(get_session),
                         current_user: Annotated[User, Depends(get_current_active_user)]):
    authors = session.exec(select(Author)).all()
    return authors


@router.post("/", response_model=AuthorPublic)
def create_author(*, session: Session = Depends(get_session),
                  current_user: Annotated[User, Depends(get_current_active_user)],
                  author: AuthorCreate):
    db_author = Author.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.get("/{author_id}", response_model=AuthorPublicWithBooks)
def read_author(*, session: Session = Depends(get_session),
                current_user: Annotated[User, Depends(get_current_active_user)],
                author_id: int):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.patch("/{author_id}", response_model=AuthorPublic)
def update_author(
        *, session: Session = Depends(get_session),
        current_user: Annotated[User, Depends(get_current_active_user)],
        author_id: int, author: AuthorUpdate):
    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    author_data = author.model_dump(exclude_unset=True)
    for key, value in author_data.items():
        setattr(db_author, key, value)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.delete("/{author_id}")
def delete_author(*, session: Session = Depends(get_session),
                  current_user: Annotated[User, Depends(get_current_active_user)],
                  author_id: int):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"ok": True}
