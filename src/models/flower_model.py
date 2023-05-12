from enum import Enum

from sqlalchemy import (
    Boolean,
    Integer,
    Column,
    ForeignKey,
    DECIMAL,
    String,
)
from sqlalchemy.orm import mapped_column

from src.models import Base


class FlowerName(Enum):
    CHAMOMILE = 'chamomile'
    TULIP = 'tulip'
    ROSE = 'rose'
    PROTEA = 'protea'


class FlowerColor(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    YELLOW = 'yellow'


class FlowerLot(Base):
    __tablename__ = 'flower_lot'

    lot_id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )

    saller_id = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE")
    )

    flower_name = Column(
        String,
        nullable=False,
        index=True,
    )

    flower_color = Column(
        String,
        nullable=False,
    )

    is_displayed = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    flowers_amount = Column(
        Integer,
        nullable=False,
    )

    price_for_one = Column(
        DECIMAL(12, 2),
        nullable=False,
    )
