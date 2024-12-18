from pydantic import BaseModel, Field
from typing import Optional


class Create_User(BaseModel):
    username: str
    password: str = Field(None, min_length=6, description="test case")
    email: str
    age: Optional[int]
