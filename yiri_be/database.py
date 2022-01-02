from datetime import datetime
from typing import Any, Callable, List, Type, TypeVar
from sqlalchemy import create_engine, Column, DateTime, BigInteger
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

__all__ = ["YiriBEModelBase", "engine", "session", "init_db", "dbcommit"]

Base: Any = declarative_base()

engine: Engine = None
session: scoped_session = None


class YiriBEModelBase(Base):
    __abstract__ = True

    session: scoped_session
    query: Query

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def save(self):
        self.session.commit()

    def insert(self):
        self.session.add(self)

    def __getattribute__(self, __name: str) -> Any:
        try:
            return object.__getattribute__(self, __name)
        except AttributeError:
            pass
        v = getattr(self.query, __name, None)
        if v is not None:
            return v
        raise AttributeError(__name)

    @classmethod
    def commit(cls):
        cls.session.commit()

    # @classmethod
    # def query(cls):
    #     return cls.session.query(cls)


def init_db(connection: str):
    global engine, session
    engine = create_engine(connection)
    session = scoped_session(sessionmaker(engine))
    YiriBEModelBase.query = session.query_property()
    YiriBEModelBase.session = session


def dbcommit(func: Callable) -> Callable:
    def do_and_commit(*args, **kwargs):
        func(*args, **kwargs)
        session.commit()

    return do_and_commit
