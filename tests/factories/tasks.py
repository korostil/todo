from datetime import datetime, timedelta

import factory

from models import Task
from services.spaces import Space
from tests.factories.base import AsyncFactory

__all__ = ('TaskFactory', 'TaskDataFactory')


class TaskDataFactory(factory.DictFactory):
    decisive = False
    description = factory.Faker('sentence')
    due = (datetime.now() + timedelta(minutes=1)).isoformat()
    title = factory.Faker('slug')
    project_id = None
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

    class Meta:
        model = Task

    class Params:
        completed = factory.Trait(completed_at=datetime.now() - timedelta(minutes=1))
