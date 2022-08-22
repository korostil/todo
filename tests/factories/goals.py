import factory

from models import Goal, Status
from tests.factories.base import AsyncFactory

__all__ = ('GoalFactory', 'GoalDataFactory')


class GoalDataFactory(factory.DictFactory):
    month = None
    status = Status.NEW.value
    title = factory.Faker('slug')
    week = None
    year = None


class GoalFactory(AsyncFactory, GoalDataFactory):
    created_at = factory.Faker('date_time')

    class Meta:
        model = Goal
