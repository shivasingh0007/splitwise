# celery.py in your project directory
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from kombu import Exchange, Queue

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# settings.py or celery.py
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (Queue('default', Exchange('default'), routing_key='default'),)

CELERY_IMPORTS = ('splitapp.tasks',)  # Add your task modules here



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'split.settings')

app = Celery('split')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send_weekly_reminders': {
        'task': 'splitapp.tasks.send_weekly_reminders',
        'schedule': crontab(day_of_week='sunday', hour=12, minute=0),  
    },
}




