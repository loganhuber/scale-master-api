from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    email: EmailStr = Field(max_length=120)
    pw_hash: str = Field(max_length=200)


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)



class ScoreBase(BaseModel):
    score: int = Field(max_digits=2)
    date: datetime

class ScoreCreate(ScoreBase):
    pass


class ScoreResponse(ScoreBase):
    id: int
    user_id: int
    user: UserResponse

