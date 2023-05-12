from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.api.registration.schemas import (
    RegistrationRequest,
    RegistrationResponse,
)
from src.api.utils import (
    get_password_hash,
    REGISTRATION_ERROR_MESSAGES,
)
from src.exceptions.exceptions import DuplicateExistingUserError
from src.api.registration import crud


router = APIRouter()


@router.post(
    "/registration/new",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrates_new_user(
    session: AsyncSession = Depends(get_async_session),
    body: RegistrationRequest = Body(),
):
    password = get_password_hash(body.password)

    try:
        client = await crud.registrate_new_client(
            session,
            body,
            password,
        )
    except DuplicateExistingUserError:
        row = await crud.user_constraints_errors(
            session,
            body.username,
            body.email,
        )

        # throws exceptions if unique fields already exist
        # in the database and its are owned by other users
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            [
                REGISTRATION_ERROR_MESSAGES[key]
                for key, value in row._asdict().items() if value
            ],
        )

    return client
