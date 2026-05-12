from ninja import Schema
from datetime import datetime, date
from typing import Optional, List


class HealthResponse(Schema):
    status: str
    message: str
    timestamp: str


class DashboardStats(Schema):
    total_leads: int
    total_clients: int
    total_projects: int = 0
    active_projects: int
    total_users: int
    present_today: int = 0
    late_checkins: int = 0
    pending_leaves: int = 0
    new_leads_this_month: int = 0
    leads_proposal: int = 0
    leads_processing: int = 0
    leads_converted: int = 0
    completed_projects: int = 0


class MonthlyLeadPoint(Schema):
    month: str
    count: int


class LeadStatusPoint(Schema):
    status: str
    label: str
    count: int


class ProjectStatusPoint(Schema):
    status: str
    count: int


class DashboardCharts(Schema):
    leads_by_month: List[MonthlyLeadPoint]
    leads_by_status: List[LeadStatusPoint]
    projects_by_status: List[ProjectStatusPoint]


class DevStats(Schema):
    my_active: int
    my_completed: int
    my_total: int
    my_on_hold: int


class DevCharts(Schema):
    projects_by_status: List[ProjectStatusPoint]


class LeadSchema(Schema):
    id: int
    name: str
    email: str
    phone: str | None = None
    status: str = "new"
    created_at: datetime


class LeadCreateSchema(Schema):
    name: str
    email: str
    phone: str | None = None
    status: str = "new"




class ProjectSchema(Schema):
    id: int
    name: str
    client_id: int
    status: str = "active"
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectCreateSchema(Schema):
    name: str
    client_id: int
    status: str = "active"
