from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from employers.serializers.serializers import EmployerSerializer, TeamMembersModelSerializer, CompanySerializer, EmployeeSerializer, EmployeePsychometricsModelSerializer, TeamSerializer
from employers.models import Employer, Company, Employee, EmployeePsychometrics, Team, TeamMember
from accounts.models import UserType
from employers.permissions import IsEmployerOrNeither
from rest_framework.generics import RetrieveAPIView, CreateAPIView
# Create your views here.

class EmployerLeadView(ModelViewSet):
    #todo: fix the permission class
    permission_classes = (IsAuthenticated, )
    serializer_class = EmployerSerializer
    queryset = Employer.objects.all()

class CompanyView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class EmployeeView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

class EmployeePsychometricsView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = EmployeePsychometricsModelSerializer
    queryset = EmployeePsychometrics.objects.all()
    lookup_field = 'employee'

class TeamView(ModelViewSet):
    permission_classes = (IsAuthenticated, ) #todo: add isemployerLead to this.
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

class ListTeamMembers(RetrieveAPIView):
    """
    List the members of a specific team
    """
    lookup_field = 'team'
    lookup_url_kwarg = 'team'
    queryset = TeamMember.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = TeamMembersModelSerializer

