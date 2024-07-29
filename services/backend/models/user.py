from typing import Optional

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    id: int = Field(default=None, nullable=False, primary_key=True)
    username: str = Field(max_length=50)
    full_name: str = Field(max_length=100)
    email: str = Field(max_length=75)
    hashed_password: str = Field(max_length=150)
    disabled: Optional[bool] = Field(default=False)


class UserFull(UserBase, table=True):
    __tablename__ = "users"


class UserRegistrationForm(SQLModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None
