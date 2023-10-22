from fastapi import Header, Request, Depends
import logging

LOGGER = logging.getLogger(__file__)

def get_refresh_token(request: Request):
    session_cookie = request.cookies.get("session-1")
    if not session_cookie:
        LOGGER.error(f"session-1 token is missing for request")
        # raise MpApiError(AuthErrorEnum.AUTH_006)
    return session_cookie