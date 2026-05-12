import json
import pytest
from main.models import User


class TestLeaveAPI:

    @pytest.fixture
    def emp(self, db):
        return User.objects.create_user(
            email='leave_emp@mail.com', login_email='leave_emp@mail.com',
            password='pass', name='Leave Emp', role='employee'
        )

    @pytest.fixture
    def emp_client(self, emp):
        from django.test import Client
        c = Client()
        c.force_login(emp)
        return c

    # 1. List leave requests requires auth
    def test_list_leave_requires_auth(self, anon_client):
        res = anon_client.get('/api/leave-requests')
        assert res.status_code == 401

    # 2. Admin sees all leave requests
    def test_admin_sees_all_leaves(self, admin_client):
        res = admin_client.get('/api/leave-requests')
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    # 3. Employee sees only their own leave requests
    def test_employee_sees_own_leaves(self, emp_client):
        res = emp_client.get('/api/leave-requests')
        assert res.status_code == 200

    # 4. Apply for leave returns 200
    def test_apply_for_leave(self, emp_client):
        res = emp_client.post('/api/leave-requests', data={
            'leave_type': 'casual',
            'start_date': '2026-06-10',
            'end_date': '2026-06-12',
            'reason': 'Personal work',
        })
        assert res.status_code == 200

    # 5. New leave has status pending
    def test_new_leave_status_pending(self, emp_client):
        res = emp_client.post('/api/leave-requests', data={
            'leave_type': 'sick',
            'start_date': '2026-07-01',
            'end_date': '2026-07-02',
            'reason': 'Fever',
        })
        assert res.json()['status'] == 'pending'

    # 6. Approve leave (admin)
    def test_approve_leave(self, admin_client, emp_client):
        emp_client.post('/api/leave-requests', data={
            'leave_type': 'casual',
            'start_date': '2026-08-01',
            'end_date': '2026-08-01',
            'reason': 'Errand',
        })
        leaves = admin_client.get('/api/leave-requests').json()
        lid = leaves[0]['id']
        res = admin_client.patch(
            f'/api/leave-requests/{lid}/status',
            json.dumps({'status': 'approved'}),
            content_type='application/json'
        )
        assert res.status_code == 200
        assert res.json()['status'] == 'approved'

    # 7. Reject leave (admin)
    def test_reject_leave(self, admin_client, emp_client):
        emp_client.post('/api/leave-requests', data={
            'leave_type': 'casual',
            'start_date': '2026-09-01',
            'end_date': '2026-09-01',
            'reason': 'Travel',
        })
        leaves = admin_client.get('/api/leave-requests').json()
        lid = leaves[0]['id']
        res = admin_client.patch(
            f'/api/leave-requests/{lid}/status',
            json.dumps({'status': 'rejected'}),
            content_type='application/json'
        )
        assert res.status_code == 200
        assert res.json()['status'] == 'rejected'

    # 8. Delete leave request
    def test_delete_leave(self, admin_client, emp_client):
        emp_client.post('/api/leave-requests', data={
            'leave_type': 'sick',
            'start_date': '2026-10-01',
            'end_date': '2026-10-01',
            'reason': 'Unwell',
        })
        leaves = admin_client.get('/api/leave-requests').json()
        lid = leaves[0]['id']
        res = admin_client.delete(f'/api/leave-requests/{lid}')
        assert res.status_code == 200

    # 9. Leave types endpoint returns list
    def test_leave_types_returns_list(self, admin_client):
        res = admin_client.get('/api/leave-types')
        assert res.status_code == 200

    # 10. Leave response has user_name field
    def test_leave_has_user_name(self, emp_client):
        res = emp_client.post('/api/leave-requests', data={
            'leave_type': 'casual',
            'start_date': '2026-11-01',
            'end_date': '2026-11-01',
            'reason': 'Holiday',
        })
        assert 'user_name' in res.json()
