import enum
from fastapi import status


class AuthErrorEnum(enum.Enum):
    AUTH_001 = ("Invalid Login Credentials", status.HTTP_400_BAD_REQUEST)
    AUTH_002 = ("Invalid request parameters", status.HTTP_422_UNPROCESSABLE_ENTITY)
    AUTH_003 = ("The token is invalid", status.HTTP_400_BAD_REQUEST)
    AUTH_004 = ("Session token is invalid", status.HTTP_401_UNAUTHORIZED)
    AUTH_005 = ("Access token is invalid", status.HTTP_401_UNAUTHORIZED)
    AUTH_006 = ("Invalid or malformed token", status.HTTP_401_UNAUTHORIZED)
    AUTH_007 = ("User not found", status.HTTP_404_NOT_FOUND)
    AUTH_008 = ("Invalid user action", status.HTTP_403_FORBIDDEN)
    AUTH_009 = ("Further account action needed", status.HTTP_403_FORBIDDEN)
    AUTH_010 = ("Invalid Registration Data", status.HTTP_400_BAD_REQUEST)
    AUTH_011 = ("User is not authorized", status.HTTP_403_FORBIDDEN)
    AUTH_012 = ("Email in use", status.HTTP_400_BAD_REQUEST)
    AUTH_013 = ("User is not authorized", status.HTTP_403_FORBIDDEN)