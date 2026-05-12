import json
import pytest


class TestHolidayAPI:

    def _payload(self, name='Diwali', date='2026-10-20'):
        return {'name': name, 'date': date}

    # 1. List holidays requires auth
    def test_list_holidays_requires_auth(self, anon_client):
        res = anon_client.get('/api/holidays')
        assert res.status_code == 401

    # 2. List holidays returns 200 when authenticated
    def test_list_holidays_authenticated(self, admin_client):
        res = admin_client.get('/api/holidays')
        assert res.status_code == 200

    # 3. List holidays has total count field
    def test_list_holidays_has_total(self, admin_client):
        res = admin_client.get('/api/holidays')
        assert 'total' in res.json()

    # 4. Create holiday requires auth
    def test_create_holiday_requires_auth(self, anon_client):
        res = anon_client.post('/api/holidays', json.dumps(self._payload()), content_type='application/json')
        assert res.status_code == 401

    # 5. Create holiday with valid data returns 200
    def test_create_holiday_valid(self, admin_client):
        res = admin_client.post('/api/holidays', json.dumps(self._payload()), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['name'] == 'Diwali'

    # 6. Created holiday appears in list
    def test_created_holiday_in_list(self, admin_client):
        admin_client.post('/api/holidays', json.dumps(self._payload('Christmas', '2026-12-25')), content_type='application/json')
        res = admin_client.get('/api/holidays')
        names = [h['name'] for h in res.json()['holidays']]
        assert 'Christmas' in names

    # 7. Update holiday name returns 200
    def test_update_holiday_name(self, admin_client):
        create_res = admin_client.post('/api/holidays', json.dumps(self._payload('Old Name', '2026-01-14')), content_type='application/json')
        hid = create_res.json()['id']
        res = admin_client.put(f'/api/holidays/{hid}', json.dumps({'name': 'New Name', 'date': '2026-01-14'}), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['name'] == 'New Name'

    # 8. Update holiday date returns 200
    def test_update_holiday_date(self, admin_client):
        create_res = admin_client.post('/api/holidays', json.dumps(self._payload('Pongal', '2026-01-14')), content_type='application/json')
        hid = create_res.json()['id']
        res = admin_client.put(f'/api/holidays/{hid}', json.dumps({'name': 'Pongal', 'date': '2026-01-15'}), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['date'] == '2026-01-15'

    # 9. Delete holiday returns success
    def test_delete_holiday(self, admin_client):
        create_res = admin_client.post('/api/holidays', json.dumps(self._payload('Delete Holiday', '2026-03-01')), content_type='application/json')
        hid = create_res.json()['id']
        res = admin_client.delete(f'/api/holidays/{hid}')
        assert res.status_code == 200
        assert res.json()['success'] is True

    # 10. Total count increases after creating a holiday
    def test_total_increases_after_create(self, admin_client):
        before = admin_client.get('/api/holidays').json()['total']
        admin_client.post('/api/holidays', json.dumps(self._payload('New Festival', '2026-04-01')), content_type='application/json')
        after = admin_client.get('/api/holidays').json()['total']
        assert after == before + 1
