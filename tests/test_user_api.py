import json
import pytest
from main.models import User


class TestUserAPI:

    # 1. List users returns 200
    def test_list_users_returns_200(self, admin_client):
        res = admin_client.get('/api/users')
        assert res.status_code == 200

    # 2. Create user with valid data
    def test_create_user_valid(self, admin_client):
        payload = {
            'name': 'Test User',
            'email': 'testuser@mail.com',
            'login_email': 'testuser@mail.com',
            'password': 'pass1234',
            'role': 'employee',
        }
        res = admin_client.post('/api/users', json.dumps(payload), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['name'] == 'Test User'

    # 3. Create user with duplicate login_email returns 400
    def test_create_user_duplicate_login_email(self, admin_client, employee_user):
        payload = {
            'name': 'Dup User',
            'email': 'other@mail.com',
            'login_email': employee_user.login_email,
            'password': 'pass1234',
            'role': 'employee',
        }
        res = admin_client.post('/api/users', json.dumps(payload), content_type='application/json')
        assert res.status_code == 400

    # 4. Create user with duplicate email returns 400
    def test_create_user_duplicate_email(self, admin_client, employee_user):
        payload = {
            'name': 'Dup Email',
            'email': employee_user.email,
            'login_email': 'uniquelogin@mail.com',
            'password': 'pass1234',
            'role': 'employee',
        }
        res = admin_client.post('/api/users', json.dumps(payload), content_type='application/json')
        assert res.status_code == 400

    # 5. Get user by id returns 200
    def test_get_user_by_id(self, admin_client, employee_user):
        res = admin_client.get(f'/api/users/{employee_user.id}')
        assert res.status_code == 200
        assert res.json()['id'] == employee_user.id

    # 6. Update user returns 200 and updated name
    def test_update_user(self, admin_client, employee_user):
        payload = {
            'name': 'Updated Name',
            'email': employee_user.email,
            'login_email': employee_user.login_email,
            'role': 'employee',
        }
        res = admin_client.put(f'/api/users/{employee_user.id}', json.dumps(payload), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['name'] == 'Updated Name'

    # 7. Delete user returns success
    def test_delete_user(self, admin_client, db):
        user = User.objects.create_user(
            email='todelete@mail.com', login_email='todelete@mail.com',
            password='pass', name='Del User', role='employee'
        )
        res = admin_client.delete(f'/api/users/{user.id}')
        assert res.status_code == 200
        assert res.json()['success'] is True

    # 8. Login with valid credentials returns success
    def test_login_valid_credentials(self, client, admin_user):
        payload = {'login_email': 'admin@test.com', 'password': 'testpass123'}
        res = client.post('/api/auth/login', json.dumps(payload), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['success'] is True

    # 9. Login with invalid credentials returns failure
    def test_login_invalid_credentials(self, client):
        payload = {'login_email': 'wrong@mail.com', 'password': 'wrongpass'}
        res = client.post('/api/auth/login', json.dumps(payload), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['success'] is False

    # 10. Auth me returns current user info
    def test_auth_me_returns_user(self, admin_client, admin_user):
        res = admin_client.get('/api/auth/me')
        assert res.status_code == 200
        assert res.json()['email'] == admin_user.email
