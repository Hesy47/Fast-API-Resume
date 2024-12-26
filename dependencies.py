from datetime import datetime, timedelta
from random import choices
from string import ascii_lowercase
from models import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def token_expire_time():
    expires_at = datetime.now() + timedelta(hours=3)
    return str(expires_at)


def token_generator():
    base_token = "".join(choices(ascii_lowercase, k=64))
    return base_token
