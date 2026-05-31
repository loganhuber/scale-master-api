import models
from database import Base, engine, get_db
from schemas import UserCreate, UserResponse, ScoreCreate, ScoreResponse
from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import CurrentUser
from datetime import datetime, timezone

router = APIRouter()

@router.get('/{score_id}', response_model=ScoreResponse)
def get_score(score_id : int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Score).where(models.Score.id == score_id))
    existing_score = result.scalars().first()

    if existing_score:
        return existing_score
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score Not Found")


@router.post('', response_model=ScoreCreate, status_code=status.HTTP_201_CREATED)
def create_score(score : ScoreCreate, current_user: CurrentUser, db: Annotated[Session, Depends(get_db)]):

    now = datetime.now(timezone.utc)

    new_score = models.Score(
        score=score.score,
        user_id=current_user.id,
        scale=score.scale,
        scale_key=score.scale_key,
        date=now
    )

    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score
    

@router.delete('/{score_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_score(score_id: int, current_user : CurrentUser, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Score).where(models.Score.id == score_id))
    score = result.scalars().first()

    if not score:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if score.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this score")
    
    db.delete(score)
    db.commit()