from enum import Enum
import uuid

from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.dialects.postgresql import UUID

from src.models import Base


class UserRoles(Enum):
    CUSTOMER = 'customer'
    SALLER = 'saller'


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {"comment": "User`s data"}

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=False,
        default=uuid.uuid4,
    )

    username = Column(
        String(32),
        unique=True,
        index=True,
        nullable=False
    )

    email = Column(
        String(),
        nullable=False,
        unique=True,
    )

    password = Column(
        String(255),
        nullable=False,
    )

    user_role = Column(
        String(12),
        nullable=False,
        default=UserRoles.CUSTOMER.value,
    )
