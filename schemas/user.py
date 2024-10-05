from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    pass


# Properties to receive on item creation
class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


# Properties to return to client
class User(UserBase):
    id: int

    class Config:
        orm_mode = True
