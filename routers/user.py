import models
from database import Base, engine, get_db
from schemas import UserCreate, UserResponse, ScoreCreate, ScoreResponse, UserUpdate, Token
from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy import select, func
from sqlalchemy.orm import Session
import pydantic
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from auth import create_access_token, verify_access_token, verify_password, hash_password, oauth2_scheme
from config import settings


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
    result = db.execute(select(models.User).where(func.lower(models.User.username) == user.username.lower()))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    result = db.execute(select(models.User).where(func.lower(models.User.email) == user.email.lower()))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = models.User(
        username=user.username,
        email=user.email.lower(),
        pw_hash=hash_password(user.pw_hash)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    result = db.execute(select(models.User).where(func.lower(models.User.email) == form_data.username.lower()))

    user = result.scalars().first()


    if not user or not verify_password(form_data.password, user.pw_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenicate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': str(user.id)},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')

@router.get('/me', response_model=UserResponse)
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    """Get the currently authenticated user"""
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )  
    result = db.execute(select(models.User).where(models.User.id == user_id_int))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            hearders={"WWW-Authenticate": "Bearer"}
        )
    return user

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




