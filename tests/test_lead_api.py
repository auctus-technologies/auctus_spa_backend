import json
import pytest
from main.models import Lead, Client


class TestLeadAPI:

    def _lead_payload(self, name='Test Lead'):
        return {
            'client_name': name,
            'company_name': 'Test Co',
            'email': f'{name.replace(" ", "").lower()}@mail.com',
            'phone': '9876543210',
            'status': 'proposal',
            'lead_from': 'instagram',
            'lead_date': '2026-01-01',
        }

    # 1. List leads requires authentication
    def test_list_leads_requires_auth(self, anon_client):
        res = anon_client.get('/api/leads')
        assert res.status_code == 401

    # 2. List leads returns 200 when authenticated
    def test_list_leads_authenticated(self, admin_client):
        res = admin_client.get('/api/leads')
        assert res.status_code == 200

    # 3. List leads has pagination fields
    def test_list_leads_pagination_fields(self, admin_client):
        res = admin_client.get('/api/leads')
        for key in ['leads', 'total', 'page', 'total_pages']:
            assert key in res.json()

    # 4. Create lead with valid data
    def test_create_lead_valid(self, admin_client):
        res = admin_client.post('/api/leads', json.dumps(self._lead_payload('Alpha Lead')), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['client_name'] == 'Alpha Lead'

    # 5. Get lead by id returns correct data
    def test_get_lead_by_id(self, admin_client):
        create_res = admin_client.post('/api/leads', json.dumps(self._lead_payload('Beta Lead')), content_type='application/json')
        lid = create_res.json()['id']
        res = admin_client.get(f'/api/leads/{lid}')
        assert res.status_code == 200
        assert res.json()['id'] == lid

    # 6. Update lead changes client_name
    def test_update_lead(self, admin_client):
        create_res = admin_client.post('/api/leads', json.dumps(self._lead_payload('Gamma Lead')), content_type='application/json')
        lid = create_res.json()['id']
        update = self._lead_payload('Updated Lead')
        res = admin_client.put(f'/api/leads/{lid}', json.dumps(update), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['client_name'] == 'Updated Lead'

    # 7. Delete lead returns success
    def test_delete_lead(self, admin_client):
        create_res = admin_client.post('/api/leads', json.dumps(self._lead_payload('Delete Lead')), content_type='application/json')
        lid = create_res.json()['id']
        res = admin_client.delete(f'/api/leads/{lid}')
        assert res.status_code == 200
        assert res.json()['success'] is True

    # 8. Search leads by client name
    def test_search_leads_by_name(self, admin_client):
        admin_client.post('/api/leads', json.dumps(self._lead_payload('SearchableLead')), content_type='application/json')
        res = admin_client.get('/api/leads?search=SearchableLead')
        assert res.status_code == 200
        assert res.json()['total'] >= 1

    # 9. Filter leads by status
    def test_filter_leads_by_status(self, admin_client):
        admin_client.post('/api/leads', json.dumps(self._lead_payload('Proposal Lead')), content_type='application/json')
        res = admin_client.get('/api/leads?status=proposal')
        assert res.status_code == 200
        for lead in res.json()['leads']:
            assert lead['status'] == 'proposal'

    # 10. Convert lead to client
    def test_convert_lead_to_client(self, admin_client):
        create_res = admin_client.post('/api/leads', json.dumps(self._lead_payload('Convert Lead')), content_type='application/json')
        lid = create_res.json()['id']
        res = admin_client.post(f'/api/leads/{lid}/convert-to-client')
        assert res.status_code == 200
        assert res.json()['status'] == 'client'
