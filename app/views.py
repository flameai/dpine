from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from app.models import RedirectedURL
from rest_framework import serializers, permissions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import authentication, exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated, AllowAny
from threading import Lock
import redis
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.core.validators import slug_re
from app.tasks import clean_redirects_by_session_id

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


class SessionAuth(authentication.BaseAuthentication):
    def authenticate(self, request):        
        if not request.session.session_key:
            # сессии не создано, попробуем создать
            request.session.create()
            if not request.session.session_key:
                # что-то пошло не так, вызовем исключение
                raise exceptions.AuthenticationFailed(_('Проблема с созданием куки.'))
            # вдруг вы тот самый удачливый человек, что получил ключ сессии умершего только что пользователя ))
            # очистим редиректы чтобы не получить наследства
            clean_redirects_by_session_id(request.session.session_key)
        return (request.session.session_key, None)


class RURLSerializer(serializers.ModelSerializer):
    """
    Redirected URL Serializer
    """    
    class Meta:
        model = RedirectedURL
        fields = ['subpart', 'dest_url', 'dt', 'user']
        read_only_fields = ['dt', 'user']        
    
    def to_internal_value(self, data):
        if not bool(data.get('subpart')):
            self.context.update({"create_subpart": True})
            data.update({'subpart': 'corRect_s1ugField'})
        return super().to_internal_value(data)
    
    
    def create(self, data):
        data["user"] = self.context["user"]
        if "create_subpart" in self.context:
            lock = Lock()
            with lock:
                data.update({"subpart": RedirectedURL.create_subpart()})
                return super().create(data)
        return super().create(data)


class RedirectedURLViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    """
    Viewset for redirections
    """
    queryset = RedirectedURL.objects.all()
    serializer_class = RURLSerializer
    authentication_classes = [SessionAuth, ]
    permission_classes_by_action = {'create': [IsAuthenticated, ],
                                    'list': [IsAuthenticated,],
                                    'retrieve': [AllowAny,],
                                    }
    lookup_field = 'subpart'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-dt')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context
    
    def retrieve(self, request, subpart):
        """
        Метод редиректа
        """
        value = redis_instance.get(subpart)
        if not value:
            return HttpResponseNotFound()
        url = value.decode()
        return HttpResponseRedirect(redirect_to=url)

def render_main_page(request):
    return render(request, 'index.html',)