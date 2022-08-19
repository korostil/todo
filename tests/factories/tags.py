import factory

from models import Tag
from tests.factories.base import AsyncFactory

__all__ = ('TagFactory', 'TagDataFactory')


class TagDataFactory(factory.DictFactory):
    title = factory.Faker('slug')


class TagFactory(AsyncFactory, TagDataFactory):
    ...

    class Meta:
        model = Tag
