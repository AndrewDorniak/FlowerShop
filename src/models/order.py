from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DECIMAL,
)

from src.models import Base


class UserRoles(Enum):
    CUSTOMER = 'customer'
    SALLER = 'saller'


class Order(Base):
    __tablename__ = 'order'

    order_id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    lot_id = Column(ForeignKey('flower_lot.lot_id'))
    saller_id = Column(ForeignKey('user.user_id'))
    customer = Column(ForeignKey('user.user_id'))
    quantity = Column(Integer, nullable=False)
    full_price = Column(DECIMAL(10,2), nullable=False)
