import os

from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detoxa_backend.settings')

app = Celery('detoxa_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'new_appointments_report': {
        'task': 'detoxa_services.tasks.appointmentsreport.new_appointments_report',
        # 'schedule': 10,
        'schedule': crontab(hour=22, minute=30,day_of_week='*'),
    },
    'new_registration_report': {
        'task': 'detoxa_services.tasks.newregistrationreport.new_registration_report',
        'schedule': crontab(hour=22, minute=45, day_of_week='*'),
        # 'schedule': crontab(minute=11, hour='*/13'),
        # 'schedule': crontab(second=5),crontab(minute=0, hour='*/6')
        # 'schedule': 10,
        # 'args': (3, 4)
    },
    'new_tests_report': {
        'task': 'detoxa_services.tasks.testconductedreport.new_tests_report',
        'schedule': crontab(hour=23, minute=00,day_of_week='*'),
        # 'schedule': 10,
    }
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')