import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# Где находятся настройки джанго
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
# Win7 problem. Использовать при ValueError при обработке worker'ом

app = Celery('movies', broker=settings.BROKER_URL)
# Чтобы celery спарсил настройки из settings через CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-email-every-midnight': {
        'task': 'contact.tasks.send_beat_email',
        'schedule': crontab(minute=0, hour=0),
    },
}
