from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from src.core import settings


engine = create_async_engine(
    settings.postgres.url,
    echo=settings.postgres.echo,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session