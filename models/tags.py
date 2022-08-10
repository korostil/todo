from sqlalchemy import Column, Integer, String

from app.database import BaseDBModel

__all__ = ('Tag',)


class Tag(BaseDBModel):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)

    title = Column(String(32), nullable=False)

    def __repr__(self) -> str:
        return f'Tag: {self.title}'
