from sqlalchemy import Column, create_engine, func, ForeignKey
from sqlalchemy import Integer, String, BigInteger, Date, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import timedelta, datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def token_expire_time():
    expires_at = datetime.now() + timedelta(hours=3)
    return expires_at


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(11), unique=True, nullable=False)
    join_date = Column(Date, default=func.current_date())
    token = relationship("Token", back_populates="user")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False, default=token_expire_time())
    is_revoked = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="token")
