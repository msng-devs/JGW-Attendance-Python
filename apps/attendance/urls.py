from . import views

from django.urls import path

urlpatterns = [
    # Read operation
    path(
        "attendancetype/", views.GetAttendanceType.as_view(), name="get_attendance_type"
    ),
    # Create, Read operations for all attendance
    path("", views.AttendanceListCreate.as_view(), name="attendance_list_create"),
    # Read, Delete, Update operations for a specific attendance
    path(
        "<int:attendance_id>/",
        views.AttendanceDetail.as_view(),
        name="attendance_detail",
    ),
]
