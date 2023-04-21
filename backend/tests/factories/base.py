import asyncio

import factory
from sqlalchemy import insert

from app.database import database


class AsyncFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda x: x + 1)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            query = insert(model_class).values(**kwargs).returning(model_class)
            record = await database.fetch_one(query)
            return record

        return asyncio.create_task(maker_coroutine())

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]
