from sqlmodel import SQLModel, Field


class AuthorBase(SQLModel):
    firstname: str
    lastname: str


class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class AuthorPublic(AuthorBase):
    id: int


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(SQLModel):
    firstname: str | None = None
    lastname: str | None = None
