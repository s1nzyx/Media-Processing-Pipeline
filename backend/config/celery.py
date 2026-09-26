import os
from celery import Celery
#указываем джанго настройки по умолчанию для celery команд
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('media_pipeline')
#читаем конфиг из сеттингс.пу, все настройки celery должны начинаться с CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')
#автоматически находим задачи в зарег приложениях джанго
app.autodiscover_tasks()