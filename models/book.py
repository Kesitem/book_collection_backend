from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from models.author import AuthorPublic
from models.bookauthorlink import BookAuthorLink

if TYPE_CHECKING:
    from .author import Author


class BookBase(SQLModel):
    title: str


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    authors: list["Author"] = Relationship(back_populates="books", link_model=BookAuthorLink)


class BookPublic(BookBase):
    id: int


class BookPublicWithAuthors(BookPublic):
    authors: list[AuthorPublic] = []


class BookCreate(BookBase):
    pass


class BookUpdate(SQLModel):
    title: str | None = None
