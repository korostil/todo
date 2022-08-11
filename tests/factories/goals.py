import factory
import funcy

from models import Goal
from tests.factories.base import AsyncFactory

__all__ = ('GoalFactory', 'GoalDataFactory')


class GoalDataFactory(factory.DictFactory):
    month = None
    title = factory.Faker('slug')
    week = None
    year = None


class GoalFactory(AsyncFactory, GoalDataFactory):
    created_at = factory.Faker('date_time')
    id = factory.Sequence(funcy.identity)

    class Meta:
        model = Goal
