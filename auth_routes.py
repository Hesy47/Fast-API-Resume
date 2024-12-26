from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import User, Token
from auth_schema import GetUserSchema, CreateUserSchema
from auth_schema import UpdateUserInfoSchema, LoginSchema
from dependencies import get_db, token_expire_time, token_generator
from dependencies import hashed_password_generator, hashed_password_checker

router = APIRouter()


@router.get("/users", response_model=List[GetUserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user in your database!",
        )
    return users


@router.get("/users/{user_id}", response_model=GetUserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post("/signup")
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
        password=hashed_password_generator(user.password),
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


@router.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or user.password != db_user.password:
        raise HTTPException("Invalid Username or PassWord")

    db_token = Token(
        user_id=db_user.id,
        token=token_generator(),
        expires_at=token_expire_time(),
    )

    return {
        "Message": "Login successfully!",
        "User_id": db_token.user_id,
        "Token": db_token.token,
        "Expire_at": db_token.expires_at,
    }


@router.delete("/remove-user/{user_id}", response_model=dict)
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


@router.put("/edit-profile/{user_id}", response_model=dict)
def edit_profile(
    user_id: int, user: UpdateUserInfoSchema, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not hashed_password_checker(user.old_password,db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="your current password is wrong",
        )

    db_user.password = hashed_password_generator(user.password)

    db.commit()
    db.refresh(db_user)

    return {"Message": "Profile has been updated successfully"}
