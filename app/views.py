from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from app.models import RedirectedURL
from rest_framework import serializers
from django.contrib.sessions.models import Session
from importlib import import_module
from django.conf import settings
from rest_framework.response import Response


class RURLSerializer(serializers.ModelSerializer):
    """
    Redirected URL Serializer
    """
    class Meta:
        model = RedirectedURL
        fields = '__all__'


class RedirectedURLViewSet(ReadOnlyModelViewSet):
    """
    Viewset for redirections
    """
    queryset = RedirectedURL.objects.all()
    serializer_class = RURLSerializer
    def list(self, request, *args, **kwargs):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        s = SessionStore()
        if not s.session_key:
            s.create()
        sess = Session.objects.get(pk=s.session_key)
        print(sess.expire_date)
        return Response("its ok!")

