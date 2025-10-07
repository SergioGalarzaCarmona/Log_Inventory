from django.urls import path
from .views import manage_chats, live_chat


urlpatterns = [
  path('chats',manage_chats,name='manage_chats'),
  path('chats/<int:id>', live_chat, name='live_chat' )
]