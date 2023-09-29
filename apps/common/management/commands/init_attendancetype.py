from django.core.management.base import BaseCommand
from apps.attendance.models import AttendanceType


class Command(BaseCommand):
    """
    AttendanceType Initializer 코드입니다.

    다음 명령어로 실행할 수 있습니다:
        python manage.py init_attendancetype
    """

    def handle(self, *args, **options):
        attendancetypes = [
            "UNA",  # Unapproved, 미결
            "APR",  # Approved, 출결
            "ABS",  # Absent, 결석
            "ACK",  # Acknowledged, 출석 인정
        ]

        for attendancetype in attendancetypes:
            AttendanceType.objects.get_or_create(name=attendancetype)

        self.stdout.write(
            self.style.SUCCESS("AttendanceType initialized successfully.")
        )
