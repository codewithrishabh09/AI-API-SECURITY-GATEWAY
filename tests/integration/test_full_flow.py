import pytest
from fastapi import status

def test_full_user_flow(client, db):
    """Test complete user registration and login flow"""
    
    # 1. Register user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "fullflowuser",
            "email": "fullflow@example.com",
            "password": "SecurePass123!",
            "full_name": "Full Flow User"
        }
    )
    assert register_response.status_code == status.HTTP_201_CREATED
    
    # 2. Login user
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "fullflow@example.com",
            "password": "SecurePass123!"
        }
    )
    assert login_response.status_code == status.HTTP_200_OK
    tokens = login_response.json()
    access_token = tokens["access_token"]
    
    # 3. Create project
    headers = {"Authorization": f"Bearer {access_token}"}
    project_response = client.post(
        "/api/v1/projects",
        json={
            "name": "Test Project",
            "description": "A test project"
        },
        headers=headers
    )
    assert project_response.status_code == status.HTTP_201_CREATED
    project_id = project_response.json()["id"]
    
    # 4. Create API key
    api_key_response = client.post(
        f"/api/v1/api-keys/{project_id}/keys",
        json={
            "name": "Test Key",
            "description": "A test API key"
        },
        headers=headers
    )
    assert api_key_response.status_code == status.HTTP_201_CREATED
    
    # 5. List projects
    list_response = client.get("/api/v1/projects", headers=headers)
    assert list_response.status_code == status.HTTP_200_OK
    assert len(list_response.json()) >= 1

def test_full_security_flow(client, db):
    """Test security detection flow"""
    
    # Attempt request with PII
    pii_response = client.post(
        "/api/v1/gateway/request",
        json={
            "api_key": "test_key",
            "endpoint": "/api/chat",
            "method": "POST",
            "data": {"message": "john.doe@example.com"}
        }
    )
    
    # Should be blocked
    assert pii_response.status_code in [400, 403]