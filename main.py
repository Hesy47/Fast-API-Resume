from fastapi import FastAPI
from models import Base, engine
from auth_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/api", tags=["authentication"])
