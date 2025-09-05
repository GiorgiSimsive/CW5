import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    "send_reminders_every_minute": {
        "task": "telegram_bot.tasks.send_reminders",
        "schedule": crontab(minute="*"),
    },
}
