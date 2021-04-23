from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notificaciones/(?P<numero_usuario>\w+)/$', consumers.NotificacionesConsumer.as_asgi()),
]
