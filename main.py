from fastapi import FastAPI, HTTPException, status, Depends
import uvicorn
from pydantic import BaseModel
from schemas import UserCreate, UserResponse

from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from routers import user, score

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(user.router, prefix='/api/users', tags=['users'])
app.include_router(score.router, prefix='/api/scores', tags=['scores'])

