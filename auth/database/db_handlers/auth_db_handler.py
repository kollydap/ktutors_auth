from uuid import UUID
from sqlalchemy import update, insert, select, delete, insert
from auth.database.db_models.auth_orm import User as UserDb, TokenStore as TokenDb
from auth.models.auth_models import UserProfile, _UserPassword, TokenType
import logging
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, OperationalError
from auth.database.db import AnSession
from datetime import datetime, timedelta
from app.core.config import settings
from fastapi import HTTPException, Security, status
from sqlalchemy.orm import Session
from auth.database.db_models.auth_orm import database
from auth.service.service_exceptions import NotFound, UpdateError

LOGGER = logging.getLogger(__file__)


async def create_user(email: str, password: str, **kwargs):
    query = UserDb.insert().values(email=email, password=password)
    try:
        await database.execute(query)
        new_user_query = UserDb.select().where(UserDb.c.email == email)
        new_user = await database.fetch_one(new_user_query)

        return new_user

    except IntegrityError as e:
        print(f"Error creating user: {e}")
        return False


async def save_token(email: str, token: str, token_type=TokenType, **kwargs):
    query = TokenDb.insert().values(email=email, token=token, token_type=token_type)
    try:
        return await database.execute(query)
    except Exception as e:
        print(f"Error Storing Token:{e}")
        return False


async def get_token(email: str):
    query = (
        TokenDb.select()
        .where(TokenDb.c.email == email)
        .order_by(desc(TokenDb.c.token_uid))
        .limit(1)
    )
    try:
        return await database.fetch_one(query)
    except OperationalError as e:
        print(e)
        return False


async def get_user_by_email(email: str):
    query = UserDb.select().where(UserDb.c.email == email)
    result = await database.fetch_one(query)
    if not result:
        raise NotFound
    return result


async def get_user_by_password(password: str):
    query = UserDb.select().where(UserDb.c.password == password)
    try:
        return await database.fetch_one(query)
    except Exception as e:
        print(f"Error fetching user by password: {e}")
        return None


async def update_password(email: str, password: str):
    query = (
        UserDb.update()
        .where(UserDb.c.email == email)
        .values(password=password)
    )
    result = await database.execute(query)
    if not result:
        raise UpdateError
    return result


async def get_user_password_by_email(email: str, **kwargs):
    query = UserDb.select().where(UserDb.c.email == email)
    result = await database.fetch_one(query)
    if not result:
        raise NotFound
    # return _UserPassword(**result.as_dict())
    return result
