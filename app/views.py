from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from app.models import RedirectedURL
from rest_framework import serializers, permissions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import authentication, exceptions
from django.utils.translation import gettext_lazy as _


class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
        

class SessionAuth(authentication.BaseAuthentication):
    def authenticate(self, request):        
        if not request.session.session_key:
            # сессии не создано, попробуем создать
            request.session.create()
        if not request.session.session_key:
            # что-то пошло не так, вызовем исключение
            raise exceptions.AuthenticationFailed(_('Проблема с созданием куки.'))
        return (request.session.session_key, None)


class RURLSerializer(serializers.ModelSerializer):
    """
    Redirected URL Serializer
    """
    class Meta:
        model = RedirectedURL
        fields = '__all__'

    def create(self, data):
        data.update({"user": self.context["user"]})
        return RedirectedURL(**data)


class RedirectedURLViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin):
    """
    Viewset for redirections
    """
    queryset = RedirectedURL.objects.all()
    serializer_class = RURLSerializer
    authentication_classes = [SessionAuth,]    

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context