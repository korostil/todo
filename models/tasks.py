from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import BaseDBModel


class Task(BaseDBModel):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    description = Column(String(256), nullable=False)
    due = Column(DateTime)
    space = Column(Integer, nullable=False)
    title = Column(String(256), nullable=False)

    def __repr__(self) -> str:
        return f'Task: {self.title}'
