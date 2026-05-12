# Import all models so Django can discover them
from .user import User
from .employee_profile import EmployeeProfile
from .bank_details import BankDetails
from .attendance import Attendance
from .address import Address
from .client import Client
from .project import Project, ProjectAttachment
from .opening import JobOpening
from .application import JobApplication
from .leave_request import LeaveRequest, LeaveDocument
from .holiday import Holiday
from .lead import Lead
from .lead_follow_up import LeadFollowUp
from .task import Task
from .notification import Notification
from .salary import Salary

__all__ = [
    "User",
    "EmployeeProfile",
    "BankDetails",
    "Attendance",
    "Address",
    "Client",
    "Project",
    "ProjectAttachment",
    "JobOpening",
    "JobApplication",
    "LeaveRequest",
    "LeaveDocument",
    "Holiday",
    "Lead",
    "LeadFollowUp",
    "Task",
    "Notification",
    "Salary",
]
