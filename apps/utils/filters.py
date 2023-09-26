# --------------------------------------------------------------------------
# 쿼리파라미터를 통한 필터링을 구현하기 위한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from django_filters import rest_framework as filters

from apps.timetable.models import TimeTable
from apps.event.models import Event
from apps.attendance.models import AttendanceType, Attendance


class BaseFilterSet(filters.FilterSet):
    """각 필터들의 부모 클래스입니다.

    이 클래스를 상속받아 각 모델에 맞는 필터를 구현합니다.
    """

    # Equal Query Options
    createdBy = filters.CharFilter(field_name="created_by")
    modifiedBy = filters.CharFilter(field_name="modified_by")

    # Range Query Options
    startCreatedDateTime = filters.DateTimeFilter(
        field_name="created_date_time", lookup_expr="gte"
    )
    endCreatedDateTime = filters.DateTimeFilter(
        field_name="created_date_time", lookup_expr="lte"
    )
    startModifiedDateTime = filters.DateTimeFilter(
        field_name="modified_date_time", lookup_expr="gte"
    )
    endModifiedDateTime = filters.DateTimeFilter(
        field_name="modified_date_time", lookup_expr="lte"
    )

    class Meta:
        abstract = True


class TimeTableFilter(BaseFilterSet):
    # Equal Query Options
    eventID = filters.NumberFilter(field_name="event")

    # Range Query Options
    startDateTime = filters.DateTimeFilter(
        field_name="start_date_time", lookup_expr="gte"
    )
    endDateTime = filters.DateTimeFilter(field_name="end_date_time", lookup_expr="lte")

    # Like Query Options
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = TimeTable
        fields = [
            "eventID",
            "createdBy",
            "modifiedBy",
            "startCreatedDateTime",
            "endCreatedDateTime",
            "startModifiedDateTime",
            "endModifiedDateTime",
            "startDateTime",
            "endDateTime",
            "name",
        ]


class EventFilter(BaseFilterSet):
    # Range Query Options
    startDateTime = filters.DateTimeFilter(
        field_name="start_date_time", lookup_expr="gte"
    )
    endDateTime = filters.DateTimeFilter(field_name="end_date_time", lookup_expr="lte")

    # Like Query Options
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    index = filters.CharFilter(field_name="index", lookup_expr="icontains")

    class Meta:
        model = Event
        fields = [
            "createdBy",
            "modifiedBy",
            "startCreatedDateTime",
            "endCreatedDateTime",
            "startModifiedDateTime",
            "endModifiedDateTime",
            "startDateTime",
            "endDateTime",
            "name",
            "index",
        ]


class AttendanceTypeFilter(BaseFilterSet):
    # Like Query Options
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = AttendanceType
        fields = [
            "createdBy",
            "modifiedBy",
            "startCreatedDateTime",
            "endCreatedDateTime",
            "startModifiedDateTime",
            "endModifiedDateTime",
            "name",
        ]


class AttendanceFilter(BaseFilterSet):
    # Equal Query Options
    attendanceTypeID = filters.NumberFilter(field_name="attendance_type_id")
    memberID = filters.CharFilter(field_name="member_id")
    timeTableID = filters.NumberFilter(field_name="time_table_id")

    # Like Query Options
    index = filters.CharFilter(field_name="index", lookup_expr="icontains")

    class Meta:
        model = Attendance
        fields = [
            "createdBy",
            "modifiedBy",
            "startCreatedDateTime",
            "endCreatedDateTime",
            "startModifiedDateTime",
            "endModifiedDateTime",
            "attendanceTypeID",
            "memberID",
            "timeTableID",
            "index",
        ]
