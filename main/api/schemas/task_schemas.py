from ninja import Schema
from datetime import date, datetime
from typing import Optional, List


class TaskSchema(Schema):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    assigned_user_ids: List[int]
    assigned_user_names: List[str]
    due_date: date
    status: str
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    created_by_name: Optional[str] = None
    created_at: datetime


class TaskCreateSchema(Schema):
    title: str
    description: Optional[str] = None
    priority: str = 'medium'
    assigned_user_ids: List[int] = []
    due_date: date
    project_id: Optional[int] = None


class TaskUpdateSchema(Schema):
    title: str
    description: Optional[str] = None
    priority: str
    assigned_user_ids: List[int] = []
    due_date: date
    project_id: Optional[int] = None


class TaskStatusUpdateSchema(Schema):
    status: str


class TaskListResponse(Schema):
    tasks: List[TaskSchema]
    total: int
    page: int
    page_size: int
    total_pages: int
