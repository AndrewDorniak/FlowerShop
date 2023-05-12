from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, validator

from src.models.flower_model import(
    FlowerColor,
    FlowerName,
)


class NewLotRequest(BaseModel):
    flower_name: str
    flower_color: str
    is_displayed: bool = Field(default=True)
    flowers_amount: int = Field(..., gt=0)
    price_for_one: Decimal = Field(..., gt=0)

    @validator('flower_name',)
    def validate_flower_name(cls, value: str):
        assert value in [
            name.value for name in FlowerName
            ], "Unvailable flower name"
        return value
    
    @validator('flower_color',)
    def validate_flower_color(cls, value: str):
        assert value in [
            color.value for color in FlowerColor
            ], "Unvailable flower name"
        return value

    
class NewLotResponse(NewLotRequest):
    class Config:
        orm_mode = True
    
    lot_id: int


class UpdateDisplayingLot(BaseModel):
    is_displayed: bool


class UserLotResponse(NewLotResponse):
    created_at: datetime
    updated_at: datetime


class UserLotsResponse(BaseModel):
    __root__: list[UserLotResponse] | None


class CommentRequest(BaseModel):
    text: str
    rating: int | None = Field(default=None, ge=0, le=5)


class LotCommentResponse(CommentRequest):
    class Config:
        orm_mode = True

    comment_id: int
    lot_id: int
    reviewer_id: UUID

class SallerCommentResponse(CommentRequest):
    class Config:
        orm_mode = True

    comment_id: int
    saller_id: UUID
    reviewer_id: UUID


class LotResponse(UserLotResponse):
    username: str = Field(..., alias="Saller")


class AllLotResponse(BaseModel):
    __root__: list[LotResponse] | None


class OrderRequest(BaseModel):
    lot_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderResponse(OrderRequest):
    customer: str
    saller: str
    full_price: Decimal
    created_at: datetime
    order_id: int
