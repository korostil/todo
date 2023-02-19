from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
    func,
)
from sqlalchemy.orm import relationship

from app.database import BaseDBModel

__all__ = ('Task',)


class Task(BaseDBModel):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    completed_at = Column(DateTime)
    decisive = Column(Boolean, nullable=False)
    description = Column(String(256))
    due_date = Column(Date)
    due_time = Column(Time)
    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship('Project', back_populates='tasks')
    space = Column(Integer, nullable=False)
    title = Column(String(256), nullable=False)

    def __repr__(self) -> str:
        return f'Task: {self.title}'
