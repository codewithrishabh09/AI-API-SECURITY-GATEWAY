import pytest
from fastapi import status
from app.core.security import hash_password, verify_password, create_access_token, verify_token

def test_password_hashing():
    """Test password hashing"""
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_token_creation_and_verification():
    """Test JWT token creation and verification"""
    data = {"sub": "user123"}
    token = create_access_token(data)
    
    assert token is not None
    payload = verify_token(token)
    assert payload["sub"] == "user123"

def test_invalid_token():
    """Test invalid token"""
    invalid_token = "invalid.token.here"
    
    with pytest.raises(Exception):
        verify_token(invalid_token)

def test_register_user(client, db):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_duplicate_email(client, db):
    """Test duplicate email registration"""
    user_data = {
        "username": "testuser1",
        "email": "duplicate@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    
    response1 = client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == status.HTTP_201_CREATED
    
    user_data["username"] = "testuser2"
    response2 = client.post("/api/v1/auth/register", json=user_data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST

def test_login(client, db):
    """Test user login"""
    # First register a user
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123",
            "full_name": "Login User"
        }
    )
    
    # Then try to login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"