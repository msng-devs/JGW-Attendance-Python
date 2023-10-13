# TODO: 출결 기한이 만료된 경우, ACK로 출석을 하지 않은 유저들의 출석 정보를 ABS로 업데이트.
# TODO: 기한이 만료된 출석 정보를 업데이트하는 로직 작성.
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

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger

from apps.timetable.models import TimeTable
from apps.attendance.models import AttendanceType, Attendance
from apps.event.models import Event

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


def delete_expired_event():
    """기한이 만료된 Event를 삭제하는 JOB입니다."""
    # today = datetime.date.today()
    pass


def delete_expired_timetable():
    """기한이 만료된 TimeTable을 삭제하는 JOB입니다."""
    today = datetime.date.today()

    TimeTables = TimeTable.objects.all()

    for timetable in TimeTables:
        if timetable.end_date_time.date() < today:
            timetable.delete()


def update_absent_attendance_info():
    """출결 기한이 만료된 경우, ACK로 출석을 하지 않은 유저들의 출석 정보를 ABS로 업데이트하는 JOB입니다."""
    pass


def start():
    """APScheduler로 JOB을 등록, 실행하는 함수입니다."""
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    cron_trigger = CronTrigger(hour=4, minute=0)  # 매일 새벽 4시에 실행

    scheduler.add_job(
        delete_expired_event,
        cron_trigger,
        id="delete_expired_event",
        replace_existing=True,
    )
    logger.info("Added job 'delete_expired_event'.")

    scheduler.add_job(
        delete_expired_timetable,
        cron_trigger,
        id="delete_expired_timetable",
        replace_existing=True,
    )
    logger.info("Added job 'delete_expired_timetable'.")

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
