from pydantic import BaseModel


class AuthSettings(BaseModel):

    jwt_secret_key: str = "verysecretkey"
    jwt_algorithm: str = "HS256"
    access_lifetime: int = 15
    refresh_lifetime: int = 1440
