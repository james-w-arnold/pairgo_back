from django.shortcuts import render
import logging

from commons.middleware.middleware import RequestLogViewMixin

from django.core.exceptions import ValidationError

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.serializers import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import permissions
from accounts.models import Candidate, UserType, CandidatePsychometrics, CandidateEducation
# Create your views here.

class LoginView(ObtainAuthToken):
    """
    Base view for allowing any user to log in and obtain their AuthToken
    """
    serializer_class = serializers.CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response(
            {
                'token': token.key,
                'id': token.user_id
            }
        )


class UserRegistrationView(CreateAPIView):
    """
    Allows for creation of new user in the system, requires an admin account to initiate the creation
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = serializers.UserRegistrationSerializer


class UserTypeView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserTypeSerializer
    queryset = UserType.objects.all()
    lookup_field = 'user'
    logger = logging.getLogger(__name__)

    def create(self, request, *args, **kwargs):
        self.logger.error(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CreateCandidateView(ModelViewSet, RequestLogViewMixin):
    """
    Allows for creation of a candidate model
    """
    permission_classes = (IsAuthenticated, permissions.IsOwner)
    queryset = Candidate.objects.all()
    serializer_class = serializers.CandidateSerializer
    lookup_field = 'user'

    def perform_create(self, serializer):
        """
        :param serializer:
        :return:
        """
        queryset = Candidate.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError('An account already exists for this user.')
        else:
            logger = logging.getLogger(__name__)
            userType, nada = UserType.objects.get_or_create(user=self.request.user)
            logger.error(userType)
            userType.isCandidate = True
            userType.save()

        serializer.save(user=self.request.user)
        #self.index(serializer.data, self.request.user.id)


class CandidatePsychometricsView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.PsychometricSerializer
    queryset = CandidatePsychometrics.objects.all()

    lookup_field = 'user'

class EducationView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.EducationModelSerializer
    queryset = CandidateEducation.objects.all()

    lookup_field = 'user'




















