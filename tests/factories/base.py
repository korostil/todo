import asyncio

from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import insert

from app.database import database


class AsyncFactory(SQLAlchemyModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            query = insert(model_class).values(**kwargs).returning(model_class)
            project = await database.fetch_one(query)
            return project

        return asyncio.create_task(maker_coroutine())

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]
