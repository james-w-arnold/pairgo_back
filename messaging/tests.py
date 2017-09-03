from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts.models import User, Candidate
from matching.models import Match
from employers.models import Employer
import logging
# Create your tests here.

class ThreadsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'test@django.com',
            first_name = 'James',
            last_name = 'Arnold',
            password = '123'
        )
        self.empuser = User.objects.create_user(
            email = 'emptest@django.com',
            first_name = 'Emilia',
            last_name = 'Arnold',
            password='123'
        )
        self.sUser = User.objects.create_superuser(
            email = 'supertest@django.com',
            first_name = 'Ryan',
            last_name = 'Arnold',
            password= '123'
        )
        self.candidate = Candidate.objects.create(user=self.user)
        self.employer = Employer.objects.create(user=self.empuser)
        self.match = Match.objects.create(candidate=self.candidate, employer=self.employer)
        self.user_token = Token.objects.get(user__email='test@django.com')
        self.empUser_token = Token.objects.get(user__email='emptest@django.com')
        self.sUser_token = Token.objects.get(user__email='supertest@django.com')
        self.client = APIClient()

    def test_creating_thread(self):
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.user_token)
        response = self.client.post('/messaging/thread/', data={"name" :"test_thread","match": self.match.id, "recipients": [self.candidate.id, self.employer.id]}, format='json')
        logger = logging.getLogger(__name__)
        logger.error(response)
