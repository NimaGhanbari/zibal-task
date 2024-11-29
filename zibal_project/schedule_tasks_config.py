from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-notification-every-night': {
        'task': 'apps.notifications.tasks.send_notification_task',
        'schedule': crontab(minute="0", hour="0"),
    },
}
