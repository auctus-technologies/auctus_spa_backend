# API Router initialization
from ninja import NinjaAPI

api = NinjaAPI(title="Auctus API", version="1.0.0")

# Import and register all API modules
from . import user_api
from . import core_api
from . import employee_api
from . import attendance_api
from . import client_api
from . import project_api
from . import opening_api
from . import leave_api
from . import holiday_api
from . import lead_api
from . import follow_up_api
from . import task_api
from . import notification_api
from . import application_api
from . import salary_api

__all__ = ["api"]
