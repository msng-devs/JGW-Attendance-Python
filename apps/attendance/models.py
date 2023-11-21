# --------------------------------------------------------------------------
# Attendance Application의 Models를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from django.db import models

from apps.common.models import Member
from apps.timetable.models import TimeTable


class AttendanceType(models.Model):
    id = models.AutoField(primary_key=True, db_column="ATTENDANCE_TYPE_PK")
    name = models.CharField(
        max_length=45, unique=True, db_column="ATTENDANCE_TYPE_NAME"
    )

    class Meta:
        db_table = "ATTENDANCE_TYPE"
        verbose_name = "Attendance Type"
        verbose_name_plural = "Attendance Types"


class Attendance(models.Model):
    id = models.AutoField(primary_key=True, db_column="ATTENDANCE_PK")
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="attendances",
        db_column="MEMBER_MEMBER_PK",
    )
    time_table = models.ForeignKey(
        TimeTable,
        on_delete=models.CASCADE,
        related_name="attendances",
        db_column="TIMETABLE_TIMETABLE_PK",
    )
    attendance_type = models.ForeignKey(
        AttendanceType,
        on_delete=models.CASCADE,
        related_name="attendances",
        db_column="ATTENDANCE_TYPE_ATTENDANCE_TYPE_PK",
    )
    modified_datetime = models.DateTimeField(
        auto_now=True,
        verbose_name="Modified Date Time",
        db_column="ATTENDANCE_MODIFIED_DTTM",
    )
    created_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created Date Time",
        db_column="ATTENDANCE_CREATED_DTTM",
    )
    index = models.TextField(null=True, blank=True, db_column="ATTENDANCE_INDEX")
    created_by = models.CharField(
        max_length=30,
        verbose_name="Created By",
        default="system",
        db_column="ATTENDANCE_CREATED_BY",
    )
    modified_by = models.CharField(
        max_length=30,
        verbose_name="Modified By",
        default="system",
        db_column="ATTENDANCE_MODIFIED_BY",
    )

    class Meta:
        db_table = "ATTENDANCE"
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"

    def update(self, attendance):
        if attendance.attendance_type:
            self.attendance_type = attendance.attendance_type
        self.index = attendance.index
        self.modified_by = attendance.modified_by
        self.save()


class AttendanceCode(models.Model):
    code = models.CharField(max_length=255, db_column="CODE")
    time_table = models.ForeignKey(
        TimeTable,
        on_delete=models.CASCADE,
        related_name="attendance_codes",
        db_column="TIMETABLE_TIMETABLE_PK",
    )
    expire_at = models.DateTimeField(null=True, blank=True, db_column="EXPIRE_AT")

    class Meta:
        db_table = "ATTENDANCE_CODE"
        unique_together = [["code", "time_table"]]
        verbose_name = "Attendance Code"
        verbose_name_plural = "Attendance Codes"
