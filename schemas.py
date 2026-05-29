from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    email: EmailStr = Field(max_length=120)

class UserCreate(UserBase):
    pw_hash: str = Field(max_length=200)
    

class UserResponse(UserBase):
    scores: list[ScoreSimple] = []
    id: int
    model_config = ConfigDict(from_attributes=True)



class ScoreBase(BaseModel):
    score: int 
    date: datetime

class ScoreSimple(ScoreBase):
    score: int
    date: datetime
    model_config = ConfigDict(from_attributes=True)

class ScoreCreate(ScoreBase):
    pass

class ScoreResponse(ScoreBase):
    id: int
    user_id: int
    user: UserBase

