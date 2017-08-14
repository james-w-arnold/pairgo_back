from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Message, Thread
from matching.models import Match
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from rest_framework import status

class ThreadView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = ThreadSerializer

    def retrieve(self, request, pk):
        match = Match.objects.get(id=pk)
        thread = Thread.objects.get(match=match)
        messages = Message.objects.filter(thread=thread)
        if messages.exists():
            messages_ser = MessageSerializer(data=messages, many=True)
            return Response(messages_ser.data, status=status.HTTP_200_OK)
        elif messages.exists() != True:
            return Response(status=status.HTTP_204_NO_CONTENT)



