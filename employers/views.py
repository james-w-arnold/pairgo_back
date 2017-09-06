from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from employers.serializers.serializers import EmployerSerializer, TeamMembersModelSerializer, CompanySerializer, EmployeeSerializer, EmployeePsychometricsModelSerializer, TeamSerializer, EmployerPsychometricSerializer
from employers.models import Employer, Company, Employee, EmployeePsychometrics, Team, TeamMember, EmployerPsychometrics
from accounts.models import UserType
from employers.permissions import IsEmployerOrNeither
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

class EmployerLeadView(ModelViewSet):
    #todo: fix the permission class
    permission_classes = (IsAuthenticated, )
    serializer_class = EmployerSerializer
    queryset = Employer.objects.all()

    lookup_field = 'user'

class CompanyView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    lookup_field = 'company_lead'

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
    lookup_field = 'company'

class ListTeamMembers(RetrieveAPIView):
    """
    List the members of a specific team
    """
    lookup_field = 'team'
    lookup_url_kwarg = 'team'
    queryset = TeamMember.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = TeamMembersModelSerializer

class InviteEmployee(APIView):
    """
    Class view to allow employers invite employees via email
    """
    permission_classes = ()

    def post(self, request, format=None):
        emails = request.data.get('emails', [])
        team  = request.data.get('team', None)
        company = request.data.get('company', None)
        if emails and team and company:

            team_obj = Team.objects.get(id=team)
            comp_obj = Company.objects.get(company_lead__id=company)
            for email in emails:

                link = "localhost:4200/invite?team={}&company={}&email={}".format(team_obj.id, comp_obj.id, email)
                email_string = "Hi there\n You've been invited to join the {} team at {}!\nClick this link to signup: {}".format(team_obj.team_name, comp_obj.company_name, link)

                mail = send_mail("You've been invited to a team on PairGo",
                          email_string,
                          from_email='james@pairgo.co.uk',
                          recipient_list=[email,]
                          )
            if mail==1:
                return Response({"success": True})
            else:
                return Response({"success": False})
        else:
            return Response({"data" : request.data, "emails" : emails},status=HTTP_400_BAD_REQUEST)


class EmployerLeadPsychoViewset(ModelViewSet):
    """
    Allows you to access the psychometrics of an employer lead
    """
    permission_classes = (IsAuthenticated,)
    queryset = EmployerPsychometrics.objects.all()
    serializer_class = EmployerPsychometricSerializer