from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import BaseDBModel

__all__ = ('Goal',)


class Goal(BaseDBModel):
    __tablename__ = 'goal'

    id = Column(Integer, primary_key=True)

    achieved_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    month = Column(Integer)
    projects = relationship('Project', back_populates='goal')
    title = Column(String(256), nullable=False)
    year = Column(Integer)

    def __repr__(self) -> str:
        return f'Goal: {self.title}'
