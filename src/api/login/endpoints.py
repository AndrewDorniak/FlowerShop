"""
    This module provides endpoint to login
    and refresh yours JWT token.

"""


from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.api.login.schemas import LoginRequest, LoginResponse
from src.api.utils import verify_password
from src.api.login.crud import get_user_by_username
from src.auth.utils import generate_pair_jwt, fetch_client_id_from_jwt


router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    session: AsyncSession = Depends(get_async_session),
    body: LoginRequest = Body(),
):
    user = await get_user_by_username(session, body.username)

    if not user or not verify_password(
        body.password,
        user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid username or password",
        )
    access_token, refresh_token = generate_pair_jwt(user.user_id)

    return{
        'access_token': access_token,
        'refresh_token': refresh_token,
    }


@router.get(
    "/refresh",
)
async def update_token_pair(
    user_id: str = Depends(fetch_client_id_from_jwt)
):
    access_token, refresh_token = generate_pair_jwt(user_id)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
