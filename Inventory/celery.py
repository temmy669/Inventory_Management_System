from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab 

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Inventory.settings')

app = Celery('Inventory')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Define the schedule for periodic tasks
app.conf.beat_schedule = {
    'generate-report-every-day': {
        'task': 'your_app_name.tasks.generate_supplier_performance_report',  # Update with your app name
        'schedule': crontab(hour=0, minute=0),  # Runs daily at midnight
    },
}
