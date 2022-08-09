from datetime import datetime, timedelta

import factory
import funcy

from models import Task
from services.spaces import Space
from tests.factories.base import AsyncFactory

__all__ = ('TaskFactory', 'TaskDataFactory')


class TaskDataFactory(factory.DictFactory):
    description = factory.Faker('sentence')
    due = (datetime.now() + timedelta(minutes=1)).isoformat()
    title = factory.Faker('slug')
    space = Space.WORK.value

    class Params:
        due_tomorrow = factory.Trait(
            due=(datetime.now() + timedelta(days=1)).isoformat()
        )
        overdue = factory.Trait(due=(datetime.now() - timedelta(minutes=1)).isoformat())


class TaskFactory(AsyncFactory, TaskDataFactory):
    created_at = factory.Faker('date_time')
    completed_at = None
    due = factory.Faker('date_time')
    id = factory.Sequence(funcy.identity)

    class Meta:
        model = Task

    class Params:
        completed = factory.Trait(completed_at=datetime.now() - timedelta(minutes=1))
