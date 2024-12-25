from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from random import choices
from string import ascii_lowercase
from typing import List
from models import engine, SessionLocal, Base
from models import User, Token
from schema import GetUserSchema, CreateUserSchema, UpdateUserInfoSchema
from schema import LoginSchema

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def token_generator():
    base_token = "".join(choices(ascii_lowercase, k=64))
    return base_token


@app.get("/users", response_model=List[GetUserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user in your database!",
        )
    return users


@app.get("/users/{user_id}", response_model=GetUserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@app.post("/signup")
def signup(user: CreateUserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email already registered",
        )

    new_user = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password=user.password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    message = "Signup was successful"
    return {
        "Message": message,
        "Username": new_user.username,
        "Email": new_user.email,
        "Phone_number": new_user.phone_number,
        "Password": new_user.password,
        "Join_date": new_user.join_date,
    }


@app.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or user.password != db_user.password:
        raise HTTPException("Invalid Username or PassWord")

    db_token = Token(user_id=db_user.id, Token=token_generator())

    return {
        "Message": "Login successfully!",
        "User_id": db_token.user_id,
        "Token": db_token.token,
        "Expire_at": db_token.expires_at,
    }


@app.delete("/remove-user/{user_id}", response_model=dict)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user)
    db.commit()
    return {"Message": f"user {user.username} has been deleted successfully"}


@app.put("/edit-profile/{user_id}", response_model=dict)
def edit_profile(
    user_id: int, user: UpdateUserInfoSchema, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not db_user.password == user.old_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="your current password is wrong",
        )

    db_user.password = user.password

    db.commit()
    db.refresh(db_user)

    return {"Message": "Profile has been updated successfully"}
