import factory
import funcy

from models import Tag
from tests.factories.base import AsyncFactory

__all__ = ('TagFactory', 'TagDataFactory')


class TagDataFactory(factory.DictFactory):
    title = factory.Faker('slug')


class TagFactory(AsyncFactory, TagDataFactory):
    id = factory.Sequence(funcy.identity)

    class Meta:
        model = Tag
