import datetime
from celery import shared_task
from .models import RedirectedURL
from django.contrib.sessions.models import Session


# Задача очистки старых редиректов
@shared_task
def clean_task():
    RedirectedURL.objects.all().exclude(user__in=Session.objects.all().values_list('session_key', flat=True)).delete()

def clean_redirects_by_session_id(session_key):
    """
    Метод очистки старых редиректов уже несуществующей сессии
    """
    RedirectedURL.objects.filter(user=session_key).delete()
