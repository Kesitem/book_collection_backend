from sqlmodel import SQLModel, Field


class BookBase(SQLModel):
    title: str


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BookPublic(BookBase):
    id: int


class BookCreate(BookBase):
    pass


class BookUpdate(SQLModel):
    title: str | None = None

