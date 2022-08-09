from datetime import datetime, timedelta

import factory
import funcy

from models import Project
from services.spaces import Space
from tests.factories.base import AsyncFactory

__all__ = ('ProjectFactory', 'ProjectDataFactory')


class ProjectDataFactory(factory.DictFactory):
    description = factory.Faker('sentence')
    title = factory.Faker('slug')
    space = Space.WORK.value


class ProjectFactory(AsyncFactory, ProjectDataFactory):
    id = factory.Sequence(funcy.identity)
    archived_at = None

    class Meta:
        model = Project

    class Params:
        archived = factory.Trait(archived_at=datetime.now() - timedelta(minutes=1))
