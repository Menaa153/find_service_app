from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomView(APIView):
    def get(self, request):
        """Retorna todas las salas de chat disponibles"""
        chats = ChatRoom.objects.all()
        serializer = ChatRoomSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crea una nueva sala de chat"""
        serializer = ChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageView(APIView):
    def get(self, request, room_name):
        """Retorna todos los mensajes de una sala de chat"""
        chatroom = get_object_or_404(ChatRoom, room_name=room_name)
        messages = Message.objects.filter(chatroom=chatroom).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, room_name):
        """Guarda un nuevo mensaje en una sala de chat"""
        chatroom = get_object_or_404(ChatRoom, room_name=room_name)
        data = request.data.copy()
        data['chatroom'] = chatroom.id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
