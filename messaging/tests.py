from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from accounts.models import User
# Create your tests here.

factory = APIRequestFactory()

request = factory.post('/accounts/login', {"email": "james@pairgo.co.uk", "password": "Darcy123"}, content_type='application/json')
print(request)

class ThreadsTest(APITestCase):
    def test_thread_create(self):

        login_request = self.client.post('/accounts/login', {"email" : "james@pairgo.co.uk", "password": "Darcy123"})
        token = login_request.data['token']
        url = "/messaging/thread/"
        data = {"name" : "Hi", "match" : 1}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)