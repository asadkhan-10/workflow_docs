# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class InputType(str, Enum):
    text = "text"
    json = "json"

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

# Workflow schemas
class WorkflowCreate(BaseModel):
    title: str
    raw_input: str
    input_type: InputType

class WorkflowOut(BaseModel):
    id: int
    title: str
    input_type: str
    documentation: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None