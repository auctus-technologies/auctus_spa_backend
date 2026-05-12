from ninja import Schema
from typing import Optional, List
from datetime import date, datetime


class ProjectAttachmentSchema(Schema):
    id: int
    file_name: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    uploaded_by: Optional[str] = None
    uploaded_at: datetime


class TeamMemberDetailSchema(Schema):
    id: int
    name: str
    designation: Optional[str] = None
    avatar_url: Optional[str] = None


class ProjectSchema(Schema):
    id: int
    name: str
    client_id: int
    client_name: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    team_members: List[int] = []
    team_member_names: List[str] = []
    team_member_details: List[TeamMemberDetailSchema] = []
    start_date: date
    end_date: date
    status: str
    attachments: List[ProjectAttachmentSchema] = []
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProjectCreateSchema(Schema):
    name: str
    client_id: int
    description: Optional[str] = None
    requirements: Optional[str] = None
    team_members: List[int] = []
    start_date: date
    end_date: date
    status: str = 'Planning'


class ProjectUpdateSchema(Schema):
    name: Optional[str] = None
    client_id: Optional[int] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    team_members: Optional[List[int]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None


class ProjectListResponse(Schema):
    projects: List[ProjectSchema]
    total: int
    page: int
    page_size: int
    total_pages: int


class TeamMemberSchema(Schema):
    id: int
    name: str
    email: str
    designation: Optional[str] = None


class ClientListResponse(Schema):
    id: int
    name: str
    email: str
    company: Optional[str] = None


class TeamMembersResponse(Schema):
    members: List[TeamMemberSchema]
