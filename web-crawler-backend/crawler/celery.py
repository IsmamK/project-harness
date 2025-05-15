import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawler.settings')

app = Celery('crawler')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Explicitly specify where to look for tasks
app.autodiscover_tasks(['api'])