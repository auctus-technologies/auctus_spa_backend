import json
import pytest
from main.models import Client


class TestProjectAPI:

    @pytest.fixture
    def client_record(self, db):
        return Client.objects.create(name='Test Client', email='tclient@mail.com')

    def _project_payload(self, client_id, name='Test Project'):
        return {
            'name': name,
            'client_id': client_id,
            'start_date': '2026-01-01',
            'end_date': '2026-12-31',
            'status': 'Planning',
            'description': 'Test description',
            'requirements': 'Test requirements',
        }

    # 1. List projects returns 200
    def test_list_projects_returns_200(self, admin_client):
        res = admin_client.get('/api/projects')
        assert res.status_code == 200

    # 2. List projects has pagination fields
    def test_list_projects_has_pagination(self, admin_client):
        res = admin_client.get('/api/projects')
        data = res.json()
        for key in ['projects', 'total', 'page', 'total_pages']:
            assert key in data

    # 3. Create project with valid data
    def test_create_project_valid(self, admin_client, client_record):
        payload = self._project_payload(client_record.id)
        res = admin_client.post(
            '/api/projects',
            data={'name': 'Test Project', 'client_id': client_record.id,
                  'start_date': '2026-01-01', 'end_date': '2026-12-31', 'status': 'Planning'},
        )
        assert res.status_code == 200

    # 4. Get project by id returns 200
    def test_get_project_by_id(self, admin_client, client_record):
        create_res = admin_client.post(
            '/api/projects',
            data={'name': 'Get Project', 'client_id': client_record.id,
                  'start_date': '2026-01-01', 'end_date': '2026-06-30', 'status': 'Planning'},
        )
        pid = create_res.json()['id']
        res = admin_client.get(f'/api/projects/{pid}')
        assert res.status_code == 200
        assert res.json()['id'] == pid

    # 5. Search projects by name
    def test_search_projects_by_name(self, admin_client, client_record):
        admin_client.post(
            '/api/projects',
            data={'name': 'UniqueSearchProject', 'client_id': client_record.id,
                  'start_date': '2026-01-01', 'end_date': '2026-06-30', 'status': 'Planning'},
        )
        res = admin_client.get('/api/projects?search=UniqueSearch')
        assert res.status_code == 200
        assert res.json()['total'] >= 1

    # 6. Filter projects by status
    def test_filter_projects_by_status(self, admin_client, client_record):
        admin_client.post(
            '/api/projects',
            data={'name': 'Completed Project', 'client_id': client_record.id,
                  'start_date': '2025-01-01', 'end_date': '2025-12-31', 'status': 'Completed'},
        )
        res = admin_client.get('/api/projects?status=Completed')
        assert res.status_code == 200
        for p in res.json()['projects']:
            assert p['status'] == 'Completed'

    # 7. Delete project returns success
    def test_delete_project(self, admin_client, client_record):
        create_res = admin_client.post(
            '/api/projects',
            data={'name': 'Delete Me', 'client_id': client_record.id,
                  'start_date': '2026-01-01', 'end_date': '2026-06-30', 'status': 'Planning'},
        )
        pid = create_res.json()['id']
        res = admin_client.delete(f'/api/projects/{pid}')
        assert res.status_code == 200

    # 8. List team members returns 200
    def test_list_team_members(self, admin_client):
        res = admin_client.get('/api/team-members')
        assert res.status_code == 200

    # 9. Employee only sees their own projects
    def test_employee_sees_only_own_projects(self, employee_client, client_record):
        res = employee_client.get('/api/projects')
        assert res.status_code == 200
        # Employee has no team assignments, so total should be 0
        assert res.json()['total'] == 0

    # 10. Pagination page_size limits results
    def test_page_size_limits_results(self, admin_client, client_record):
        for i in range(3):
            admin_client.post(
                '/api/projects',
                data={'name': f'Page Project {i}', 'client_id': client_record.id,
                      'start_date': '2026-01-01', 'end_date': '2026-12-31', 'status': 'Planning'},
            )
        res = admin_client.get('/api/projects?page_size=2')
        assert len(res.json()['projects']) <= 2
