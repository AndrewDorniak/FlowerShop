from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, validator

from src.models.user import UserRoles
from src.api.utils import check_password


class RegistrationRequest(BaseModel):
    username: str = Field(
        ...,
        regex="^(?=.*?[A-Z])(?=.*?[a-z])",
        max_length=32,
        description="Your username",
        example="ExampleUser",
    )

    email: EmailStr = Field(
        ...,
        description="Your email",
        example="ExampleUser@mail.com",
    )

    user_role: str = Field(
        ...,
        description="User role in the system",
        example="customer",
    )

    password: str = Field(
        ...,
        description="User`s password",
        example='Qwerty1_}',
    )

    @validator("user_role",)
    def validate_user_role(cls, value: str):

        assert value in [
            role.value for role in UserRoles
            ], "Available roles: customer/saller"
        return value
    
    @validator("password",)
    def validate_password(cls, value: str):
        assert check_password(value), (
            "Password must contain 8 to 20 symbols," +
            "1 uppercase and 1 lowercase letter, 1 digit and " +
            "1 special character"
        )
        return value


class RegistrationResponse(BaseModel):

    class Config:
        orm_mode = True

    user_id: UUID
    username: str
    email: EmailStr
    user_role: str