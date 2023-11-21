# --------------------------------------------------------------------------
# TimeTable Application의 Models를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from django.db import models

from apps.event.models import Event


class TimeTable(models.Model):
    id = models.AutoField(primary_key=True, db_column="TIMETABLE_PK")
    name = models.CharField(
        max_length=50, db_column="TIMETABLE_NM", verbose_name="Time Table Name"
    )
    index = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_column="TIMETABLE_INDEX",
        verbose_name="Time Table Index",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        db_column="EVENT_EVENT_PK",
        verbose_name="Related Event",
    )
    start_date_time = models.DateTimeField(
        db_column="TIMETABLE_START_DTTM", verbose_name="Time Table Start DateTime"
    )
    end_date_time = models.DateTimeField(
        db_column="TIMETABLE_END_DTTM", verbose_name="Time Table End DateTime"
    )
    created_by = models.CharField(
        max_length=30,
        db_column="TIMETABLE_CREATED_BY",
        verbose_name="Created By",
        default="system",
    )
    modified_by = models.CharField(
        max_length=30,
        db_column="TIMETABLE_MODIFIED_BY",
        verbose_name="Modified By",
        default="system",
    )
    created_datetime = models.DateTimeField(
        auto_now_add=True,
        db_column="TIMETABLE_CREATED_DTTM",
        verbose_name="Created Date Time",
    )
    modified_datetime = models.DateTimeField(
        auto_now=True,
        db_column="TIMETABLE_MODIFIED_DTTM",
        verbose_name="Modified Date Time",
    )

    class TimeTableDateTimesManager(models.Manager):
        def get_max_start_datetime(self):
            return self.aggregate(models.Max("start_date_time"))["start_date_time__max"]

        def get_min_start_datetime(self):
            return self.aggregate(models.Min("start_date_time"))["start_date_time__min"]

        def get_max_end_datetime(self):
            return self.aggregate(models.Max("end_date_time"))["end_date_time__max"]

        def get_min_end_datetime(self):
            return self.aggregate(models.Min("end_date_time"))["end_date_time__min"]

    objects = TimeTableDateTimesManager()

    class Meta:
        db_table = "TIMETABLE"
        verbose_name = "Time Table"
        verbose_name_plural = "Time Tables"

    def validation_datetime(self):
        return (self.start_date_time >= self.event.start_date_time) and (
            self.end_date_time <= self.event.end_date_time
        )

    def update(self, new_time_table):
        self.index = new_time_table.index
        self.name = new_time_table.name
        self.start_date_time = new_time_table.start_datetime
        self.end_date_time = new_time_table.end_datetime
        self.modified_by = new_time_table.modified_by
        self.save()
