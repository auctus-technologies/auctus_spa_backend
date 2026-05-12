from ninja import File, UploadedFile
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpRequest
from ..models import Project, ProjectAttachment, Client, User, Notification
from .schemas.project_schemas import (
    ProjectSchema, ProjectListResponse, TeamMemberSchema,
    TeamMembersResponse, ClientListResponse, ProjectAttachmentSchema,
    TeamMemberDetailSchema
)
from . import api


def _notify_project_members(user_ids, project_name):
    users = User.objects.filter(id__in=user_ids)
    Notification.objects.bulk_create([
        Notification(
            user=u,
            title=f'Project Assigned: {project_name}',
            message=f'You have been added to the project "{project_name}".',
            notif_type='project_assigned',
        )
        for u in users
    ])


def _team_member_detail(member):
    avatar_url = None
    if member.avatar and member.avatar.name:
        avatar_url = f"/media/{member.avatar.name}"
    profile = getattr(member, 'profile', None)
    return {
        'id': member.id,
        'name': member.name,
        'designation': profile.designation if profile else None,
        'avatar_url': avatar_url,
    }


@api.get("/projects", response=ProjectListResponse)
def list_projects(
    request,
    search: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    """Get projects with optional search, status filter, and pagination"""
    qs = Project.objects.all().prefetch_related('team_members', 'attachments').select_related('client', 'created_by')

    # Non-admin users only see projects they are a member of
    if request.user.is_authenticated and request.user.role != 'admin':
        qs = qs.filter(team_members=request.user)

    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(client__name__icontains=search) |
            Q(created_by__name__icontains=search)
        )

    if status and status != 'All':
        qs = qs.filter(status=status)

    total = qs.count()
    page_size = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    project_list = []
    for project in qs[offset: offset + page_size]:
        members = list(project.team_members.select_related('profile').all())
        project_list.append({
            'id': project.id,
            'name': project.name,
            'client_id': project.client.id,
            'client_name': project.client.name,
            'description': project.description,
            'requirements': project.requirements,
            'team_members': [m.id for m in members],
            'team_member_names': [m.name for m in members],
            'team_member_details': [_team_member_detail(m) for m in members],
            'start_date': project.start_date,
            'end_date': project.end_date,
            'status': project.status,
            'attachments': [
                {
                    'id': att.id,
                    'file_name': att.file_name,
                    'file_size': att.file_size,
                    'file_type': att.file_type,
                    'uploaded_by': att.uploaded_by.name if att.uploaded_by else 'Unknown',
                    'uploaded_at': att.uploaded_at
                } for att in project.attachments.all()
            ],
            'created_by': project.created_by.name if project.created_by else None,
            'created_at': project.created_at,
            'updated_at': project.updated_at
        })

    return {
        'projects': project_list,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
    }


@api.get("/projects/{project_id}", response=ProjectSchema)
def get_project(request, project_id: int):
    """Get a single project by ID"""
    project = get_object_or_404(
        Project.objects.prefetch_related('team_members__profile', 'attachments'), id=project_id
    )
    members = list(project.team_members.select_related('profile').all())

    return {
        'id': project.id,
        'name': project.name,
        'client_id': project.client.id,
        'client_name': project.client.name,
        'description': project.description,
        'requirements': project.requirements,
        'team_members': [m.id for m in members],
        'team_member_names': [m.name for m in members],
        'team_member_details': [_team_member_detail(m) for m in members],
        'start_date': project.start_date,
        'end_date': project.end_date,
        'status': project.status,
        'attachments': [
            {
                'id': att.id,
                'file_name': att.file_name,
                'file_size': att.file_size,
                'file_type': att.file_type,
                'uploaded_by': att.uploaded_by.name if att.uploaded_by else None,
                'uploaded_at': att.uploaded_at
            } for att in project.attachments.all()
        ],
        'created_by': project.created_by.name if project.created_by else None,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    }


@api.post("/projects", response=ProjectSchema)
def create_project(request: HttpRequest, files: Optional[List[UploadedFile]] = File(None)):
    """Create a new project with attachments"""
    # Get form data directly from request
    client_id = int(request.POST.get('client_id'))
    name = request.POST.get('name')
    description = request.POST.get('description', '')
    requirements = request.POST.get('requirements', '')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    status = request.POST.get('status', 'Planning')
    team_members = request.POST.getlist('team_members')
    
    client = get_object_or_404(Client, id=client_id)
    
    project = Project.objects.create(
        name=name,
        client=client,
        description=description,
        requirements=requirements,
        start_date=start_date,
        end_date=end_date,
        status=status,
        created_by=request.user if request.user.is_authenticated else None
    )
    # Add team members
    if team_members:
        member_ids = [int(m) for m in team_members]
        project.team_members.set(member_ids)
        _notify_project_members(member_ids, project.name)
    
    # Handle file uploads
    if files:
        for file in files:
            ProjectAttachment.objects.create(
                project=project,
                file=file,
                file_name=file.name,
                file_size=file.size,
                file_type=file.content_type or 'Unknown',
                uploaded_by=request.user if request.user.is_authenticated else None
            )
    
    _members = list(project.team_members.select_related('profile').all())
    return {
        'id': project.id,
        'name': project.name,
        'client_id': project.client.id,
        'client_name': project.client.name,
        'description': project.description,
        'requirements': project.requirements,
        'team_members': [m.id for m in _members],
        'team_member_names': [m.name for m in _members],
        'team_member_details': [_team_member_detail(m) for m in _members],
        'start_date': project.start_date,
        'end_date': project.end_date,
        'status': project.status,
        'attachments': [
            {
                'id': att.id,
                'file_name': att.file_name,
                'file_size': att.file_size,
                'file_type': att.file_type,
                'uploaded_by': att.uploaded_by.name if att.uploaded_by else None,
                'uploaded_at': att.uploaded_at
            } for att in project.attachments.all()
        ],
        'created_by': project.created_by.name if project.created_by else None,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    }


@api.put("/projects/{project_id}", response=ProjectSchema)
def update_project(request: HttpRequest, project_id: int, files: Optional[List[UploadedFile]] = File(None)):
    """Update an existing project with optional new attachments"""
    # Get form data directly from request
    name = request.POST.get('name')
    client_id = request.POST.get('client_id')
    description = request.POST.get('description')
    requirements = request.POST.get('requirements')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    status = request.POST.get('status')
    team_members = request.POST.getlist('team_members')
    removed_attachment_ids = request.POST.getlist('removed_attachment_ids')

    project = get_object_or_404(Project.objects.prefetch_related('team_members', 'attachments'), id=project_id)
    prev_member_ids = set(project.team_members.values_list('id', flat=True))

    if name:
        project.name = name
    if client_id:
        project.client = get_object_or_404(Client, id=int(client_id))
    if description is not None:
        project.description = description
    if requirements is not None:
        project.requirements = requirements
    if start_date:
        project.start_date = start_date
    if end_date:
        project.end_date = end_date
    if status:
        project.status = status
    
    project.save()
    
    # Update team members — notify only newly added members
    if team_members:
        new_ids = [int(m) for m in team_members]
        project.team_members.set(new_ids)
        newly_added = set(new_ids) - prev_member_ids
        if newly_added:
            _notify_project_members(newly_added, project.name)
    
    # Delete removed attachments
    if removed_attachment_ids:
        ProjectAttachment.objects.filter(
            id__in=[int(i) for i in removed_attachment_ids],
            project=project
        ).delete()

    # Handle new file uploads
    if files:
        for file in files:
            ProjectAttachment.objects.create(
                project=project,
                file=file,
                file_name=file.name,
                file_size=file.size,
                file_type=file.content_type or 'Unknown',
                uploaded_by=request.user if request.user.is_authenticated else None
            )
    
    _upd_members = list(project.team_members.select_related('profile').all())
    return {
        'id': project.id,
        'name': project.name,
        'client_id': project.client.id,
        'client_name': project.client.name,
        'description': project.description,
        'requirements': project.requirements,
        'team_members': [m.id for m in _upd_members],
        'team_member_names': [m.name for m in _upd_members],
        'team_member_details': [_team_member_detail(m) for m in _upd_members],
        'start_date': project.start_date,
        'end_date': project.end_date,
        'status': project.status,
        'attachments': [
            {
                'id': att.id,
                'file_name': att.file_name,
                'file_size': att.file_size,
                'file_type': att.file_type,
                'uploaded_by': att.uploaded_by.name if att.uploaded_by else None,
                'uploaded_at': att.uploaded_at
            } for att in project.attachments.all()
        ],
        'created_by': project.created_by.name if project.created_by else None,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    }


@api.delete("/projects/{project_id}")
def delete_project(request, project_id: int):
    """Delete a project"""
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"success": True, "message": "Project deleted successfully"}


@api.get("/team-members", response=TeamMembersResponse)
def list_team_members(request):
    """Get all team members (non-admin users)"""
    members = User.objects.filter(role='employee', is_active=True, profile__department='development').select_related('profile')

    return {
        'members': [
            {
                'id': m.id,
                'name': m.name,
                'email': m.email,
                'designation': m.profile.designation if hasattr(m, 'profile') and m.profile else None
            } for m in members
        ]
    }


@api.get("/clients-for-projects", response=List[ClientListResponse])
def list_clients_for_projects(request):
    """Get all clients for project selection"""
    clients = Client.objects.filter(status='active').values('id', 'name', 'email', 'company')
    
    return [
        {
            'id': c['id'],
            'name': c['name'],
            'email': c['email'],
            'company': c['company']
        } for c in clients
    ]


@api.delete("/projects/{project_id}/attachments/{attachment_id}")
def delete_project_attachment(request, project_id: int, attachment_id: int):
    """Delete a project attachment"""
    attachment = get_object_or_404(ProjectAttachment, id=attachment_id, project_id=project_id)
    attachment.delete()
    return {"success": True, "message": "Attachment deleted successfully"}


@api.get("/projects/{project_id}/attachments/{attachment_id}/download")
def download_project_attachment(request, project_id: int, attachment_id: int):
    """Download a project attachment"""
    attachment = get_object_or_404(ProjectAttachment, id=attachment_id, project_id=project_id)
    
    from django.http import FileResponse
    return FileResponse(
        attachment.file.open(),
        as_attachment=True,
        filename=attachment.file_name
    )
