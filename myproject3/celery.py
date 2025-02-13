from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject3.settings')

app = Celery('myproject3')

# Load task modules from all registered Django apps.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
