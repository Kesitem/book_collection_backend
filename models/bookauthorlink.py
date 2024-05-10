from sqlmodel import SQLModel, Field


class BookAuthorLink(SQLModel, table=True):
    book_id: int | None = Field(default=None, foreign_key="book.id", primary_key=True)
    author_id: int | None = Field(default=None, foreign_key="author.id", primary_key=True)