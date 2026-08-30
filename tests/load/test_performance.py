import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi import status

def test_concurrent_requests(client):
    """Test concurrent request handling"""
    
    def make_request():
        response = client.get("/api/v1/gateway/health")
        return response.status_code
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [f.result() for f in futures]
    
    # All requests should succeed
    assert all(status_code == 200 for status_code in results)

def test_response_time(client):
    """Test response time"""
    start = time.time()
    
    for _ in range(100):
        response = client.get("/api/v1/gateway/health")
        assert response.status_code == 200
    
    end = time.time()
    total_time = end - start
    avg_time = total_time / 100
    
    # Average response time should be less than 100ms
    assert avg_time < 0.1