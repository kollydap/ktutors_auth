from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from uuid import UUID
from typing import Optional
from redis_om import JsonModel, Field,HashModel,get_redis_connection,Migrator
from abc import ABC

class Password(BaseModel):
    password: constr(
        # regex="^(?=.*[A-Z])(?=.*[!@#$&*_+%-=])(?=.*[0-9])(?=.*[a-z]).{8,}$"
    )


class PasswordChange(Password):
    old_password: str


class _UserPassword(BaseModel):
    user_uid: UUID
    email: EmailStr
    password: Optional[str]
    permissions: dict


class TokenVerification(BaseModel):
    email: EmailStr
    token: constr(min_length=6, max_length=6)
    # password: Optional[constr(regex="^(?=.*[A-Z])(?=.*[!@#$&*_+%-=])(?=.*[0-9])(?=.*[a-z]).{8,}$")]
    password: Optional[constr()]


class TokenProfile(BaseModel):
    message: str
    validity: int


class UserSignUp(BaseModel):
    first_name: str
    last_name: str
    email: str = Field(index=True, primary_key=True)
    phone_number: str

    class Config:
        extra = "ignore"


class Login(BaseModel):
    email: EmailStr
    password: str


class AuthenticatedUserProfile(BaseModel):
    access_token: constr(min_length=1)


class UserProfile(BaseModel):
    user_uid: UUID
    email: EmailStr
    # user_type: UserType
    is_verified: bool
    # permissions: dict

class UserStore(HashModel):
    first_name: str
    last_name: str
    email: str = Field(index=True, primary_key=True)
    phone_number: str

    class Config:
        extra = "ignore"


class TokenType(str, Enum):
    USER_SIGN_UP = "USER_SIGN_UP"
    # EMPLOYEE_SIGN_UP = "EMPLOYEE_SIGN_UP"
    FORGOT_PASSWORD = "FORGOT_PASSWORD"
    EMAIL_CHANGE = "EMAIL_CHANGE"




# class TokenStore(BaseModel):
#     email: str
#     token: str
#     token_type: TokenType
#     # user_uid: Optional[UUID]
#     user_uid: Optional[int]

#     class Config:
#         extra = "ignore"



# *------------redis-------------------------

class TokenStore(HashModel):
    # todo change email to EmailStr
    email: str = Field(index=True, primary_key=True)
    token: str
    token_type: TokenType


    class Config:
        extra = "ignore"

class UserAccessStore(HashModel):
    # todo : change user_uid to UUID
    user_uid: int= Field(index=True, primary_key=True)
    # permissions: dict
    access_token: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        extra = "allow"


class UserRefreshStore(HashModel):
    # todo change to uuid
    user_uid: int = Field(index=True, primary_key=True)
    refresh_token: str = Field(index=True)

    class Config:
        extra ="ignore"
