from pydantic import BaseModel, PostgresDsn, SecretStr


class PostgreSQLSettings(BaseModel):
    """Database Settings"""

    echo: bool = False
    url: PostgresDsn = 'postgresql+asyncpg://postgres:password@localhost:5432/postgresdb' # noqa
    user: str = 'postgres'
    db: str = 'flowers_db'
    password: SecretStr = SecretStr('password')