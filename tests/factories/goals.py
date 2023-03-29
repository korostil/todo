from datetime import datetime, timedelta

import factory

from models import Goal
from tests.factories.base import AsyncFactory

__all__ = ('GoalFactory', 'GoalDataFactory')


class GoalDataFactory(factory.DictFactory):
    month = None
    title = factory.Faker('slug')
    year = None


class GoalFactory(AsyncFactory, GoalDataFactory):
    achieved_at = None
    created_at = factory.Faker('date_time')

    class Meta:
        model = Goal

    class Params:
        achieved = factory.Trait(achieved_at=datetime.now() - timedelta(minutes=1))
