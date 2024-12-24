from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import engine, SessionLocal, Base
from models import User
from schema import GetUserSchema, CreateUserSchema, UpdateUserInfoSchema
from schema import CreateTokenSchema, LoginSchema

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    new_user = User(name=user.name, email=user.email, password=user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    message = "Signup was successful"
    return {"Message": message, "information": new_user}


@app.post("/login")
def login():
    pass


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
    return {"Message": f"user {user.name} has been deleted successfully"}


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
