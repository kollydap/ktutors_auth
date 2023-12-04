from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
from auth.models.auth_models import TokenType
from sqlalchemy import Column, Integer, String, Enum, JSON, Boolean
import sqlalchemy


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
database = databases.Database(SQLALCHEMY_DATABASE_URL)


metadata = sqlalchemy.MetaData()

User = sqlalchemy.Table(
    "user",
    metadata,
    Column(
        "user_uid", String, primary_key=True, unique=True, nullable=False, index=True
    ),
    Column("email", String, unique=True, index=True),
    Column("password", String),
    Column("permission", JSON, nullable=True, default={}),
    Column("is_verified", Boolean, default=False),
)


engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
