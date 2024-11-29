from zibal_project import settings
from zibal_project import celeryconfig
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zibal_project.settings')
app = Celery('zibal_project')
app.config_from_object(celeryconfig)
app.config_from_object('zibal_project.schedule_tasks_config')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)