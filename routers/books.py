from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from internal.security import get_current_active_user
from models.book import BookPublic, Book, BookCreate, BookUpdate, BookPublicWithAuthors
from models.user import User

router = APIRouter(
    prefix="/books",
    tags=["books"])


@router.get("/", response_model=list[BookPublic])
async def get_all_books(*, session: Session = Depends(get_session),
                        current_user: Annotated[User, Depends(get_current_active_user)]):
    books = session.exec(select(Book)).all()
    return books


@router.post("/", response_model=BookPublic)
def create_book(*, session: Session = Depends(get_session),
                current_user: Annotated[User, Depends(get_current_active_user)],
                book: BookCreate):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.get("/{book_id}", response_model=BookPublicWithAuthors)
def read_book(*, session: Session = Depends(get_session),
              current_user: Annotated[User, Depends(get_current_active_user)],
              book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=BookPublic)
def update_book(
    *, session: Session = Depends(get_session),
        current_user: Annotated[User, Depends(get_current_active_user)], book_id: int, book: BookUpdate):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.delete("/{book_id}")
def delete_book(*, session: Session = Depends(get_session),
                current_user: Annotated[User, Depends(get_current_active_user)], book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}
