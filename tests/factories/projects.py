import factory
import funcy

from models import Project
from services.spaces import Space
from tests.factories.base import AsyncFactory

__all__ = ('ProjectFactory', 'ProjectDataFactory')


class ProjectDataFactory(factory.DictFactory):
    archived = False
    description = factory.Faker('sentence')
    title = factory.Faker('slug')
    space = Space.WORK.value


class ProjectFactory(AsyncFactory, ProjectDataFactory):
    id = factory.Sequence(funcy.identity)

    class Meta:
        model = Project
