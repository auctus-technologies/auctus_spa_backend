import json
import pytest
from main.models import User


class TestTaskAPI:

    def _task_payload(self, title='Test Task'):
        return {
            'title': title,
            'priority': 'medium',
            'due_date': '2026-12-31',
            'assigned_user_ids': [],
        }

    # 1. List tasks requires authentication
    def test_list_tasks_requires_auth(self, anon_client):
        res = anon_client.get('/api/tasks')
        assert res.status_code == 401

    # 2. Admin can list all tasks
    def test_admin_list_tasks(self, admin_client):
        res = admin_client.get('/api/tasks')
        assert res.status_code == 200

    # 3. List tasks has pagination fields
    def test_list_tasks_has_pagination(self, admin_client):
        res = admin_client.get('/api/tasks')
        for key in ['tasks', 'total', 'page', 'total_pages']:
            assert key in res.json()

    # 4. Create task (admin only) returns 200
    def test_create_task_admin(self, admin_client):
        res = admin_client.post('/api/tasks', json.dumps(self._task_payload()), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['title'] == 'Test Task'

    # 5. Employee cannot create task (403)
    def test_create_task_employee_forbidden(self, employee_client):
        res = employee_client.post('/api/tasks', json.dumps(self._task_payload()), content_type='application/json')
        assert res.status_code == 403

    # 6. Get task by id (via list) returns correct task
    def test_created_task_appears_in_list(self, admin_client):
        admin_client.post('/api/tasks', json.dumps(self._task_payload('Unique Task XYZ')), content_type='application/json')
        res = admin_client.get('/api/tasks?search=Unique+Task+XYZ')
        assert res.json()['total'] >= 1

    # 7. Update task (admin only) returns 200
    def test_update_task_admin(self, admin_client):
        create_res = admin_client.post('/api/tasks', json.dumps(self._task_payload('Update Me')), content_type='application/json')
        tid = create_res.json()['id']
        update = {'title': 'Updated Task', 'priority': 'high', 'due_date': '2026-11-30', 'assigned_user_ids': []}
        res = admin_client.put(f'/api/tasks/{tid}', json.dumps(update), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['title'] == 'Updated Task'

    # 8. Update task status returns 200
    def test_update_task_status(self, admin_client):
        create_res = admin_client.post('/api/tasks', json.dumps(self._task_payload('Status Task')), content_type='application/json')
        tid = create_res.json()['id']
        res = admin_client.patch(f'/api/tasks/{tid}/status', json.dumps({'status': 'review'}), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['status'] == 'review'

    # 9. Update status with invalid value returns 400
    def test_update_task_status_invalid(self, admin_client):
        create_res = admin_client.post('/api/tasks', json.dumps(self._task_payload('Bad Status Task')), content_type='application/json')
        tid = create_res.json()['id']
        res = admin_client.patch(f'/api/tasks/{tid}/status', json.dumps({'status': 'invalid_status'}), content_type='application/json')
        assert res.status_code == 400

    # 10. Delete task (admin only) returns success
    def test_delete_task_admin(self, admin_client):
        create_res = admin_client.post('/api/tasks', json.dumps(self._task_payload('Delete Task')), content_type='application/json')
        tid = create_res.json()['id']
        res = admin_client.delete(f'/api/tasks/{tid}')
        assert res.status_code == 200
        assert res.json()['success'] is True
