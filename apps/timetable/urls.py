from . import views

from django.urls import path

urlpatterns = [
    # Create operation
    path("add/", views.AddTimeTable.as_view(), name="add_timetable"),
    path(
        "<int:timetableId>/attendanceCode/register/",
        views.RegisterAttendanceCode.as_view(),
        name="attendance_code_register",
    ),
    # Read operations for all timetables
    path("", views.TimeTableList.as_view(), name="timetable_list"),
    # Read, Delete, Update operations for a specific timetable
    path(
        "<int:timetableId>/",
        views.TimeTableDetail.as_view(),
        name="timetable_detail",
    ),
    path(
        "<int:timetableId>/attendanceCode/",
        views.AttendanceCodeDetail.as_view(),
        name="attendance_code_detail",
    ),
]
