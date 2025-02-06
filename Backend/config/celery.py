from celery import Celery
from celery.schedules import crontab

app = Celery('config')

app.conf.beat_schedule = {
    'generate-daily-insights': {
        'task': 'apps.ai_insights.tasks.generate_periodic_insights',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
} 