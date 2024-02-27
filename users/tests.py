from datetime import datetime, timedelta
# Create your tests here.
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    fixtures = ['socialapp.json']
    def setUp(self):
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], "Регистрация")
        self.assertTemplateUsed(response, "users/registration.html")

    def test_user_registration_post_success(self):
        data = {
            "first_name" : "nikita", "last_name" : "recaca",
            "username" : "recanos", "email" : "recanos@yandex.ru",
            "password1" : "123qwer321", "password2" : "123qwer321" 
        }

        username = data["username"]
        response = self.client.post(self.path, data)

        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())
        

class UserLoginViewTestCase(TestCase):
    fixtures = ['socialapp.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.login_url = reverse('users:login')

    def test_login_page_loads_successfully(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_successful(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, reverse('index'))

    def test_login_failure(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)