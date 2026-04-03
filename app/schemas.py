from pydantic import EmailStr, BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum
from .models import RecordType,UserRole,FinancialCategory

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    type: RecordType
    category: FinancialCategory
    description: Optional[str] = None

class RecordCreate(RecordBase):
    pass  

class Record(RecordBase):
    id: int
    date: datetime
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: Optional[UserRole] = UserRole.VIEWER

class User(UserBase):
    id: int
    role: UserRole
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
