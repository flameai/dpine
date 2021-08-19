from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from app.models import RedirectedURL
from rest_framework import serializers
from django.http import HttpResponse, response


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
        if not self.request.COOKIES.get('redirectAPP'):
            response = HttpResponse("First time visit")
            response.set_cookie('redirectAPP', 'user_id_123123124')
            return response
        return super().list(request, *args, **kwargs)

