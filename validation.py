from enum import Enum
from pydantic import BaseModel


class ModelName(str, Enum):
    it = "Amir"
    social = "Amin"
    sell = "Rezo"


class User(BaseModel):
    username: str
    password: str
    phone:int | None = None
    email: str | None = None
