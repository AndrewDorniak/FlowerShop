from sqlalchemy import Column, func, DateTime
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
    )
