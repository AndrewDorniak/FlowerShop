from sqlalchemy import Column, INTEGER, Text, ForeignKey
from sqlalchemy.orm import mapped_column

from src.models import Base


class LotComment(Base):
    __tablename__ = 'lot_comment'

    comment_id = Column(
        INTEGER,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )

    text = Column(
        Text,
        nullable=False,
    )

    rating = Column(
        INTEGER,
        nullable=True,
    )

    lot_id = Column(
        ForeignKey('flower_lot.lot_id'),
        comment='the number of the lot to whom the review is written',
    )

    reviewer_id = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE")
    )
