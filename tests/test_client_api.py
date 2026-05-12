import json
import pytest
from main.models import Client


class TestClientAPI:

    def _client_payload(self, suffix='01'):
        return {
            'name': f'Client {suffix}',
            'email': f'client{suffix}@mail.com',
            'phone': '9876543210',
            'company': f'Company {suffix}',
            'status': 'active',
        }

    # 1. List clients returns 200
    def test_list_clients_returns_200(self, admin_client):
        res = admin_client.get('/api/clients')
        assert res.status_code == 200

    # 2. List clients response has pagination fields
    def test_list_clients_has_pagination(self, admin_client):
        res = admin_client.get('/api/clients')
        data = res.json()
        for key in ['total', 'page', 'total_pages', 'active_count', 'inactive_count']:
            assert key in data

    # 3. Create client with valid data
    def test_create_client_valid(self, admin_client):
        res = admin_client.post('/api/clients', json.dumps(self._client_payload('10')), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['name'] == 'Client 10'

    # 4. Get client by id
    def test_get_client_by_id(self, admin_client):
        create_res = admin_client.post('/api/clients', json.dumps(self._client_payload('11')), content_type='application/json')
        cid = create_res.json()['id']
        res = admin_client.get(f'/api/clients/{cid}')
        assert res.status_code == 200
        assert res.json()['id'] == cid

    # 5. Update client name
    def test_update_client(self, admin_client):
        create_res = admin_client.post('/api/clients', json.dumps(self._client_payload('12')), content_type='application/json')
        cid = create_res.json()['id']
        update = self._client_payload('12')
        update['name'] = 'Updated Client'
        res = admin_client.put(f'/api/clients/{cid}', json.dumps(update), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['name'] == 'Updated Client'

    # 6. Delete client returns success
    def test_delete_client(self, admin_client):
        create_res = admin_client.post('/api/clients', json.dumps(self._client_payload('13')), content_type='application/json')
        cid = create_res.json()['id']
        res = admin_client.delete(f'/api/clients/{cid}')
        assert res.status_code == 200

    # 7. Search clients by name
    def test_search_clients_by_name(self, admin_client):
        admin_client.post('/api/clients', json.dumps(self._client_payload('14')), content_type='application/json')
        res = admin_client.get('/api/clients?search=Client+14')
        assert res.status_code == 200
        data = res.json()
        assert any('14' in c['name'] for c in data['clients'])

    # 8. Filter clients by status active
    def test_filter_clients_by_status(self, admin_client):
        admin_client.post('/api/clients', json.dumps(self._client_payload('15')), content_type='application/json')
        res = admin_client.get('/api/clients?status=active')
        assert res.status_code == 200
        for c in res.json()['clients']:
            assert c['status'] == 'active'

    # 9. Active count matches actual active clients
    def test_active_count_correct(self, admin_client, db):
        active = Client.objects.filter(status='active').count()
        res = admin_client.get('/api/clients')
        assert res.json()['active_count'] == active

    # 10. Page size limits results
    def test_page_size_limits_results(self, admin_client):
        for i in range(20, 25):
            admin_client.post('/api/clients', json.dumps(self._client_payload(str(i))), content_type='application/json')
        res = admin_client.get('/api/clients?page_size=2')
        assert len(res.json()['clients']) <= 2
