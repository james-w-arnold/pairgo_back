from django.shortcuts import render
import logging

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
from accounts.models import Candidate
# Create your views here.

class LoginView(ObtainAuthToken):
    """
    Base view for allowing any user to log in and obtain their AuthToken
    """
    serializer_class = serializers.CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        #TODO: Add functionality to check which type user is

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


class CreateCandidateView(ModelViewSet):
    """
    Allows for creation of a candidate model
    """
    permission_classes = (IsAuthenticated, permissions.IsOwner)
    queryset = Candidate.objects.all()
    #serializer_class =

    def perform_create(self, serializer):
        """
        :param serializer:
        :return:
        """


























