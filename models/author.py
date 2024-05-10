from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from models.bookauthorlink import BookAuthorLink

if TYPE_CHECKING:
    from .book import Book, BookPublic


class AuthorBase(SQLModel):
    firstname: str
    lastname: str


class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(back_populates="authors", link_model=BookAuthorLink)


class AuthorPublic(AuthorBase):
    id: int


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(SQLModel):
    firstname: str | None = None
    lastname: str | None = None
