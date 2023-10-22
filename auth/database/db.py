from typing import Annotated

from fastapi import Depends
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import (
    # AsyncAttrs,
    AsyncSession,
    # async_sessionmaker,
    create_async_engine,
)
# from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

if settings.debug:
    async_engine = create_async_engine(
        "sqlite+aiosqlite:///./test.db",
        echo=settings.db_echo,
        future=True,
        connect_args={"check_same_thread": False},
    )

else:
    async_engine = create_async_engine(
        settings.database_url.__str__(),
        echo=settings.db_echo,
        future=True,
    )


async def db_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


# class Base(AsyncAttrs, DeclarativeBase):
#     def as_dict(self):
#         data_dict = {
#             c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs
#         }
#         return data_dict


AnSession = Annotated[AsyncSession, Depends(db_session)]

# * Anytime we call the AnSession, it creates the AsyncSession with async_sessionmaker
