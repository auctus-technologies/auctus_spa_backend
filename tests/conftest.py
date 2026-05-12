import pytest
from django.test import Client
from main.models import User


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email='admin@test.com',
        login_email='admin@test.com',
        password='testpass123',
        name='Admin User',
        role='admin',
    )


@pytest.fixture
def employee_user(db):
    return User.objects.create_user(
        email='emp@test.com',
        login_email='emp@test.com',
        password='testpass123',
        name='Employee User',
        role='employee',
    )


@pytest.fixture
def admin_client(admin_user):
    c = Client()
    c.force_login(admin_user)
    return c


@pytest.fixture
def employee_client(employee_user):
    c = Client()
    c.force_login(employee_user)
    return c


@pytest.fixture
def anon_client():
    return Client()
