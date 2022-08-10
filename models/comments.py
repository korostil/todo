from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import BaseDBModel

__all__ = ('Comment',)


class Comment(BaseDBModel):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    text = Column(String(1024), nullable=False)

    def __repr__(self) -> str:
        return f'Comment: {self.id}'
