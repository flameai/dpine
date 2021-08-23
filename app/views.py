from rest_framework.viewsets import ModelViewSet
from app.models import RedirectedURL
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes


class RURLSerializer(serializers.ModelSerializer):
    """
    Redirected URL Serializer
    """
    class Meta:
        model = RedirectedURL
        fields = '__all__'


class RedirectedURLViewSet(ModelViewSet):
    """
    Viewset for redirections
    """
    queryset = RedirectedURL.objects.all()
    serializer_class = RURLSerializer
    
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_or_create_session(request):
    if not request.session.session_key:
        request.session.create()
    key = request.session.session_key
    return Response({"key":key}, status=200)