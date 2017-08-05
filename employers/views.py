from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from employers.serializers.serializers import EmployerSerializer, CompanySerializer
from employers.models import Employer, Company
from accounts.models import UserType
from employers.permissions import IsEmployerOrNeither
# Create your views here.

class EmployerLeadView(ModelViewSet):
    #todo: fix the permission class
    permission_classes = (IsAuthenticated, )
    serializer_class = EmployerSerializer
    queryset = Employer.objects.all()

    def perform_create(self, serializer):
        queryset = Employer.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError('You already have an employer account!')
        else:
            userType = UserType.objects.get(user=self.request.user)
            userType.isEmployer = True
            userType.save()
        serializer.save(user=self.request.user)

class CompanyView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

