from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(...)
    email: EmailStr
    password: str = Field(..., min_length=6)
    token: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    token: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    message: str
    delete_user_id: int