import models
from database import Base, engine, get_db
from schemas import UserCreate, UserResponse, ScoreCreate, ScoreResponse, UserUpdate
from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
import pydantic



router = APIRouter()

@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id : int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


@router.post('',
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

@router.patch('/{user_id}',
              response_model=UserResponse,
              status_code=status.HTTP_201_CREATED)
def update_user(user_id : int, user_data: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        update_data = user_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
@router.delete('/{user_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        db.delete(user)
        db.commit()




