from django.shortcuts import get_object_or_404
from . import api
from main.models import Holiday
from .schemas.holiday_schemas import HolidaySchema, HolidayCreateSchema, HolidayUpdateSchema, HolidayListResponse


def _to_schema(h: Holiday) -> HolidaySchema:
    return HolidaySchema(id=h.id, name=h.name, date=h.date, created_at=h.created_at)


@api.get("/holidays", response=HolidayListResponse)
def list_holidays(request):
    if not request.user.is_authenticated:
        return api.create_response(request, {"error": "Not authenticated"}, status=401)
    holidays = Holiday.objects.all()
    return HolidayListResponse(
        holidays=[_to_schema(h) for h in holidays],
        total=holidays.count(),
    )


@api.post("/holidays", response=HolidaySchema)
def create_holiday(request, data: HolidayCreateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {"error": "Not authenticated"}, status=401)
    holiday = Holiday.objects.create(name=data.name, date=data.date)
    return _to_schema(holiday)


@api.put("/holidays/{holiday_id}", response=HolidaySchema)
def update_holiday(request, holiday_id: int, data: HolidayUpdateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {"error": "Not authenticated"}, status=401)
    holiday = get_object_or_404(Holiday, id=holiday_id)
    if data.name is not None:
        holiday.name = data.name
    if data.date is not None:
        holiday.date = data.date
    holiday.save()
    return _to_schema(holiday)


@api.delete("/holidays/{holiday_id}")
def delete_holiday(request, holiday_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {"error": "Not authenticated"}, status=401)
    holiday = get_object_or_404(Holiday, id=holiday_id)
    holiday.delete()
    return {"success": True}
