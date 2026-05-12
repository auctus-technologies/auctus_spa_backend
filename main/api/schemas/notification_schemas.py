from ninja import Schema
from datetime import datetime
from typing import List


class NotificationSchema(Schema):
    id: int
    title: str
    message: str
    notif_type: str
    is_read: bool
    created_at: datetime


class NotificationListResponse(Schema):
    notifications: List[NotificationSchema]
    unread_count: int
