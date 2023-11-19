# --------------------------------------------------------------------------
# Event Application의 Models를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from django.db import models
from apps.common.models import BaseEntity


class Event(BaseEntity):
    name = models.CharField(max_length=50, null=False, verbose_name="Event Name")
    index = models.TextField(verbose_name="Event Index")
    start_date_time = models.DateTimeField(verbose_name="Event Start DateTime")
    end_date_time = models.DateTimeField(verbose_name="Event End DateTime")

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
