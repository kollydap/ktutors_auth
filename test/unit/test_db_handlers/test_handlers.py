# import pytest
# from fastapi.testclient import TestClient
# from your_app import app  # Import your FastAPI app
# from your_database_module import create_user_table  # Import your database setup functions
# from auth.database.db_handlers import get_user_by_email  # Import your function for retrieving a user

# # Set up a test database and client
# @pytest.fixture(scope="module")
# def test_app():
#     # Use an in-memory SQLite database for testing
#     database_url = "sqlite:///./test_db.sqlite"
#     create_user_table(database_url)  # Create user table in the test database
#     app.database_url = database_url
#     client = TestClient(app)
#     return client

# # Define a test case
# def test_get_user_by_email(test_app):
#     # Insert a test user into the database
#     test_user = {"email": "test@example.com", "password": "password123"}
#     # Your code for inserting the test user goes here

#     # Retrieve the test user by email using your function
#     retrieved_user = get_user_by_email(test_user["email"])

#     # Assert that the retrieved user matches the expected user
#     assert retrieved_user is not None
#     assert retrieved_user["email"] == test_user["email"]
#     # Add more assertions based on your user data and schema

# # You can add more test cases for different scenarios as needed


# test_auth.py

import pytest
from fastapi.testclient import TestClient
from main import app  # Replace with the actual import path to your FastAPI app
from auth.database.db_models.auth_orm import (
    User as UserDb,
)
from app.core.application import get_app

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_get_user_by_email( database):
    test_client = TestClient(app=get_app())
    # Assuming you have a test user inserted into your test database
    test_email = "test@example.com"

    # Insert a test user into the database (you may need to adjust this based on your model)
    await database.execute(UserDb.insert().values(email=test_email))

    # Call the API endpoint to get the user by email
    response = await test_client.get(f"/get_user_by_email?email={test_email}")

    assert response.status_code == 200  # Check if the response status code is 200
    user = response.json()
    assert user["email"] == test_email  # Check if the returned user matches the test email

# You can run this test using pytest
