from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, model_validator, Field
from re import match


class GetUserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str


class CreateUserSchema(BaseModel):
    username: str
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
        error_message_1 = "The password must contain at least one Capital and one Small letter and one Number"
        error_message_2 = "the pass length must be at least 8 characters"

        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message_1,
            )

        if len(value) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message_2,
            )

        return value


class LoginSchema(BaseModel):
    username: str
    password: str


class CreateTokenSchema(BaseModel):
    token: str = Field(readOnly=True)
    created_at: str = Field(readOnly=True)
    expires_at: str = Field(readOnly=True)


class UpdateUserInfoSchema(BaseModel):
    old_password: str
    password: str
    password_confirmation: str

    @model_validator(mode="after")
    def general_validation(value):
        error_message_1 = "The password and password confirmation are not match"
        error_message_2 = "The new password must not be the same as old password"
        error_message_3 = "The password must contain at least one Capital and one Small letter and one Number"
        error_message_4 = "the pass length must be at least 8 characters"
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$"

        if not value.password == value.password_confirmation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message_1,
            )

        if value.old_password == value.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error_message_2
            )

        if not match(pattern, value.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message_3,
            )

        if len(value.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message_4,
            )

        return value
