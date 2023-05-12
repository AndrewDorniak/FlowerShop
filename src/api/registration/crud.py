from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import INTEGER, Row, func, select, insert
from pydantic import EmailStr

from src.api.registration.schemas import RegistrationRequest
from src.models import User
from src.exceptions.exceptions import DuplicateExistingUserError


async def user_constraints_errors(
        session: AsyncSession,
        username: str,
        email: EmailStr,
):

    query = select(
        func.max(
            func.cast(User.email == email, INTEGER),
        ).label('email'),
        func.max(
            func.cast(User.username == username, INTEGER),
        ).label('username'),
    )
    users = await session.execute(query)
    return users.fetchone()


async def registrate_new_client(
        session: AsyncSession,
        body: RegistrationRequest,
        password: str,
) -> Optional[Row[tuple]]:

    query = insert(User).values(
        username=body.username,
        email=body.email,
        password=password,
        user_role=body.user_role,
    ).returning(
        User.user_id,
        User.email,
        User.username,
        User.user_role,
    )
    try:
        client = await session.execute(query)
    except IntegrityError:
        await session.rollback()
        raise DuplicateExistingUserError()
    else:
        await session.commit()
        return client.fetchone()
