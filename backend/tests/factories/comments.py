import factory

from models import Comment
from tests.factories.base import AsyncFactory

__all__ = ('CommentFactory', 'CommentDataFactory')


class CommentDataFactory(factory.DictFactory):
    text = factory.Faker('text')


class CommentFactory(AsyncFactory, CommentDataFactory):
    created_at = factory.Faker('date_time')

    class Meta:
        model = Comment
