import random
import bcrypt
import jwt
# from auth.settings import Settings
from app.core.config import Settings
from uuid import UUID
import datetime
from datetime import timezone


AUTH_PRIVATE_KEY = None
AUTH_PUBLIC_KEY = None
AUTH_ALGO = "RS256"
ACCESS_TOKEN_VALIDITY_SECONDS = 24 * 60 * 60  # 24 hours
REFRESH_TOKEN_VALIDITY_SECONDS = 7 * 24 * 60 * 60  # 7 days
EMAIL_TOKEN_EXPIRE_IN_SECONDS = 10 * 60  # seconds


def generate_random_6_digit_number():
    return random.randrange(100000, 1000000)


def encrypt_password(password: str):
    password = password.encode("utf-8")
    binary_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return binary_password.decode("utf-8")


def is_password_same_as_encrypted(unencrypted_password: str, encrypted_password: str):
    if not isinstance(encrypted_password, str):
        return False
    unencrypted_password = unencrypted_password.encode("utf-8")
    encrypted_password = encrypted_password.encode("utf-8")
    return bcrypt.checkpw(unencrypted_password, encrypted_password)


def encode_jwt_data(data: dict):
    global AUTH_PRIVATE_KEY
    if not AUTH_PRIVATE_KEY:
        auth_settings = Settings()
        AUTH_PRIVATE_KEY = auth_settings.auth_private_key
    return jwt.encode(payload=data, key=AUTH_PRIVATE_KEY, algorithm=AUTH_ALGO)


def decode_jwt_data(encoded: str):
    global AUTH_PUBLIC_KEY
    if not AUTH_PUBLIC_KEY:
        auth_settings = Settings()
        AUTH_PUBLIC_KEY = auth_settings.auth_public_key
    return jwt.decode(jwt=encoded, key=AUTH_PUBLIC_KEY, algorithms=[AUTH_ALGO])

# change to uuid
def generate_access_token(user_uid:int):
    return encode_jwt_data(data={"user_uid": user_uid})


def generate_refresh_token(user_uid: UUID):
    time_diff = datetime.timedelta(seconds=REFRESH_TOKEN_VALIDITY_SECONDS)
    data = {
        "exp": datetime.datetime.now(tz=timezone.utc) + time_diff,
        "iat": datetime.datetime.now(tz=timezone.utc),
        "jwt_custom_claim": {"user_uid": str(user_uid)},
    }
    return encode_jwt_data(data=data)


def get_refresh_token_data(refresh_token: str):
    decoded_refresh_token = decode_jwt_data(encoded=refresh_token)
    return decoded_refresh_token["jwt_custom_claim"]


def get_access_token_data(access_token: str):
    decoded_access_token = decode_jwt_data(encoded=access_token)
    return decoded_access_token
