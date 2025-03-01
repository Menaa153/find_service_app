from django.urls import path
from .views import ChatRoomView, MessageView

urlpatterns = [
    path('chats/', ChatRoomView.as_view(), name="chats"),
    path('chats/<str:room_name>/messages/', MessageView.as_view(), name="chat-messages"),
]
