import os

from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        if settings.SCHEDULER_DEFAULT and os.environ.get("RUN_MAIN") == "true":
            from core import scheduler

            scheduler.start()
