from django.shortcuts import render
from rest_framework.views import APIView
from accounts.models import Candidate
from employers.models import Employer
from .models import Match
from .serializers import MatchSerializer
from rest_framework.response import Response
class CandidateGetMatchView(APIView):
    """"""
    def get(self, request, candidate):
        candidate = Candidate.objects.get(id=candidate)
        match = Match.objects.filter(candidate=candidate)
        serializer = MatchSerializer(match, many=True)

        return Response(serializer.data)

class EmployerGetMatchView(APIView):

    def get(self, request, employer):
        employer = Employer.objects.get(user__id=employer)
        match = Match.objects.filter(posting__company__company_lead=employer)
        serializer = MatchSerializer(match, many=True)

        return Response(serializer.data)