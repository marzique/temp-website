import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temp.settings.production')

app = Celery('temp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


TASK_SERIALIZER = 'json'
ACCEPT_CONTENT = ['json']

app.conf.update(

    CELERY_TIMEZONE=settings.TIME_ZONE,
    CELERY_ALWAYS_EAGER=False,
    CELERY_ENABLE_UTC=False,

    CELERYBEAT_SCHEDULE={
        # hour=0, minute=0 - once a day
        # minute=0 - once per hour

        "notify_birthdays": {
            "task": "squad.tasks.notify_birthdays",
            "schedule": crontab(hour=0, minute=0),
            "args": ()
        },
        # "TODO": {
        #     "task": "squad.tasks.TODO",
        #     "schedule": crontab(hour=18, minute=0), # -2 to UTC
        #     "args": ()
        # },
    },
)
