import json
import pytest
from main.models import Lead, User
from main.models.employee_profile import EmployeeProfile


class TestFollowUpAPI:

    @pytest.fixture
    def lead(self, db):
        return Lead.objects.create(client_name='Follow-up Lead', lead_date='2026-01-01')

    @pytest.fixture
    def sales_user(self, db):
        user = User.objects.create_user(
            email='sales@mail.com', login_email='sales@mail.com',
            password='pass', name='Sales Person', role='employee'
        )
        EmployeeProfile.objects.create(user=user, department='sales', designation='sales_executive')
        return user

    def _fu_payload(self, user_id):
        return {
            'follow_up_user_id': user_id,
            'follow_up_date': '2026-06-01',
            'notes': 'Called and discussed requirements',
        }

    # 1. Get follow-up users requires auth
    def test_get_follow_up_users_requires_auth(self, anon_client):
        res = anon_client.get('/api/lead-follow-up-users')
        assert res.status_code == 401

    # 2. Get follow-up users returns list when authenticated
    def test_get_follow_up_users_returns_list(self, admin_client, sales_user):
        res = admin_client.get('/api/lead-follow-up-users')
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    # 3. List follow-ups requires auth
    def test_list_follow_ups_requires_auth(self, anon_client, lead):
        res = anon_client.get(f'/api/leads/{lead.id}/follow-ups')
        assert res.status_code == 401

    # 4. List follow-ups returns empty list for new lead
    def test_list_follow_ups_empty_for_new_lead(self, admin_client, lead):
        res = admin_client.get(f'/api/leads/{lead.id}/follow-ups')
        assert res.status_code == 200
        assert res.json() == []

    # 5. Create follow-up requires auth
    def test_create_follow_up_requires_auth(self, anon_client, lead, sales_user):
        res = anon_client.post(f'/api/leads/{lead.id}/follow-ups', json.dumps(self._fu_payload(sales_user.id)), content_type='application/json')
        assert res.status_code == 401

    # 6. Create follow-up with valid data
    def test_create_follow_up_valid(self, admin_client, lead, sales_user):
        res = admin_client.post(f'/api/leads/{lead.id}/follow-ups', json.dumps(self._fu_payload(sales_user.id)), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['lead_id'] == lead.id

    # 7. Follow-up appears in list after creation
    def test_follow_up_appears_in_list(self, admin_client, lead, sales_user):
        admin_client.post(f'/api/leads/{lead.id}/follow-ups', json.dumps(self._fu_payload(sales_user.id)), content_type='application/json')
        res = admin_client.get(f'/api/leads/{lead.id}/follow-ups')
        assert len(res.json()) == 1

    # 8. Update follow-up changes notes
    def test_update_follow_up(self, admin_client, lead, sales_user):
        create_res = admin_client.post(f'/api/leads/{lead.id}/follow-ups', json.dumps(self._fu_payload(sales_user.id)), content_type='application/json')
        fu_id = create_res.json()['id']
        update = self._fu_payload(sales_user.id)
        update['notes'] = 'Updated notes'
        res = admin_client.put(f'/api/leads/{lead.id}/follow-ups/{fu_id}', json.dumps(update), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['notes'] == 'Updated notes'

    # 9. Delete follow-up returns success
    def test_delete_follow_up(self, admin_client, lead, sales_user):
        create_res = admin_client.post(f'/api/leads/{lead.id}/follow-ups', json.dumps(self._fu_payload(sales_user.id)), content_type='application/json')
        fu_id = create_res.json()['id']
        res = admin_client.delete(f'/api/leads/{lead.id}/follow-ups/{fu_id}')
        assert res.status_code == 200

    # 10. Follow-up has correct follow_up_date
    def test_follow_up_has_correct_date(self, admin_client, lead, sales_user):
        admin_client.post(f'/api/leads/{lead.id}/follow-ups', json.dumps(self._fu_payload(sales_user.id)), content_type='application/json')
        res = admin_client.get(f'/api/leads/{lead.id}/follow-ups')
        assert res.json()[0]['follow_up_date'] == '2026-06-01'
