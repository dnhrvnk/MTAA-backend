from django.urls import path
from . import consumers


websocket_urlpatterns = (
    path('video/<uuid:clubid>/', consumers.Consumer.as_asgi()),
)