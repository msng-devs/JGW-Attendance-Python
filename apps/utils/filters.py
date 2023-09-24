from django_filters import rest_framework as filters

from apps.timetable.models import TimeTable


class TimeTableFilter(filters.FilterSet):
    # Equal Query Options
    eventID = filters.NumberFilter(field_name="event")
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
