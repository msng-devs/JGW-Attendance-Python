from django.db import models

from apps.common.models import BaseEntity, Member
from apps.timetable.models import TimeTable


class AttendanceType(BaseEntity):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = "attendance_type"
        verbose_name = "Attendance Type"
        verbose_name_plural = "Attendance Types"


class Attendance(BaseEntity):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="attendances"
    )
    time_table = models.ForeignKey(
        TimeTable, on_delete=models.CASCADE, related_name="attendances"
    )
    attendance_type = models.ForeignKey(
        AttendanceType, on_delete=models.CASCADE, related_name="attendances"
    )
    index = models.TextField()

    class Meta:
        db_table = "attendance"
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"

    def update(self, attendance):
        if attendance.attendance_type:
            self.attendance_type = attendance.attendance_type
        self.index = attendance.index
        self.modified_by = attendance.modified_by
        self.save()


class AttendanceCode(models.Model):
    code = models.CharField(max_length=255)
    time_table = models.ForeignKey(
        TimeTable, on_delete=models.CASCADE, related_name="attendance_codes"
    )
    expire_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [["code", "time_table"]]
        verbose_name = "Attendance Code"
        verbose_name_plural = "Attendance Codes"
