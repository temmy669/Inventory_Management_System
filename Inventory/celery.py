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

# schedule for periodic tasks
from celery.schedules import crontab

# Define the schedule for periodic tasks
app.conf.beat_schedule = {
    'generate-report-every-week': {
        'task': 'inventoryapp.tasks.generate_supplier_performance_report',  # Update with your app name
        'schedule': crontab(hour=0, minute=0, day_of_week='monday'),  # Runs every Monday at midnight
    },
}
