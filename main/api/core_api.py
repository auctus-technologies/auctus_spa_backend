from datetime import datetime
from . import api
from .schemas import (
    HealthResponse, DashboardStats,
    ProjectSchema, ProjectCreateSchema,
)
from .schemas.core_schemas import DashboardCharts, MonthlyLeadPoint, LeadStatusPoint, ProjectStatusPoint, DevStats, DevCharts


# Core Endpoints
@api.get("/health", response=HealthResponse)
def health_check(request):
    return HealthResponse(
        status="ok",
        message="Auctus API is running",
        timestamp=datetime.now().isoformat()
    )


# Dashboard stats endpoint
@api.get("/dashboard/stats", response=DashboardStats)
def get_dashboard_stats(request):
    from main.models import User, Attendance, LeaveRequest, Lead
    from main.models.client import Client
    from main.models.project import Project
    from datetime import date

    from datetime import time as time_type
    today = date.today()
    late_time = time_type(9, 30)

    total_leads = Lead.objects.count()
    total_clients = Client.objects.count()
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status__in=['Planning', 'Progress', 'Testing']).count()
    total_users = User.objects.filter(role='employee').count()
    present_today = Attendance.objects.filter(date=today, status='present').count()
    late_checkins = Attendance.objects.filter(date=today, check_in_time__gt=late_time).count()
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    new_leads_this_month = Lead.objects.filter(
        created_at__month=today.month,
        created_at__year=today.year,
    ).count()
    leads_proposal = Lead.objects.filter(status='proposal').count()
    leads_processing = Lead.objects.filter(status='processing').count()
    leads_converted = Lead.objects.filter(status='client').count()
    completed_projects = Project.objects.filter(status='Completed').count()

    return DashboardStats(
        total_leads=total_leads,
        total_clients=total_clients,
        total_projects=total_projects,
        active_projects=active_projects,
        total_users=total_users,
        present_today=present_today,
        late_checkins=late_checkins,
        pending_leaves=pending_leaves,
        new_leads_this_month=new_leads_this_month,
        leads_proposal=leads_proposal,
        leads_processing=leads_processing,
        leads_converted=leads_converted,
        completed_projects=completed_projects,
    )


@api.get('/dashboard/charts', response=DashboardCharts)
def get_dashboard_charts(request):
    from main.models import Lead
    from datetime import date
    from django.db.models import Count
    from django.db.models.functions import TruncMonth

    today = date.today()

    def month_start(n_months_back):
        total = today.year * 12 + today.month - 1 - n_months_back
        return date(total // 12, total % 12 + 1, 1)

    start = month_start(5)
    monthly_qs = (
        Lead.objects
        .filter(created_at__date__gte=start)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    month_map = {row['month'].strftime('%Y-%m'): row['count'] for row in monthly_qs}
    leads_by_month = []
    for i in range(5, -1, -1):
        d = month_start(i)
        leads_by_month.append(MonthlyLeadPoint(
            month=d.strftime('%b %Y'),
            count=month_map.get(d.strftime('%Y-%m'), 0),
        ))

    STATUS_LABELS = {
        'proposal':       'Proposal',
        'sent':           'Sent',
        'processing':     'Processing',
        'client':         'Client',
        'lost':           'Lost',
        'not_interested': 'Not Interested',
    }
    status_qs = (
        Lead.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )
    leads_by_status = [
        LeadStatusPoint(
            status=row['status'],
            label=STATUS_LABELS.get(row['status'], row['status'].title()),
            count=row['count'],
        )
        for row in status_qs
        if row['count'] > 0
    ]

    from main.models.project import Project
    all_statuses = ['Planning', 'Progress', 'Testing', 'Completed', 'On Hold']
    proj_qs = {
        row['status']: row['count']
        for row in Project.objects.values('status').annotate(count=Count('id'))
    }
    projects_by_status = [
        ProjectStatusPoint(status=s, count=proj_qs.get(s, 0))
        for s in all_statuses
    ]

    return DashboardCharts(
        leads_by_month=leads_by_month,
        leads_by_status=leads_by_status,
        projects_by_status=projects_by_status,
    )


@api.get('/dashboard/dev-stats', response=DevStats)
def get_dev_stats(request):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    from main.models.project import Project
    user_projects = Project.objects.filter(team_members=request.user)
    return DevStats(
        my_active=user_projects.filter(status__in=['Planning', 'Progress', 'Testing']).count(),
        my_completed=user_projects.filter(status='Completed').count(),
        my_total=user_projects.count(),
        my_on_hold=user_projects.filter(status='On Hold').count(),
    )


@api.get('/dashboard/dev-charts', response=DevCharts)
def get_dev_charts(request):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    from main.models.project import Project
    from django.db.models import Count
    all_statuses = ['Planning', 'Progress', 'Testing', 'Completed', 'On Hold']
    proj_qs = {
        row['status']: row['count']
        for row in Project.objects.filter(team_members=request.user).values('status').annotate(count=Count('id'))
    }
    return DevCharts(
        projects_by_status=[
            ProjectStatusPoint(status=s, count=proj_qs.get(s, 0))
            for s in all_statuses
        ]
    )
