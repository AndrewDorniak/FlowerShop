from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        description="Specify your username",
        example="SimpleUser",
    )

    password: str = Field(
        ...,
        description="Specify your password",
    )


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
