from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your tests here.



class RegistrationTestCase(APITestCase):
    
    def test_registration(self):
        data = {
            "username": "testcase",
            "email": "email@email.com",
            "password": "password@123",
            "password2": "password@123",
        }
        
        response=self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username="example", password="password@123")
        
    def test_login(self):
        data={
            "username":"example",
            "password":"password@123",
        }
        
        response=self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        self.token=Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION="TOKEN " + self.token.key)
        response=self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        