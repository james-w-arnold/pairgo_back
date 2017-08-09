from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import PostingSerializer
from .models import Posting
class PostingViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    serializer_class = PostingSerializer
    queryset = Posting.objects.all()
