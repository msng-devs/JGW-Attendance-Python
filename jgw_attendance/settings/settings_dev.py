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

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
