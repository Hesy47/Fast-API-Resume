from pydantic import BaseModel, Field


class get_user_schema(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class create_user_schema(BaseModel):
    name: str
    email: str
    password: str
