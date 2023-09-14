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

ZMQ_HOST = os.getenv("ZMQ_HOST")
ZMQ_PORT = os.getenv("ZMQ_PORT")
