# --------------------------------------------------------------------------
# Scheduling을 위한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import zmq
import json
import logging
import datetime

from django.conf import settings
from django.db.models import Q

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger

from apps.attendance.models import Attendance, AttendanceType

logger = logging.getLogger("django")


def send_mail(to: str, subject: str, template: str, args: str, service_name: str):
    """zmq를 통해 메일을 발송합니다.

    :param to: 메일을 받을 사람의 이메일 주소입니다.
    :param subject: 메일 제목입니다.
    :param template: 메일 내용입니다.
    :param args: 메일 내용에 들어갈 인자입니다.
    :param service_name: 메일을 발송하는 서비스의 이름입니다.
    :return: None
    """
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect(f"tcp://{settings.ZMQ_HOST}:{settings.ZMQ_PORT}")

    message = {
        "to": to,
        "subject": subject,
        "template": template,
        "arg": args,
        "who": service_name,
    }
    request = json.dumps(
        message,
        default=lambda o: o.__dict__,
        sort_keys=True,
        indent=4,
        ensure_ascii=False,
    )
    zmq_socket.send_json(request)


def update_attendance_type_apr():
    """AttendanceType이 UNA인 Attendance의 AttendanceType를 APR로 업데이트하는 JOB입니다."""
    today = datetime.date.today()

    # AttendanceType을 UNA에서 APR로 변경
    una_type = AttendanceType.objects.get(name="UNA")
    apr_type = AttendanceType.objects.get(name="APR")

    # start_date_time이 오늘이면서 AttendanceType이 UNA인 Attendance를 찾아서 APR로 업데이트
    Attendance.objects.filter(
        time_table__start_date_time__date=today, attendance_type=una_type
    ).update(attendance_type=apr_type)


def update_absent_attendance_info():
    """출결 기한이 만료된 경우, ACK로 출석을 하지 않은 유저들의 출석 정보를 ABS로 업데이트하는 JOB입니다."""
    today = datetime.date.today()

    # AttendanceType을 UNA, APR, ABS로 조회
    una_type = AttendanceType.objects.get(name="UNA")
    apr_type = AttendanceType.objects.get(name="APR")
    abs_type = AttendanceType.objects.get(name="ABS")

    # 생성된 Attendance 중에서(UNA 혹은 APR인) 기한이 지난 TimeTable를 가진 Attendance를 찾아서 ABS로 업데이트
    expired_attendances = Attendance.objects.filter(
        Q(attendance_type=una_type) | Q(attendance_type=apr_type),
        time_table__end_date_time__lt=today,
    )
    expired_attendances.update(attendance_type=abs_type)


def start():
    """APScheduler로 JOB을 등록, 실행하는 함수입니다."""
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    cron_trigger = CronTrigger(hour=4, minute=0)  # 매일 새벽 4시에 실행

    scheduler.add_job(
        update_attendance_type_apr,
        cron_trigger,
        id="update_attendance_type_apr",
        replace_existing=True,
    )
    logger.info("Added job 'update_attendance_type_apr'.")

    scheduler.add_job(
        update_absent_attendance_info,
        cron_trigger,
        id="update_absent_attendance_info",
        replace_existing=True,
    )
    logger.info("Added job 'update_absent_attendance_info'.")

    try:
        logger.info("Starting scheduler...")
        scheduler.start()

    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
