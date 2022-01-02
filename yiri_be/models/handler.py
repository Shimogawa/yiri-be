from yiri_be.database import YiriBEModelBase
from sqlalchemy import Column, Integer, String, Text

__all__ = ["Handler"]


class Handler(YiriBEModelBase):
    __tablename__ = "handlers"

    name = Column(String(50), nullable=False, unique=True)
    type = Column(String(30), nullable=False)
    script = Column(Text, nullable=False)
    priority = Column(Integer, nullable=False, default=0)
