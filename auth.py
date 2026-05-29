from datetime import datetime, timedelta
import jwt

from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from config import settings

pw_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/user/token')

def hash_password(password: str) -> str:
    return pw_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pw_hash.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a jwt token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timedelta.utc) + expires_delta
    else:
        expire = datetime.now(timedelta.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm
        )
    return encoded_jwt

def verify_access_token(token: str) -> str | None:
    """Verify access token and return User id if valid"""
    try:
        payload = jwt.decode(
            token, settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require" : ["exp", "sub"]}
        )
    except jwt.InvalidTokenError:
        return None
    
    return payload.get('sub')


