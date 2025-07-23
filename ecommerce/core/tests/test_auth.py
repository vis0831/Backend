import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_signup():
    client = APIClient()
    response = client.post('/api/signup/', {
        "email": "test@example.com",
        "name": "Test User",
        "password": "strongpassword123"
    })
    assert response.status_code == 201
    assert User.objects.count() == 1