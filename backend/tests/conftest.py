import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import BaseDBModel, database
from main import app

engine = create_async_engine(app.settings.database_url)
async_session = sessionmaker(class_=AsyncSession)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
@pytest.fixture(scope='session')
async def client():
    client = AsyncClient(
        app=app,
        base_url='http://test',
        headers={'Authorization': 'Bearer secret_token'},
    )
    async with client:
        yield client


@pytest.mark.asyncio
@pytest.fixture(scope='session')
async def anonymous_client():
    client = AsyncClient(app=app, base_url='http://test')
    async with client:
        yield client


@pytest.fixture(autouse=True, scope='session')
async def tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.drop_all)
        await conn.run_sync(BaseDBModel.metadata.create_all)


@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def connection():
    await database.connect()
    yield
    await database.disconnect()
