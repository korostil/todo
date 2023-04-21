from datetime import datetime, timedelta

import factory

from models import Task
from services.spaces import Space
from tests.factories.base import AsyncFactory

__all__ = ('TaskFactory', 'TaskDataFactory')


class TaskDataFactory(factory.DictFactory):
    decisive = False
    description = factory.Faker('sentence')
    due_date = datetime.now().date().isoformat()
    due_time = (datetime.now() + timedelta(minutes=1)).time().isoformat()
    title = factory.Faker('slug')
    project_id = None
    space = Space.WORK.value

    class Params:
        due_tomorrow = factory.Trait(
            due_date=(datetime.now() + timedelta(days=1)).date().isoformat()
        )
        overdue = factory.Trait(
            due_date=(datetime.now() - timedelta(minutes=1)).isoformat()
        )


class TaskFactory(AsyncFactory, TaskDataFactory):
    created_at = datetime.now()
    completed_at = None
    due_date = factory.Faker('date_object')
    due_time = factory.Faker('time_object')

    class Meta:
        model = Task

    class Params:
        completed = factory.Trait(completed_at=datetime.now() - timedelta(minutes=1))
