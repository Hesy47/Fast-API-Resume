from pydantic import BaseModel, field_validator, model_validator
from re import match
from fastapi import HTTPException, status


class get_user_schema(BaseModel):
    id: int
    name: str
    email: str
    password: str


class create_user_schema(BaseModel):
    name: str
    email: str
    password: str
    password_confirmation: str

    @model_validator(mode="after")
    def general_validation(value):
        error_message = "The password and password confirmation are not match"

        if not value.password == value.password_confirmation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message,
            )

        return value

    @field_validator("password")
    def password_validator(value):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$"
        error_message = "The password must contain at least one Capital and one Small letter and one Number"

        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message,
            )

        if len(value) < 8:
            raise ValueError("the pass length must be at least 8 characters")

        return value

class update_user_info_schema(BaseModel):
    pass