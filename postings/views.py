from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostingSerializer, MultiplePostingSerializer
from .models import Posting
from matching.pg_nn.pgnn.pgnearestneighbour import Matching
from employers.models import Employer, Employee
import logging
import threading

class PostingViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    serializer_class = PostingSerializer
    queryset = Posting.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #logger.error(serializer.data['id'])
        #produce matches

        matches = Matching(serializer.data)
        matches.cleanCandidates()
        matches.match()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class RetrievePostingsView(APIView):
    def get(self, request, employer, *args, **kwargs):
        postings = Posting.objects.filter(employer__id=employer)
        serializers = PostingSerializer(postings, many=True)

        return Response(serializers.data)

class TeamRetrievePostingsView(APIView):
    def get(self, request, team, *args, **kwargs):
        postings = Posting.objects.filter(team__id=team)
        serializers = PostingSerializer(postings, many=True)

        return Response(serializers.data)



