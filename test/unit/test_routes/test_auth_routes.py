from fastapi.testclient import TestClient
from uuid import uuid4
from app.core.application import get_app

from faker import Faker
from unittest.mock import patch, AsyncMock
from auth.models.auth_models import Login, UserSignUp, PasswordChange, TokenVerification
from fastapi.responses import JSONResponse

FAKE = Faker("en_US")


@patch("auth.routers.auth_routes.auth_service", new_callable=AsyncMock)
async def test_login_user_happy_path(mock_auth_service):
    route_test_client = TestClient(app=get_app())

    mock_response_dict = {"access_token": "don't sleep dapo"}

    # later on we wil return the response from service as a json response
    mock_auth_service.login_user.return_value = mock_response_dict
    login_json = {"email": "dapkolly@gmail.com", "password": "@Bad002"}
    response = route_test_client.post("api/v1/accounts/login", json=login_json)
    login = Login(**login_json)
    assert response.status_code == 200
    mock_auth_service.login_user.assert_awaited_once_with(login=login)
    assert response.json() == mock_response_dict


@patch("auth.routers.auth_routes.auth_service", new_callable=AsyncMock)
async def test_create_user_happy_path(mock_auth_service):
    route_test_client = TestClient(app=get_app())
    mock_response_dict = {
        "message": "Kolawole",
        "validity": 10,
    }
    mock_auth_service.create_user.return_value = mock_response_dict
    signup_json = {
        "first_name": "Kolawole",
        "last_name": "Joseph",
        "email": "dapkolly@gmail.com",
    }
    response = route_test_client.post("api/v1/accounts/signup", json=signup_json)
    user_signup = UserSignUp(**signup_json)
    assert response.status_code == 200
    mock_auth_service.create_user.assert_awaited_once_with(user_signup=user_signup)
    assert response.json() == mock_response_dict


@patch("auth.routers.auth_routes.auth_service", new_callable=AsyncMock)
async def test_forgot_password_happy_path(mock_auth_service):
    route_test_client = TestClient(app=get_app())
    mock_response_dict = {
        "message": "Kolawole",
        "validity": 10,
    }
    mock_auth_service.forgot_password.return_value = mock_response_dict
    email = {"email": "dapkolly@gmail.com"}
    response = route_test_client.post("api/v1/accounts/forgot/password", json=email)
    assert response.status_code == 200
    mock_auth_service.forgot_password.assert_awaited_once_with(
        email="dapkolly@gmail.com"
    )
    assert response.json() == mock_response_dict


@patch("auth.routers.auth_routes.auth_service", new_callable=AsyncMock)
async def test_change_password_happy_path(mock_auth_service):
    route_test_client = TestClient(app=get_app())
    mock_auth_service.change_password.return_value = None

    password_change = {
        "old_password": "Kolawole",
        "password": "@Jaga10",
    }
    response = route_test_client.post(
        "api/v1/accounts/change/password", json=password_change
    )
    assert response.status_code == 200
    mock_auth_service.change_password.assert_awaited_once_with(
        password_change=PasswordChange(**password_change)
    )


@patch("auth.routers.auth_routes.auth_service", new_callable=AsyncMock)
async def test_token_verification_happy_path(mock_auth_service):
    route_test_client = TestClient(app=get_app())
    mock_auth_service.token_verification.return_value = None
    json_data = {"email": FAKE.email(), "token": "902920", "password": "@Jaja90"}
    response = route_test_client.post(
        "api/v1/accounts/token/verification", json=json_data
    )
    assert response.status_code == 200
    mock_auth_service.token_verification.assert_awaited_once_with(
        token_verification=TokenVerification(**json_data)
    )


@patch("auth.routers.auth_routes.auth_service", new_callable=AsyncMock)
async def test_logout_happy_path(mock_auth_service):
    route_test_client = TestClient(app=get_app())
    mock_auth_service.logout.return_value = None
    response = route_test_client.post(
        "api/v1/accounts/logout"
    )
    assert response.status_code == 200
    mock_auth_service.logout.assert_awaited_once(
    )


@patch("auth.routers.auth_routes.auth_service", new_callable=AsyncMock)
async def test_refresh_happy_path(mock_auth_service):
    route_test_client = TestClient(app=get_app())
    mock_response_dict = {"access_token": "don't sleep Dapo"}
    json_response = JSONResponse(content=mock_response_dict)
    json_response.set_cookie(key="session-1", value="just another session")
    mock_auth_service.refresh.return_value = json_response
    headers = {
        "x-callers-name": "unknown gun men",
        "x-user-uid": str(uuid4()),
        "x-request-uid": str(uuid4()),
        "Cookie": "session-1=dummy-cookie...",
    }
    response = route_test_client.get("api/v1/accounts/refresh", headers=headers)
    refresh_token = "dummy-cookie..."
    assert response.status_code == 200
    mock_auth_service.refresh.assert_awaited_once_with(refresh_token=refresh_token)
    assert response.json() == mock_response_dict

