from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    first_name: str
    last_name: str


class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class UserCreate(UserBase):
    pass