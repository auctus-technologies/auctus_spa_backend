from typing import Optional
from django.shortcuts import get_object_or_404
from django.db.models import Q
from . import api
from main.models import Task, User, Notification, Project
from .schemas.task_schemas import (
    TaskSchema, TaskCreateSchema, TaskUpdateSchema,
    TaskStatusUpdateSchema, TaskListResponse,
)


def _notify_users(user_ids, title, message):
    users = User.objects.filter(id__in=user_ids)
    Notification.objects.bulk_create([
        Notification(user=u, title=title, message=message, notif_type='task_assigned')
        for u in users
    ])


def _to_schema(task: Task) -> TaskSchema:
    users = list(task.assigned_users.all())
    return TaskSchema(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        assigned_user_ids=[u.id for u in users],
        assigned_user_names=[u.name for u in users],
        due_date=task.due_date,
        status=task.status,
        project_id=task.project_id,
        project_name=task.project.name if task.project else None,
        created_by_name=task.created_by.name if task.created_by else None,
        created_at=task.created_at,
    )


@api.get('/tasks', response=TaskListResponse)
def list_tasks(
    request,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)

    qs = Task.objects.prefetch_related('assigned_users').select_related('created_by', 'project')

    if request.user.role != 'admin':
        qs = qs.filter(assigned_users=request.user)

    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if priority and priority != 'all':
        qs = qs.filter(priority=priority)
    if status and status != 'all':
        qs = qs.filter(status=status)

    total = qs.count()
    page_size = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    return TaskListResponse(
        tasks=[_to_schema(t) for t in qs[offset:offset + page_size]],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@api.post('/tasks', response=TaskSchema)
def create_task(request, data: TaskCreateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    if request.user.role != 'admin':
        return api.create_response(request, {'error': 'Permission denied'}, status=403)

    project = None
    if data.project_id:
        project = get_object_or_404(Project, id=data.project_id)

    task = Task.objects.create(
        title=data.title,
        description=data.description or None,
        priority=data.priority,
        due_date=data.due_date,
        project=project,
        created_by=request.user,
    )
    if data.assigned_user_ids:
        task.assigned_users.set(User.objects.filter(id__in=data.assigned_user_ids))
        _notify_users(
            data.assigned_user_ids,
            title=f'New Task: {task.title}',
            message=f'You have been assigned a new task "{task.title}" due {task.due_date}.',
        )

    task.refresh_from_db()
    return _to_schema(task)


@api.put('/tasks/{task_id}', response=TaskSchema)
def update_task(request, task_id: int, data: TaskUpdateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    if request.user.role != 'admin':
        return api.create_response(request, {'error': 'Permission denied'}, status=403)

    task = get_object_or_404(Task.objects.select_related('project'), id=task_id)
    prev_user_ids = set(task.assigned_users.values_list('id', flat=True))
    task.title = data.title
    task.description = data.description or None
    task.priority = data.priority
    task.due_date = data.due_date
    task.project = get_object_or_404(Project, id=data.project_id) if data.project_id else None
    task.save()
    task.assigned_users.set(User.objects.filter(id__in=data.assigned_user_ids))

    # notify only newly added users
    new_user_ids = set(data.assigned_user_ids) - prev_user_ids
    if new_user_ids:
        _notify_users(
            new_user_ids,
            title=f'Task Assigned: {task.title}',
            message=f'You have been assigned to the task "{task.title}" due {task.due_date}.',
        )

    task.refresh_from_db()
    return _to_schema(task)


@api.patch('/tasks/{task_id}/status', response=TaskSchema)
def update_task_status(request, task_id: int, data: TaskStatusUpdateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)

    task = get_object_or_404(Task, id=task_id)

    if request.user.role != 'admin' and not task.assigned_users.filter(id=request.user.id).exists():
        return api.create_response(request, {'error': 'Permission denied'}, status=403)

    valid = {'in_progress', 'review', 'completed'}
    if data.status not in valid:
        return api.create_response(request, {'error': 'Invalid status'}, status=400)

    task.status = data.status
    task.save()
    task.refresh_from_db()
    return _to_schema(task)


@api.delete('/tasks/{task_id}')
def delete_task(request, task_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    if request.user.role != 'admin':
        return api.create_response(request, {'error': 'Permission denied'}, status=403)

    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return {'success': True}
