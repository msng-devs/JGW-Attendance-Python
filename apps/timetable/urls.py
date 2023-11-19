from . import views

from django.urls import path

urlpatterns = [
    # Create operation
    path(
        "<int:timetable_id>/attendanceCode/register/",
        views.RegisterAttendanceCode.as_view(),
        name="attendance_code_register",
    ),
    # Create, Read operations for all timetables
    path("", views.TimeTableListCreate.as_view(), name="timetable_list_create"),
    # Read, Delete, Update operations for a specific timetable
    path(
        "<int:timetable_id>/",
        views.TimeTableDetail.as_view(),
        name="timetable_detail",
    ),
    path(
        "<int:timetable_id>/attendanceCode/",
        views.AttendanceCodeDetail.as_view(),
        name="attendance_code_detail",
    ),
]
