from uuid import UUID
from fastapi import HTTPException, status, Request
from sqlalchemy import select, and_, update, insert, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.models import (
    User,
    FlowerLot,
    LotComment,
    SallerComment,
    Order,
)
from src.auth.utils import fetch_client_id_from_jwt
from src.models.user import UserRoles
from src.core.database import AsyncSessionLocal
from src.api.shop.schemas import (
    NewLotRequest,
    CommentRequest,
)


async def get_saller_by_id(
    session: AsyncSession,
    user_id: str,
):
    query = select(
        User,
    ).where(
        and_(
            User.user_id == user_id,
            User.user_role == UserRoles.SALLER.value,
        )
    )
    result = await session.execute(query)
    return result.scalar()


async def check_saller(request: Request):
    user_id = await fetch_client_id_from_jwt(request)
    async with AsyncSessionLocal() as session:
        user = await get_saller_by_id(
            session,
            user_id,
        )
        await session.commit()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You has not permissions",
        )
    return user


async def create_new_lot_entity(
    session: AsyncSession,
    data: NewLotRequest,
    saller_id: UUID,
):
    lot = FlowerLot(
        **data.dict(),
        saller_id=saller_id,
    )
    session.add(lot)
    await session.commit()
    return lot


async def update_lot_displaying_mode(
    session: AsyncSession,
    lot_id: int,
    saller_id: UUID,
    is_displayed: bool,
):
    query = update(
        FlowerLot,
    ).where(
        and_(
            FlowerLot.lot_id == lot_id,
            FlowerLot.saller_id == saller_id,
        )
    ).values(
        {"is_displayed": is_displayed}
    ).returning(
        FlowerLot.is_displayed,
    )
    is_displayed_status = await session.execute(query)
    await session.commit()
    return is_displayed_status.scalar()


async def show_lots(
    session: AsyncSession,
    saller_id: UUID,
):
    query = select(
        FlowerLot,
    ).where(
        FlowerLot.saller_id == saller_id,
    )

    result = await session.execute(query)
    await session.commit()
    return result.all()


async def show_one_lot(
    session: AsyncSession,
    saller_id: UUID,
    lot_id: int,
):
    query = select(
        FlowerLot,
    ).where(
        and_(
            FlowerLot.saller_id == saller_id,
            FlowerLot.lot_id == lot_id,
        )
    )

    result = await session.execute(query)
    await session.commit()
    return result.scalar()




async def delete_one_lot(
    session: AsyncSession,
    saller_id: UUID,
    lot_id: int,
):
    query = delete(
        FlowerLot,
    ).where(
        and_(
            FlowerLot.saller_id == saller_id,
            FlowerLot.lot_id == lot_id,
        )
    )

    await session.execute(query)
    await session.commit()


async def lot_comment_add(
    session: AsyncSession,
    reviewer_id: UUID,
    lot_id: int,  
    body: CommentRequest,
):
    query = insert(
        LotComment,
    ).values(
        {
            "lot_id": lot_id,
            "text": body.text,
            "reviewer_id": reviewer_id,
            "rating": body.rating,

        },
    ).returning(
        LotComment,
    )
    result = await session.execute(query)
    await session.commit()
    return result.scalar()


async def get_saller_by_username(
    session: AsyncSession,
    saller_name: str,
):
    query = select(
        User.user_id,
    ).where(
        and_(
            User.username == saller_name,
            User.user_role == UserRoles.SALLER.value,
        )
    )
    result = await session.execute(query)
    return result.scalar()


async def saller_comment_add(
    session: AsyncSession,
    reviewer_id: UUID,
    saller_id: UUID,  
    body: CommentRequest,
):
    query = insert(
        SallerComment,
    ).values(
        {
            "saller_id": saller_id,
            "text": body.text,
            "reviewer_id": reviewer_id,
            "rating": body.rating,

        },
    ).returning(
        SallerComment,
    )
    result = await session.execute(query)
    await session.commit()
    return result.scalar()


async def get_all_offers(
    session: AsyncSession,
):
    query = select(
        FlowerLot.lot_id,
        FlowerLot.flower_name,
        FlowerLot.flower_color,
        FlowerLot.flowers_amount,
        FlowerLot.price_for_one,
        FlowerLot.created_at,
        FlowerLot.updated_at,
        User.username.label('Saller'),
    ).join(
        User,
        User.user_id == FlowerLot.saller_id,
    ).where(
        FlowerLot.is_displayed == True,
    )
    result = await session.execute(query)
    await session.commit()
    return result.all()


async def get_concreat_saller_offers(
    session: AsyncSession,
    saller_name: str,
):
    query = select(
        FlowerLot.lot_id,
        FlowerLot.flower_name,
        FlowerLot.flower_color,
        FlowerLot.flowers_amount,
        FlowerLot.price_for_one,
        FlowerLot.created_at,
        FlowerLot.updated_at,
        User.username.label('Saller'),
    ).join(
        User,
        User.user_id == FlowerLot.saller_id,
    ).where(
        FlowerLot.is_displayed == True,
    ).filter(
        User.username == saller_name,
    )
    result = await session.execute(query)
    await session.commit()
    return result.all()


async def get_customer_by_id(
    session: AsyncSession,
    user_id: str,
):
    query = select(
        User,
    ).where(
        and_(
            User.user_id == user_id,
            User.user_role == UserRoles.CUSTOMER.value,
        )
    )
    result = await session.execute(query)
    return result.scalar()


async def check_customer(request: Request):
    user_id = await fetch_client_id_from_jwt(request)
    async with AsyncSessionLocal() as session:
        user = await get_customer_by_id(
            session,
            user_id,
        )
        await session.commit()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You has not permissions",
        )
    return user


async def fetch_lot(
    session: AsyncSession,
    lot_id: int,
):
    query = select(
        FlowerLot,
    ).where(
        FlowerLot.lot_id == lot_id,
    )
    result = await session.execute(query)
    return result.scalar()


async def create_order_entity(
    session: AsyncSession,
    quantity: int,
    lot: FlowerLot,
    customer_id: UUID, 
):
    if lot.flowers_amount < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Available flower amount: {lot.flowers_amount}, got: {quantity}"
        )
    full_price = lot.price_for_one * quantity

    order_query = insert(
        Order,
    ).values(
        {
            "lot_id": lot.lot_id,
            "saller_id": lot.saller_id,
            "customer": customer_id,
            "quantity": quantity,
            "full_price": full_price,
        },
    ).returning(Order)

    query = update(
        FlowerLot,
    ).where(
        FlowerLot.lot_id == lot.lot_id,
    ).values(
        {'flowers_amount': lot.flowers_amount - quantity}
    )

    saller = await get_saller_by_id(session, lot.saller_id)
    order =await session.execute(order_query)
    await session.execute(query)
    await session.commit()
    return (order.scalar(), saller.username)


async def show_saller_comments(
    session: AsyncSession,
    saller_name: str,  
):
    query = select(
        SallerComment,
    ).join(
        User,
        User.user_id == SallerComment.saller_id,
    ).filter(
        User.username == saller_name,
    )

    comments = await session.execute(query)
    await session.commit()
    return comments.all()


async def show_lot_comments(
    session: AsyncSession,
    lot_id: int,  
):
    query = select(
        LotComment,
    ).where(
        LotComment.lot_id == lot_id,
    )

    comments = await session.execute(query)
    await session.commit()
    return comments.scalars().all()


async def get_deals(
    session: AsyncSession,
    user_id: UUID,
):
    customer = aliased(User)
    saller = aliased(User)

    query = select(
        Order.lot_id,
        Order.full_price,
        Order.created_at,
        Order.quantity,
        Order.order_id,
        customer.username.label('customer'),
        saller.username.label('saller'),
    ).join(
        customer,
        customer.user_id == Order.customer,
    ).join(
        saller,
        saller.user_id == Order.saller_id,
    ).filter(
        or_(
            Order.customer == user_id,
            Order.saller_id == user_id,
        )
    )

    result = await session.execute(query)
    await session.commit()
    return result.all()