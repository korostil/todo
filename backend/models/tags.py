from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from app.database import BaseDBModel

__all__ = ('Tag',)


class Tag(BaseDBModel):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)

    color = Column(String(7))  # hexadecimal
    title = Column(String(32), nullable=False)

    def __repr__(self) -> str:
        return f'Tag: {self.title}'

    @validates('color')
    def validate_color(self, key: str, value: str) -> str:
        assert value.startswith('#') is True
        return value
