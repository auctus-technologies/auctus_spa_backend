import pytest


class TestCoreAPI:

    # 1. Health check returns 200
    def test_health_check_status_200(self, client):
        res = client.get('/api/health')
        assert res.status_code == 200

    # 2. Health check response body has status "ok"
    def test_health_check_status_ok(self, client):
        res = client.get('/api/health')
        assert res.json()['status'] == 'ok'

    # 3. Health check response has message field
    def test_health_check_has_message(self, client):
        res = client.get('/api/health')
        assert 'message' in res.json()

    # 4. Dashboard stats returns 200
    def test_dashboard_stats_returns_200(self, client):
        res = client.get('/api/dashboard/stats')
        assert res.status_code == 200

    # 5. Dashboard stats has all required keys
    def test_dashboard_stats_has_required_keys(self, client):
        res = client.get('/api/dashboard/stats')
        data = res.json()
        for key in ['total_leads', 'total_clients', 'total_projects', 'total_users']:
            assert key in data

    # 6. Dashboard stats counts are non-negative integers
    def test_dashboard_stats_counts_non_negative(self, client):
        res = client.get('/api/dashboard/stats')
        data = res.json()
        assert data['total_leads'] >= 0
        assert data['total_projects'] >= 0

    # 7. Dashboard charts returns 200
    def test_dashboard_charts_returns_200(self, client):
        res = client.get('/api/dashboard/charts')
        assert res.status_code == 200

    # 8. Dashboard charts has leads_by_month with 6 months
    def test_dashboard_charts_leads_by_month(self, client):
        res = client.get('/api/dashboard/charts')
        data = res.json()
        assert 'leads_by_month' in data
        assert len(data['leads_by_month']) == 6

    # 9. Dev stats requires authentication
    def test_dev_stats_requires_auth(self, anon_client):
        res = anon_client.get('/api/dashboard/dev-stats')
        assert res.status_code == 401

    # 10. Dev stats returns 200 when authenticated
    def test_dev_stats_authenticated(self, admin_client):
        res = admin_client.get('/api/dashboard/dev-stats')
        assert res.status_code == 200
        data = res.json()
        assert 'my_active' in data
        assert 'my_completed' in data
