from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from random import choices
from string import ascii_lowercase
from models import SessionLocal, Token
import bcrypt

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def token_expire_time():
    expires_at = datetime.now() + timedelta(hours=3)
    return expires_at


def token_generator():
    base_token = "".join(choices(ascii_lowercase, k=64))
    return base_token


def hashed_password_generator(base_password):
    salt = bcrypt.gensalt(rounds=10)
    hashed_password = bcrypt.hashpw(base_password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def hashed_password_checker(base_pass, data_pass):
    return bcrypt.checkpw(base_pass.encode("utf-8"), data_pass.encode("utf-8"))


def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    db_token = db.query(Token).filter(Token.token == token).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if db_token.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if db_token.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return db_token
