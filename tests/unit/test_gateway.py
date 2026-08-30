import pytest
from fastapi import status

def test_gateway_health(client):
    """Test gateway health check"""
    response = client.get("/api/v1/gateway/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "operational"

def test_gateway_request_without_api_key(client):
    """Test gateway request without API key"""
    response = client.post(
        "/api/v1/gateway/request",
        json={
            "api_key": "invalid_key",
            "endpoint": "/api/chat",
            "method": "POST",
            "data": {"message": "hello"}
        }
    )
    
    assert response.status_code in [400, 401]

def test_gateway_request_with_pii(client):
    """Test gateway request with PII"""
    response = client.post(
        "/api/v1/gateway/request",
        json={
            "api_key": "valid_key",
            "endpoint": "/api/chat",
            "method": "POST",
            "data": {"message": "My email is test@example.com"}
        }
    )
    
    # Should be blocked due to PII
    assert response.status_code in [400, 403]