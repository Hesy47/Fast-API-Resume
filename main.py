from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import engine, SessionLocal, Base
from models import User
from schema import get_user_schema, create_user_schema

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=List[get_user_schema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    if not users:
        raise HTTPException(
            status_code=404, detail="There is no user in your database!"
        )
    return users


@app.get("/users/{user_id}", response_model=get_user_schema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/signup")
def signup(user: create_user_schema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email, password=user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    message = "Signup was successful"
    return {"Message": message, "information": new_user}


@app.delete("/remove-user/{user_id}", response_model=dict)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"Message": f"user {user.name} has been deleted successfully"}
