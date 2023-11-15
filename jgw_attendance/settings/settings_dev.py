# flake8: noqa: F403, F405
# --------------------------------------------------------------------------
# Dev용 settings 파일입니다.
#
# 이 파일은 로컬에서 개발할 때 사용합니다.
# 테스트케이스 실행 및 테스트 서버 실행 시, 다음 명령어로 이 세팅을 적용할 수 있습니다.
#  - python manage.py <명령어> --settings=jgw_attendance.settings.settings_dev
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "JGWAttendanceDBdev",
        "USER": "bnbong",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

ZMQ_HOST = "127.0.0.1"
ZMQ_PORT = "5555"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

TESTING_MODE = True
