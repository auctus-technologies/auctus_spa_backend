import json
import pytest
from main.models import Notification, User


class TestNotificationAPI:

    @pytest.fixture
    def notification(self, admin_user):
        return Notification.objects.create(
            user=admin_user,
            title='Test Notification',
            message='This is a test',
            notif_type='task_assigned',
            is_read=False,
        )

    # 1. List notifications requires auth
    def test_list_notifications_requires_auth(self, anon_client):
        res = anon_client.get('/api/notifications')
        assert res.status_code == 401

    # 2. List notifications returns 200 when authenticated
    def test_list_notifications_authenticated(self, admin_client):
        res = admin_client.get('/api/notifications')
        assert res.status_code == 200

    # 3. Response has notifications list and unread_count
    def test_notifications_response_structure(self, admin_client):
        res = admin_client.get('/api/notifications')
        data = res.json()
        assert 'notifications' in data
        assert 'unread_count' in data

    # 4. New notification is unread
    def test_new_notification_is_unread(self, admin_client, notification):
        res = admin_client.get('/api/notifications')
        unread = [n for n in res.json()['notifications'] if not n['is_read']]
        assert len(unread) >= 1

    # 5. Unread count matches actual unread notifications
    def test_unread_count_correct(self, admin_client, notification):
        res = admin_client.get('/api/notifications')
        data = res.json()
        unread_in_list = sum(1 for n in data['notifications'] if not n['is_read'])
        assert data['unread_count'] == unread_in_list

    # 6. Mark notification as read requires auth
    def test_mark_read_requires_auth(self, anon_client, notification):
        res = anon_client.post(f'/api/notifications/{notification.id}/read')
        assert res.status_code == 401

    # 7. Mark notification as read returns success
    def test_mark_notification_read(self, admin_client, notification):
        res = admin_client.post(f'/api/notifications/{notification.id}/read')
        assert res.status_code == 200
        assert res.json()['success'] is True

    # 8. Unread count decreases after marking as read
    def test_unread_count_decreases_after_read(self, admin_client, notification):
        before = admin_client.get('/api/notifications').json()['unread_count']
        admin_client.post(f'/api/notifications/{notification.id}/read')
        after = admin_client.get('/api/notifications').json()['unread_count']
        assert after == before - 1

    # 9. Mark all notifications as read
    def test_mark_all_read(self, admin_client, notification):
        res = admin_client.post('/api/notifications/read-all')
        assert res.status_code == 200
        assert res.json()['success'] is True

    # 10. Unread count is 0 after mark all read
    def test_unread_count_zero_after_mark_all(self, admin_client, notification):
        admin_client.post('/api/notifications/read-all')
        res = admin_client.get('/api/notifications')
        assert res.json()['unread_count'] == 0
