import sqlalchemy.exc
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine


Base = declarative_base()

DB_SYS = "postgresql"
DRIVER = "asyncpg" 


class DBEngineProvider:
    """DataBase Engine provider"""
    def __init__(self, db_user, db_pwd, db_host, db_port, db_name):
        db_url = f"{DB_SYS}+{DRIVER}://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
        self._engine = create_async_engine(db_url, echo=True)

    @property
    def engine(self):
        return self._engine


class ORGDatabase:
    """DataBase Session"""
    def __init__(self, engine_provider: DBEngineProvider):
        self._engine: DBEngineProvider = engine_provider.engine
        self._async_session_factory = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    def new_session(self) -> AsyncSession:
        return self._async_session_factory()
