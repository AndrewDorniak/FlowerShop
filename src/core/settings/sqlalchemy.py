from pydantic import AnyUrl
from pydantic import BaseModel


class SqlAlchemySettings(BaseModel):
    """SQLAlchemy settings"""

    url: AnyUrl | None = None