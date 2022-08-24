from databases.interfaces import Record
from sqlalchemy import delete, insert, select, update

from app.database import BaseDBModel, database
from services.exceptions import DoesNotExist


async def create_one(*, model: BaseDBModel, data: dict | None = None) -> Record:
    query = insert(model).values(**data).returning(model)
    instance = await database.fetch_one(query)
    return instance  # type: ignore


async def delete_one(*, model: BaseDBModel, pk: int | None = None) -> None:
    query = delete(model).where(model.id == pk).returning(model.id)
    instance = await database.fetch_val(query)
    if instance is None:
        raise DoesNotExist


async def get_one(*, model: BaseDBModel, pk: int | None = None) -> Record | None:
    if pk is None:
        return None

    query = select(model).filter(model.id == pk)
    instance = await database.fetch_one(query)
    if instance is None:
        raise DoesNotExist

    return instance


async def update_one(
    *, model: BaseDBModel, pk: int | None = None, data: dict | None = None
) -> Record | None:
    if pk is None:
        return None

    if data:
        query = update(model).where(model.id == pk).values(**data).returning(model)
    else:
        query = select(model).where(model.id == pk)

    instance = await database.fetch_one(query)
    if instance is None:
        raise DoesNotExist

    return instance
