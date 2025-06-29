import pytest
from ninja.testing import TestClient
from django.test import Client
from apps.accounts.models import CustomUser

@pytest.fixture
def api_client():
    from settings.urls import api
    return TestClient(api)

@pytest.fixture
def django_client():
    return Client()

@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def admin_user():
    return CustomUser.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123'
    ) 