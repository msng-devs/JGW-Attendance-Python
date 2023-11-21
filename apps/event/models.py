# --------------------------------------------------------------------------
# Event Application의 Models를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from django.db import models


class Event(models.Model):
    id = models.AutoField(primary_key=True, db_column="EVENT_PK")
    name = models.CharField(
        max_length=50, null=False, db_column="EVENT_NM", verbose_name="Event Name"
    )
    index = models.TextField(
        null=True, blank=True, db_column="EVENT_INDEX", verbose_name="Event Index"
    )
    start_date_time = models.DateTimeField(
        db_column="EVENT_START_DTTM", verbose_name="Event Start DateTime"
    )
    end_date_time = models.DateTimeField(
        db_column="EVENT_END_DTTM", verbose_name="Event End DateTime"
    )
    created_by = models.CharField(
        max_length=30,
        verbose_name="Created By",
        default="system",
        db_column="EVENT_CREATED_BY",
    )
    modified_by = models.CharField(
        max_length=30,
        verbose_name="Modified By",
        default="system",
        db_column="EVENT_MODIFIED_BY",
    )
    created_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created Date Time",
        db_column="EVENT_CREATED_DTTM",
    )
    modified_datetime = models.DateTimeField(
        auto_now=True,
        verbose_name="Modified Date Time",
        db_column="EVENT_MODIFIED_DTTM",
    )

    class Meta:
        db_table = "EVENT"
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def update(self, new_event):
        self.name = new_event.name
        self.index = new_event.index
        self.modified_by = new_event.modified_by
        self.start_date_time = new_event.start_datetime
        self.end_date_time = new_event.end_datetime
        self.save()
