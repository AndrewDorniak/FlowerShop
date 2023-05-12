from pydantic import Field
from uvicorn.config import (
    HTTPProtocolType,
    LoopSetupType,
)

from pydantic import BaseModel


class UvicornSettings(BaseModel):
    """Uvicorn Settings"""

    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8000
    loop: LoopSetupType = "auto"
    http: HTTPProtocolType = "auto"
    reload: bool = Field(default=None, description="Enable auto-reload.")
    workers: int | None = None
