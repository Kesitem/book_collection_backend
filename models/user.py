from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str
    full_name: str
    disabled: bool


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
