import sys
from pathlib import Path


sys.path.append(Path(__file__).parent)


from decimal import Decimal
import asyncio

from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from pydantic import BaseModel

from src.core.database import AsyncSessionLocal
from src.models import User, Order
from src.models.user import UserRoles


class StatisticsOneSaller(BaseModel):
    saller: str
    customer: str
    sum_price: Decimal


class Statistics(BaseModel):
    __root__: list[StatisticsOneSaller] | None


async def statistics():
    async with AsyncSessionLocal() as session:

        saller = aliased(User)
        customer = aliased(User)

        query = select(
            saller.username.label('saller'),
            customer.username.label('customer'),
            func.sum(Order.full_price).label('sum_price'),
        ).join(
            Order,
            Order.saller_id == saller.user_id,
        ).join(
            customer,
            customer.user_id == Order.customer,
        ).where(
            saller.user_role == UserRoles.SALLER.value,
        ).group_by(
            saller.username.label('saller'),
            customer.username.label('customer'),
        )
        result = await session.execute(query)
        await session.commit()

    stat = [item._asdict() for item in result.all()]
    stat = Statistics(__root__ =stat)

    with open('statistics.json', 'w') as file:
        file.write(stat.json())


if __name__ == '__main__':
    asyncio.run(statistics())