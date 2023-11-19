# --------------------------------------------------------------------------
# TimeTable Application의 Models를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from django.db import models

from apps.common.models import BaseEntity
from apps.event.models import Event


class TimeTable(BaseEntity):
    name = models.CharField(max_length=50, verbose_name="Time Table Name")
    index = models.TextField(max_length=200, verbose_name="Time Table Index")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name="Related Event"
    )
    start_date_time = models.DateTimeField(verbose_name="Time Table Start DateTime")
    end_date_time = models.DateTimeField(verbose_name="Time Table End DateTime")

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
