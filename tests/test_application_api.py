import json
import pytest
from main.models import JobOpening


class TestApplicationAPI:

    @pytest.fixture
    def opening(self, db):
        return JobOpening.objects.create(job_title='Test Role', status='active')

    def _app_data(self, opening_id=None, email='applicant@mail.com'):
        data = {'full_name': 'John Applicant', 'email': email}
        if opening_id:
            data['opening_id'] = opening_id
        return data

    # 1. Submit application without auth (public endpoint) returns 200
    def test_submit_application_public(self, anon_client, opening):
        res = anon_client.post('/api/applications', data=self._app_data(opening.id))
        assert res.status_code == 200

    # 2. Application stores full_name correctly
    def test_application_stores_full_name(self, anon_client, opening):
        res = anon_client.post('/api/applications', data=self._app_data(opening.id, 'unique_app1@mail.com'))
        assert res.json()['full_name'] == 'John Applicant'

    # 3. Duplicate application returns 409
    def test_duplicate_application_returns_409(self, anon_client, opening):
        anon_client.post('/api/applications', data=self._app_data(opening.id, 'dup@mail.com'))
        res = anon_client.post('/api/applications', data=self._app_data(opening.id, 'dup@mail.com'))
        assert res.status_code == 409

    # 4. List applications requires auth
    def test_list_applications_requires_auth(self, anon_client):
        res = anon_client.get('/api/applications')
        assert res.status_code == 401

    # 5. Admin can list all applications
    def test_admin_list_applications(self, admin_client):
        res = admin_client.get('/api/applications')
        assert res.status_code == 200

    # 6. List applications has pagination fields
    def test_list_applications_pagination(self, admin_client):
        res = admin_client.get('/api/applications')
        for key in ['applications', 'total', 'page']:
            assert key in res.json()

    # 7. Get application by id
    def test_get_application_by_id(self, admin_client, anon_client, opening):
        anon_client.post('/api/applications', data=self._app_data(opening.id, 'getbyid@mail.com'))
        res = admin_client.get('/api/applications')
        app_id = res.json()['applications'][0]['id']
        detail_res = admin_client.get(f'/api/applications/{app_id}')
        assert detail_res.status_code == 200

    # 8. Update application status (admin)
    def test_update_application_status(self, admin_client, anon_client, opening):
        anon_client.post('/api/applications', data=self._app_data(opening.id, 'statustest@mail.com'))
        app_id = admin_client.get('/api/applications').json()['applications'][0]['id']
        res = admin_client.patch(
            f'/api/applications/{app_id}/status',
            json.dumps({'status': 'shortlisted'}),
            content_type='application/json'
        )
        assert res.status_code == 200

    # 9. Delete application (admin)
    def test_delete_application(self, admin_client, anon_client, opening):
        anon_client.post('/api/applications', data=self._app_data(opening.id, 'delapp@mail.com'))
        app_id = admin_client.get('/api/applications').json()['applications'][0]['id']
        res = admin_client.delete(f'/api/applications/{app_id}')
        assert res.status_code == 200

    # 10. Filter applications by opening id
    def test_filter_applications_by_opening(self, admin_client, anon_client, opening):
        anon_client.post('/api/applications', data=self._app_data(opening.id, 'filter@mail.com'))
        res = admin_client.get(f'/api/applications?opening_id={opening.id}')
        assert res.status_code == 200
