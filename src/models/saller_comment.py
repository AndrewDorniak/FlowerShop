from sqlalchemy import Column, INTEGER, Text, ForeignKey
from sqlalchemy.orm import mapped_column

from src.models import Base


class SallerComment(Base):
    __tablename__ = 'saller_comment'

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

    saller_id = Column(
        ForeignKey('user.user_id'),
        comment='the number of the seller to whom the review is written',
    )

    reviewer_id = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE")
    )