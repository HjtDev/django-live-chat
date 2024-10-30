from django.urls import path
from .consumers import ChatConsumer


urlpatterns = [
    path('ws/<str:room_name>/', ChatConsumer.as_asgi()),
]
