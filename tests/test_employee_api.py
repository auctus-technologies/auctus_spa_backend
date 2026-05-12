import json
import pytest
from main.models import User


class TestEmployeeAPI:

    def _create_payload(self, suffix='01'):
        return {
            'name': f'Emp {suffix}',
            'email': f'emp{suffix}@mail.com',
            'login_email': f'emp{suffix}@mail.com',
            'password': 'pass1234',
            'department': 'development',
            'designation': 'software_engineer',
        }

    # 1. List employees returns 200
    def test_list_employees_returns_200(self, admin_client):
        res = admin_client.get('/api/employees')
        assert res.status_code == 200

    # 2. List employees has pagination fields
    def test_list_employees_has_pagination(self, admin_client):
        res = admin_client.get('/api/employees')
        data = res.json()
        assert 'total' in data
        assert 'page' in data

    # 3. Create employee with valid data
    def test_create_employee_valid(self, admin_client):
        res = admin_client.post('/api/employees', json.dumps(self._create_payload('10')), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['role'] == 'employee'

    # 4. Created employee has correct department
    def test_create_employee_correct_department(self, admin_client):
        res = admin_client.post('/api/employees', json.dumps(self._create_payload('11')), content_type='application/json')
        assert res.json()['department'] == 'development'

    # 5. Get employee by id returns correct data
    def test_get_employee_by_id(self, admin_client):
        create_res = admin_client.post('/api/employees', json.dumps(self._create_payload('12')), content_type='application/json')
        emp_id = create_res.json()['id']
        res = admin_client.get(f'/api/employees/{emp_id}')
        assert res.status_code == 200
        assert res.json()['id'] == emp_id

    # 6. Search employees by name
    def test_search_employees_by_name(self, admin_client):
        admin_client.post('/api/employees', json.dumps(self._create_payload('13')), content_type='application/json')
        res = admin_client.get('/api/employees?search=Emp+13')
        assert res.status_code == 200

    # 7. Filter employees by department
    def test_filter_employees_by_department(self, admin_client):
        admin_client.post('/api/employees', json.dumps(self._create_payload('14')), content_type='application/json')
        res = admin_client.get('/api/employees?department=development')
        assert res.status_code == 200

    # 8. Update employee name
    def test_update_employee(self, admin_client):
        create_res = admin_client.post('/api/employees', json.dumps(self._create_payload('15')), content_type='application/json')
        emp_id = create_res.json()['id']
        update = {
            'name': 'Updated Emp',
            'email': 'emp15@mail.com',
            'login_email': 'emp15@mail.com',
            'employee_id': create_res.json().get('employee_id', 'EMP001'),
            'department': 'development',
            'designation': 'software_engineer',
        }
        res = admin_client.put(f'/api/employees/{emp_id}', json.dumps(update), content_type='application/json')
        assert res.status_code == 200
        assert res.json()['name'] == 'Updated Emp'

    # 9. Delete employee returns success
    def test_delete_employee(self, admin_client):
        create_res = admin_client.post('/api/employees', json.dumps(self._create_payload('16')), content_type='application/json')
        emp_id = create_res.json()['id']
        res = admin_client.delete(f'/api/employees/{emp_id}')
        assert res.status_code == 200

    # 10. Page size limits results
    def test_employee_page_size(self, admin_client):
        for i in range(20, 25):
            admin_client.post('/api/employees', json.dumps(self._create_payload(str(i))), content_type='application/json')
        res = admin_client.get('/api/employees?page_size=2')
        assert res.status_code == 200
        assert len(res.json()['employees']) <= 2
