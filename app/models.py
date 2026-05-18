from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import EmailStr

class RegularUserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserResponse(SQLModel):
    id: Optional[int]
    username: str
    email: str

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    done: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="todos")

    def get_cat_list(self):
        return ''

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str
    role: str = Field(default="regular_user")

    todos: List[Todo] = Relationship(back_populates="user")
