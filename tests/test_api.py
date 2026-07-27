from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test that the health endpoint returns OK with correct response"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test that root endpoint exists and returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]