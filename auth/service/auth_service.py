from auth.models.auth_models import (
    UserSignUp,
    TokenProfile,
    UserProfile,
    UserAccessStore,
    UserRefreshStore,
    Login,
    TokenType,
    TokenStore,
    TokenVerification,
    UserStore,
)
import auth.database.db_handlers.auth_db_handler as auth_db_handlers
import logging
from auth.service.service_exceptions import NotFound, DuplicateError
from auth.service.service_errors import AuthErrorEnum
import auth.service.service_utils as service_utils
from fastapi.responses import JSONResponse
from uuid import UUID
from jwt.exceptions import InvalidTokenError
import json
from sqlalchemy.orm import Session
from errors.k_api_error import KApiError
import pika

LOGGER = logging.getLogger(__file__)

# todo :Work on converting email to lowercase before saving to db
# * /changes are made to the db during token verification


async def _complete_login(user_uid: UUID, permissions: dict):
    access_token = service_utils.generate_access_token(user_uid=user_uid)
    response = JSONResponse(content={"access_token": access_token})
    refresh_token = service_utils.generate_refresh_token(user_uid=user_uid)
    response.set_cookie(
        key="session-1",
        value=refresh_token,
        max_age=service_utils.REFRESH_TOKEN_VALIDITY_SECONDS,
        secure=True,
        httponly=True,
        samesite="strict",
    )
    user_access_store = UserAccessStore(user_uid=user_uid, access_token=access_token)
    user_access_store.save()
    user_access_store.expire(service_utils.ACCESS_TOKEN_VALIDITY_SECONDS)
    user_refresh_store = UserRefreshStore(
        user_uid=user_uid, refresh_token=refresh_token
    )
    user_refresh_store.save()
    user_refresh_store.expire(service_utils.REFRESH_TOKEN_VALIDITY_SECONDS)
    return response


async def _email_login(login: Login, **kwargs):
    try:
        user_password = await auth_db_handlers.get_user_password_by_email(
            email=login.email,
        )
    except NotFound as e:
        LOGGER.exception(e)
        raise Exception
    if not service_utils.is_password_same_as_encrypted(
        encrypted_password=user_password.password, unencrypted_password=login.password
    ):
        LOGGER.info(
            f"user with email{user_password.user_uid} attempted with wrong password"
        )
        raise Exception

    return await _complete_login(user_uid=user_password.user_uid, permissions={})


async def login_user(login: Login, **kwargs):
    return await _email_login(login=login)


async def _save_token_and_send_email(
    email: str,
    token_type: TokenType,
    routing_action: str,
    # todo user_uid: UUID = None,
    user_uid: int = None,
    **kwargs,
):
    token = service_utils.generate_random_6_digit_number()
    print(token)
    token_store = TokenStore(
        # todo change back to uuid by removing int
        email=email,
        token=token,
        token_type=token_type,
    )
    token_store.save()
    token_store.expire(num_seconds=service_utils.EMAIL_TOKEN_EXPIRE_IN_SECONDS)

    # message_dict = {"email": email, "token": token}

    # email_payload = BaseRabbitMqMessage(
    #     message=message_dict, routing_action=routing_action
    # )
    # await MpRabbitMq.publish_message(
    #     exchange_name="gns", routing_key="auth_to_gns", message=email_payload
    # )


async def user_signup(user_signup: UserSignUp, **kwargs):
    print(user_signup.email)
    user_store = UserStore(**user_signup.dict())
    user_store.save()
    user_store.expire(num_seconds=500)
    await _save_token_and_send_email(
        email=user_signup.email,
        token_type=TokenType.USER_SIGN_UP,
        routing_action="user_signup",
    )

    return TokenProfile(
        message=f"email with token sent to {user_signup.email}",
        validity=service_utils.ACCESS_TOKEN_VALIDITY_SECONDS,
    )


async def token_verification(token_verification: TokenVerification, **kwargs):
    token_store = TokenStore.get(token_verification.email)
    print(token_store)
    if not token_store:
        raise KApiError(AuthErrorEnum.AUTH_003)

    if token_store.token != token_verification.token:
        raise KApiError(AuthErrorEnum.AUTH_003)

    if token_store.token_type == TokenType.USER_SIGN_UP:
        encrypted_password = service_utils.encrypt_password(
            password=token_verification.password
        )
        user_profile = await auth_db_handlers.create_user(
            email=token_verification.email, password=encrypted_password, **kwargs
        )
        user_store = UserStore.get(token_verification.email)
        user_store = user_store.dict()
        user_store["auth_user_uid"] = user_profile.user_uid
        user_data = json.dumps(user_store)
        _send_user_data_to_pms(user_data)

    elif token_store.token_type == TokenType.FORGOT_PASSWORD:
        user_profile = await auth_db_handlers.get_user_by_email(
            email=token_verification.email, **kwargs
        )

    elif token_store.token_type == TokenType.EMAIL_CHANGE:
        try:
            user_profile = await auth_db_handlers.update_user_email(
                x_user_uid=token_store.user_uid,
                new_email=token_verification.email,
                **kwargs,
            )
        except DuplicateError as e:
            LOGGER.exception(e)
            raise KApiError(AuthErrorEnum.AUTH_012)
            print(user_profile)
    return await _complete_login(
        # todo change user permission
        user_uid=user_profile.user_uid,
        permissions={},
    )


def _send_user_data_to_pms(user_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="auth_to_pms")
    channel.basic_publish(exchange="", routing_key="auth_to_pms", body=user_data)
    print(" [x] Sent  data to pms")
    connection.close()


async def logout(**kwargs):
    ...


async def refresh(**kwargs):
    ...


async def forgot_password(**kwargs):
    ...


async def change_password(**kwargs):
    ...
