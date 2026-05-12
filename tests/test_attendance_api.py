import json
import pytest
from main.models import User, Attendance
from datetime import date


class TestAttendanceAPI:

    @pytest.fixture
    def emp(self, db):
        return User.objects.create_user(
            email='attend@mail.com', login_email='atteend@mail.com',
            password='pass', name='Attend Emp', role='employee'
        )

    def _payload(self, user_id, date_str='2026-05-01', status='present'):
        return {
            'user_id': user_id,
            'date': date_str,
            'check_in_time': '09:00',
            'check_out_time': '18:00',
            'status': status,
        }

    # 1. List attendance returns 200
    def test_list_attendance_returns_200(self, admin_client):
        res = admin_client.get('/api/attendance')
        assert res.status_code == 200

    # 2. Create attendance record returns 200
    def test_create_attendance_valid(self, admin_client, emp):
        res = admin_client.post('/api/attendance', json.dumps(self._payload(emp.id)), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['status'] == 'present'

    # 3. Created attendance has correct user
    def test_create_attendance_correct_user(self, admin_client, emp):
        res = admin_client.post('/api/attendance', json.dumps(self._payload(emp.id)), content_type='application/json')
        assert res.json()['user_id'] == emp.id

    # 4. Filter attendance by user_id
    def test_filter_attendance_by_user(self, admin_client, emp):
        admin_client.post('/api/attendance', json.dumps(self._payload(emp.id, '2026-05-02')), content_type='application/json')
        res = admin_client.get(f'/api/attendance?user_id={emp.id}')
        assert res.status_code == 200
        for record in res.json():
            assert record['user_id'] == emp.id

    # 5. Filter attendance by date_from
    def test_filter_attendance_by_date_from(self, admin_client, emp):
        admin_client.post('/api/attendance', json.dumps(self._payload(emp.id, '2026-06-01')), content_type='application/json')
        res = admin_client.get('/api/attendance?date_from=2026-06-01')
        assert res.status_code == 200

    # 6. Filter attendance by date range
    def test_filter_attendance_by_date_range(self, admin_client, emp):
        admin_client.post('/api/attendance', json.dumps(self._payload(emp.id, '2026-07-15')), content_type='application/json')
        res = admin_client.get('/api/attendance?date_from=2026-07-01&date_to=2026-07-31')
        assert res.status_code == 200

    # 7. Update attendance record
    def test_update_attendance(self, admin_client, emp):
        create_res = admin_client.post('/api/attendance', json.dumps(self._payload(emp.id, '2026-08-01')), content_type='application/json')
        aid = create_res.json()['id']
        update = self._payload(emp.id, '2026-08-01', 'late')
        update['check_in_time'] = '10:00'
        res = admin_client.put(f'/api/attendance/{aid}', json.dumps(update), content_type='application/json')
        assert res.status_code == 200

    # 8. Delete attendance record
    def test_delete_attendance(self, admin_client, emp):
        create_res = admin_client.post('/api/attendance', json.dumps(self._payload(emp.id, '2026-09-01')), content_type='application/json')
        aid = create_res.json()['id']
        res = admin_client.delete(f'/api/attendance/{aid}')
        assert res.status_code == 200

    # 9. Attendance response has check_in_time field
    def test_attendance_has_check_in_time(self, admin_client, emp):
        res = admin_client.post('/api/attendance', json.dumps(self._payload(emp.id, '2026-10-01')), content_type='application/json')
        assert 'check_in_time' in res.json()

    # 10. Attendance stats returns 200
    def test_attendance_stats_returns_200(self, admin_client):
        res = admin_client.get('/api/attendance/stats')
        assert res.status_code == 200
