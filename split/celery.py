# celery.py in your project directory
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'split.settings')

app = Celery('split')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weekly_reminders': {
        'task': 'your_app.tasks.send_weekly_reminders',
        'schedule': crontab(day_of_week='sunday', hour=12, minute=0),  
    },
}