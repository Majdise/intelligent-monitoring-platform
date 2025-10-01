import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "endpoints" in data

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    # Check that some metrics are present
    assert b"http_requests_total" in response.content

def test_get_services():
    """Test get services endpoint"""
    response = client.get("/api/services")
    assert response.status_code == 200
    services = response.json()
    assert isinstance(services, list)
    assert len(services) > 0
    # Check service structure
    for service in services:
        assert "name" in service
        assert "status" in service
        assert "uptime" in service

def test_get_alerts():
    """Test get alerts endpoint"""
    response = client.get("/api/alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert isinstance(alerts, list)

def test_simulate_incident():
    """Test incident simulation"""
    response = client.post(
        "/api/simulate-incident",
        params={"service_name": "test-service"}
    )
    assert response.status_code == 200
    incident = response.json()
    assert incident["type"] == "incident"
    assert incident["service"] == "test-service"
    assert "timestamp" in incident

def test_cors_headers():
    """Test CORS headers are present"""
    response = client.options("/api/services")
    assert response.status_code == 200