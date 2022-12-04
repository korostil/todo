from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import BaseDBModel

__all__ = ('Goal', 'Status')


class Status(Enum):
    NEW = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Goal(BaseDBModel):
    __tablename__ = 'goal'

    id = Column(Integer, primary_key=True)

    archived_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    month = Column(Integer)
    projects = relationship('Project', back_populates='goal')
    status = Column(Integer, nullable=False, server_default=str(Status.NEW.value))
    title = Column(String(256), nullable=False)
    week = Column(Integer)
    year = Column(Integer)

    def __repr__(self) -> str:
        return f'Goal: {self.title}'
