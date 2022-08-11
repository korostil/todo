from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import BaseDBModel

__all__ = ('Goal',)


class Goal(BaseDBModel):
    __tablename__ = 'goal'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    month = Column(Integer)
    title = Column(String(256), nullable=False)
    week = Column(Integer)
    year = Column(Integer)

    def __repr__(self) -> str:
        return f'Goal: {self.title}'
