import json
import pytest


class TestOpeningAPI:

    def _opening_payload(self, title='Software Engineer'):
        return {
            'job_title': title,
            'department': 'development',
            'role': 'software_engineer',
            'location': 'Chennai',
            'required_experience': 2,
            'status': 'active',
        }

    # 1. List openings returns 200
    def test_list_openings_returns_200(self, admin_client):
        res = admin_client.get('/api/openings')
        assert res.status_code == 200

    # 2. List openings has pagination fields
    def test_list_openings_has_pagination(self, admin_client):
        res = admin_client.get('/api/openings')
        for key in ['openings', 'total', 'page', 'total_pages']:
            assert key in res.json()

    # 3. Create opening requires auth
    def test_create_opening_requires_auth(self, anon_client):
        res = anon_client.post('/api/openings', json.dumps(self._opening_payload()), content_type='application/json')
        assert res.status_code == 401

    # 4. Create opening with valid data
    def test_create_opening_valid(self, admin_client):
        res = admin_client.post('/api/openings', json.dumps(self._opening_payload()), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['job_title'] == 'Software Engineer'

    # 5. Get opening by id returns correct data
    def test_get_opening_by_id(self, admin_client):
        create_res = admin_client.post('/api/openings', json.dumps(self._opening_payload('DevOps Lead')), content_type='application/json')
        oid = create_res.json()['id']
        res = admin_client.get(f'/api/openings/{oid}')
        assert res.status_code == 200
        assert res.json()['id'] == oid

    # 6. Update opening changes job_title
    def test_update_opening(self, admin_client):
        create_res = admin_client.post('/api/openings', json.dumps(self._opening_payload('Old Title')), content_type='application/json')
        oid = create_res.json()['id']
        update = self._opening_payload('New Title')
        update['status'] = 'active'
        res = admin_client.put(f'/api/openings/{oid}', json.dumps(update), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['job_title'] == 'New Title'

    # 7. Delete opening returns success
    def test_delete_opening(self, admin_client):
        create_res = admin_client.post('/api/openings', json.dumps(self._opening_payload('Delete Opening')), content_type='application/json')
        oid = create_res.json()['id']
        res = admin_client.delete(f'/api/openings/{oid}')
        assert res.status_code == 200

    # 8. Search openings by job title
    def test_search_openings_by_title(self, admin_client):
        admin_client.post('/api/openings', json.dumps(self._opening_payload('UniqueOpeningTitle')), content_type='application/json')
        res = admin_client.get('/api/openings?search=UniqueOpeningTitle')
        assert res.json()['total'] >= 1

    # 9. Filter openings by status active
    def test_filter_openings_by_status(self, admin_client):
        admin_client.post('/api/openings', json.dumps(self._opening_payload('Active Role')), content_type='application/json')
        res = admin_client.get('/api/openings?status=active')
        assert res.status_code == 200
        for o in res.json()['openings']:
            assert o['status'] == 'active'

    # 10. Get form choices returns departments and designations
    def test_get_form_choices(self, admin_client):
        res = admin_client.get('/api/openings/form-choices')
        assert res.status_code == 200
        data = res.json()
        assert 'departments' in data
        assert 'designations' in data
        assert len(data['departments']) > 0
