from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import User


async def get_user_by_username(session: AsyncSession, username: str):
    query = select(User).filter(User.username == username)
    result = await session.execute(query)
    return result.scalars().first()