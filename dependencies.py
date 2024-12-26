from datetime import datetime, timedelta
from random import choices
from string import ascii_lowercase
from models import SessionLocal
import bcrypt


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


def hashed_password_generator(base_password):
    salt = bcrypt.gensalt(rounds=6)
    hashed_password = bcrypt.hashpw(base_password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def hashed_password_checker(base_pass, data_pass):
    return bcrypt.checkpw(base_pass.encode("utf-8"), data_pass.encode("utf-8"))
