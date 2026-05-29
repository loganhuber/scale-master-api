import models
from database import Base, engine, get_db
from schemas import UserCreate, UserResponse, ScoreCreate, ScoreResponse
from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session


router = APIRouter()


@router.get('/{score_id}', response_model=ScoreResponse)
def get_scores(score_id : int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Score).where(models.Score.id == score_id))
    existing_score = result.scalars().first()

    if existing_score:
        return existing_score
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score Not Found")


@router.post('', response_model=ScoreCreate, status_code=status.HTTP_201_CREATED)
def create_score(score : ScoreCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == score.user_id))
    existing_user = result.scalars().first()

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