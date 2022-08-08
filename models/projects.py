from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.database import BaseDBModel


class Project(BaseDBModel):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)

    archived = Column(Boolean(), default=False, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    description = Column(String(256), nullable=False)
    space = Column(Integer, nullable=False)
    title = Column(String(256), nullable=False)

    def __repr__(self) -> str:
        return f'Project: {self.title}'
