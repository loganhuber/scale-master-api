from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=50)

class UserCreate(UserBase):
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8)
    
class UserResponse(UserBase):
    scores: list[ScoreBase] = []
    id: int
    # model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=5, max_length=50)
    email: str | None = Field(default=None, max_length=120)
    password: str | None = Field(default=None, max_length=200)

class Token(BaseModel):
    access_token: str
    token_type: str

class ScoreBase(BaseModel):
    score: int 
    scale: str
    scale_key: str
    bpm: int
    model_config = ConfigDict(from_attributes=True)

class ScoreCreate(ScoreBase):
    pass
    

class ScoreResponse(ScoreBase):
    id: int
    user_id: int
    user: UserBase
    date: datetime
