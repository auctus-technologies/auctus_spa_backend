from django.shortcuts import get_object_or_404
from . import api
from main.models import Notification
from .schemas.notification_schemas import NotificationSchema, NotificationListResponse


@api.get('/notifications', response=NotificationListResponse)
def list_notifications(request):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)

    qs = Notification.objects.filter(user=request.user).order_by('-created_at')[:50]
    notifications = list(qs)
    unread = sum(1 for n in notifications if not n.is_read)

    return NotificationListResponse(
        notifications=[
            NotificationSchema(
                id=n.id, title=n.title, message=n.message,
                notif_type=n.notif_type, is_read=n.is_read, created_at=n.created_at,
            )
            for n in notifications
        ],
        unread_count=unread,
    )


@api.post('/notifications/{notif_id}/read')
def mark_read(request, notif_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return {'success': True}


@api.post('/notifications/read-all')
def mark_all_read(request):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return {'success': True}
