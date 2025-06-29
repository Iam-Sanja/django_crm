import pytest
from ninja.testing import TestClient
from apps.accounts.models import CustomUser

def test_register_user(api_client):
    response = api_client.post("/auth/register", json={
        "email": "new@example.com",
        "password": "testpass123",
        "first_name": "New",
        "last_name": "User"
    })
    
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"
    assert CustomUser.objects.filter(email="new@example.com").exists()

def test_login_user(api_client, user):
    response = api_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()

def test_get_user_info(api_client, user):
    # First login to get token
    login_response = api_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = login_response.json()["token"]
    
    # Use token to get user info
    response = api_client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com" 