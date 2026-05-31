from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "http://localhost:3000",  # Default Create React App port
    "http://localhost:5173",  # Default Vite port
    "https://yourproductiondomain.com", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows specific client applications
    allow_credentials=True,           # Allows cookies and auth headers
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allows all request headers
)

app.include_router(user.router, prefix='/api/users', tags=['users'])
app.include_router(score.router, prefix='/api/scores', tags=['scores'])

