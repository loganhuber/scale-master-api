from fastapi import FastAPI, HTTPException, status, Depends
import uvicorn
from pydantic import BaseModel
from schemas import UserCreate, UserResponse

from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import UserCreate, UserResponse, ScoreCreate, ScoreResponse

Base.metadata.create_all(bind=engine)


app = FastAPI()

# @app.get('/api/users', response_model=list[UserResponse])
# def get_users():
#     return users


#>>>>>>>>ROUTES<<<<<<<
#>>>>>>>>>>><<<<<<<<<<
@app.get('/api/user/{user_id}', response_model=UserResponse)
def get_user(user_id : int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


@app.post('/api/users',
        response_model=UserCreate,
        status_code=status.HTTP_201_CREATED
        )
def create_user(user : UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    result = db.execute(select(models.User).where(models.User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        pw_hash=user.pw_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/api/scores/{score_id}', response_model=ScoreResponse)
def get_scores(score_id : int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Score).where(models.Score.id == score_id))
    existing_score = result.scalar().first()

    if existing_score:
        return existing_score
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score Not Found")


@app.post('/api/scores', response_model=ScoreCreate, status_code=status.HTTP_201_CREATED)
def create_score(score : ScoreCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == score.user_id))
    existing_user = result.scalar().first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")
    else:
        new_score = models.Score(
            score=score.score,
            user_id=score.user_id
        )

        db.add(new_score)
        db.commit()
        db.refresh(new_score)
        return new_score
