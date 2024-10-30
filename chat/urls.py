from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('api/create-room/<str:uuid>/', views.create_room, name='create_room'),
    path('chat-admin/delete-room/<str:uuid>/', views.delete_room, name='delete_room'),
    path('chat-admin/', views.admin_room, name='admin_room'),
    path('chat-admin/add-user/', views.add_user, name='add_user'),
    path('chat-admin/<str:uuid>/', views.room_view, name='room'),
    path('chat-admin/users/<uuid:uuid>/', views.user_view, name='user_detail'),
]
