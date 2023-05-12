from contextlib import suppress

from fastapi import APIRouter, Depends, Body, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.core.database import get_async_session
from src.api.shop.crud import (
    check_saller,
    create_new_lot_entity,
    update_lot_displaying_mode,
    show_lots,
    show_one_lot,
    lot_comment_add,
    get_saller_by_username,
    saller_comment_add,
    get_all_offers,
    get_concreat_saller_offers,
    check_customer,
    delete_one_lot,
    fetch_lot,
    create_order_entity,
    show_saller_comments,
    show_lot_comments,
    get_deals,
)
from src.api.shop.schemas import (
    NewLotRequest,
    NewLotResponse,
    UpdateDisplayingLot,
    UserLotsResponse,
    UserLotResponse,
    CommentRequest,
    LotCommentResponse,
    SallerCommentResponse,
    AllLotResponse,
    OrderRequest,
    OrderResponse,
)
from src.models import User
from src.auth.utils import fetch_client_id_from_jwt


router = APIRouter()


@router.post(
    "/new-lot",
    status_code=status.HTTP_201_CREATED,
    response_model=NewLotResponse,
)
async def create_new_lot(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(check_saller),
    body: NewLotRequest = Body(),
):
    lot = await create_new_lot_entity(session, body, user.user_id)
    return lot


@router.patch(
    "/lot/{lot_id}/display",
    status_code=status.HTTP_200_OK,
)
async def change_displaying_mode(
    lot_id: int = Path(gt=0),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(check_saller),
    body: UpdateDisplayingLot = Body(),
):
    displayed_status = await update_lot_displaying_mode(
        session,
        lot_id,
        user.user_id,
        body.is_displayed,
    )
    if not displayed_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lot not found or you do not have permissions",
        )
    return {'message': 'displaying status has been successfully updated'}


@router.get(
    '/lots',
    status_code=status.HTTP_200_OK,
    response_model=UserLotsResponse,
)
async def show_user_lots(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(check_saller),
):
    """Endpoint to sallers.

    Provides list of existing lots, related to requested user
    if he is a saller.

    """
    lots = await show_lots(session, user.user_id)

    with suppress([IndexError]):
        lots = [lot[0] for lot in lots]

    return lots


@router.get(
    '/lots/{lot_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserLotResponse | None,
)
async def show_one_user_lot(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(check_saller),
    lot_id: int = Path(gt=0),
):
    """Endpoint to sallers.

    Provides existing lot, related to requested user
    if he is a saller.

    """
    lot = await show_one_lot(session, user.user_id, lot_id)

    return lot


@router.delete(
    '/lots/{lot_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_one_user_lot(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(check_saller),
    lot_id: int = Path(gt=0),
):
    """Endpoint to sallers.

    Deletes existing lot, related to requested user
    if he is a saller.

    """
    await delete_one_lot(session, user.user_id, lot_id)


@router.post(
    '/lot/{lot_id}/comment',
    status_code=status.HTTP_201_CREATED,
    response_model=LotCommentResponse,
)
async def add_comment_to_lot(
    session: AsyncSession = Depends(get_async_session),
    reviewer: User = Depends(fetch_client_id_from_jwt),
    lot_id: int = Path(gt=0),
    body: CommentRequest = Body(),
):
    try:
        comment = await lot_comment_add(session, reviewer, lot_id, body)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lot not found",
        )

    return comment


@router.post(
    '/saller/{saller_name}/comment',
    status_code=status.HTTP_201_CREATED,
    response_model=SallerCommentResponse,
)
async def add_comment_to_saller(
    session: AsyncSession = Depends(get_async_session),
    reviewer: User = Depends(fetch_client_id_from_jwt),
    saller_name: str = Path(regex="^(?=.*?[A-Z])(?=.*?[a-z])"),
    body: CommentRequest = Body(),
):
    saller_id = await get_saller_by_username(session, saller_name)
    if not saller_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified saller does not exists",
        )
    
    try:
        comment = await saller_comment_add(session, reviewer, saller_id, body)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified saller does not exists",
        )

    return comment


@router.get(
    "/flowershop/all_flowers",
    response_model=AllLotResponse,
    status_code=status.HTTP_200_OK,
)
async def show_all_offers(
    session: AsyncSession = Depends(get_async_session),
    _: User = Depends(fetch_client_id_from_jwt),
):
    lots = await get_all_offers(session)
    return lots


@router.get(
    "/flowershop/all_flowers/{saller_name}",
    response_model=AllLotResponse,
    status_code=status.HTTP_200_OK,
)
async def show_concreat_saller_offers(
    session: AsyncSession = Depends(get_async_session),
    _: User = Depends(fetch_client_id_from_jwt),
    saller_name: str = Path(..., regex="^(?=.*?[A-Z])(?=.*?[a-z])"),
):
    lots = await get_concreat_saller_offers(session, saller_name)
    return lots


@router.post(
    "/create-order",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def purchase(
    session: AsyncSession = Depends(get_async_session),
    customer: User = Depends(check_customer),
    body: OrderRequest = Body(),
):

    lot = await fetch_lot(session, body.lot_id)

    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lot not found",
        )
    order, saller_name = await create_order_entity(
        session,
        body.quantity,
        lot,
        customer.user_id,
    )

    response = {
        "customer": customer.username,
        "saller": saller_name,
        "lot_id": order.lot_id,
        "quantity": order.quantity,
        "full_price": order.full_price,
        "created_at": order.created_at,
        "order_id": order.order_id,
    }

    return response



@router.get(
    '/saller/{saller_name}/comment',
    status_code=status.HTTP_200_OK,
    response_model=list[SallerCommentResponse] | None,
)
async def get_saller_comments(
    session: AsyncSession = Depends(get_async_session),
    _: User = Depends(fetch_client_id_from_jwt),
    saller_name: str = Path(regex="^(?=.*?[A-Z])(?=.*?[a-z])"),
):
    comments = await show_saller_comments(session, saller_name)

    with suppress([IndexError]):
        comments = [comment[0] for comment in comments]

    return comments


@router.get(
    '/lot/{lot_id}/comment',
    status_code=status.HTTP_200_OK,
    response_model=list[LotCommentResponse] | None,
)
async def show_all_lot_comments(
    session: AsyncSession = Depends(get_async_session),
    _: User = Depends(fetch_client_id_from_jwt),
    lot_id: int = Path(gt=0),
):
    return await show_lot_comments(session, lot_id)


@router.get(
    "/deals",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderResponse] | None,
)
async def user_deals(
    session: AsyncSession = Depends(get_async_session),
    user_id: str = Depends(fetch_client_id_from_jwt),
):
    result = await get_deals(session, user_id)
    return [row._asdict() for row in result]
