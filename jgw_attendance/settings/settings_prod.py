# flake8: noqa: F403, F405
# --------------------------------------------------------------------------
# Production용 settings 파일입니다.
#
# 이 파일은 실제 서비스를 운영할 때 사용합니다.
# 실제 서비스를 운영할 때는 이 파일을 사용하고, 로컬에서 개발할 때는 settings_dev.py를 사용합니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
# from .base import *

# DEBUG = True

# ALLOWED_HOSTS = []

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "JGWAttendanceDBdev",
#         "USER": "bnbong",
#         "PASSWORD": "password",
#         "HOST": "localhost",
#         "PORT": "3306",
#     }
# }

# ZMQ_HOST = "your_host_here"
# ZMQ_PORT = "your_port_here"

TESTING_MODE = False
