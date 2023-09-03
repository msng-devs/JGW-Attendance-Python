from . import views

from django.urls import path

urlpatterns = [
    # Create operation
    path("attendance/add/", views.AddAttendance.as_view(), name="add_attendance"),
    # Read operation
    path(
        "attendanceType/", views.GetAttendanceType.as_view(), name="get_attendance_type"
    ),
    # Read operations for all attendance
    path("attendance/", views.AttendanceList.as_view(), name="attendance_list"),
    # Read, Delete, Update operations for a specific attendance
    path(
        "attendance/<int:attendanceId>/",
        views.AttendanceDetail.as_view(),
        name="attendance_detail",
    ),
]
