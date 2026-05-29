from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    email: EmailStr = Field(max_length=120)

class UserCreate(UserBase):
    pw_hash: str = Field(max_length=200)
    

class UserResponse(UserBase):
    scores: list[ScoreBase] = []
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=5, max_length=50)
    email: str | None = Field(default=None, max_length=120)
    pw_hash: str | None = Field(default=None, max_length=200)




class ScoreBase(BaseModel):
    score: int 
    date: datetime
    scale: str
    scale_key: str
    model_config = ConfigDict(from_attributes=True)


# class ScoreSimple(ScoreBase):
#     model_config = ConfigDict(from_attributes=True)

class ScoreCreate(ScoreBase):
    user_id: int

class ScoreResponse(ScoreBase):
    id: int
    user_id: int
    user: UserBase

