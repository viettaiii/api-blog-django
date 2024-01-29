from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user = {
            'email': 'test@gmail.com',
            'password': '123123'
        }

        self.user_invalid_email = {
            'email': 'invalid_email',
            'password': '123123'
        }

        self.user_invalid_password = {
            'email': 'test@gmail.com',
            'password': ''
        }

        self.user_email_not_found = {
            'email': 'not_found_email@gmail.com',
            'password': ''
        }

        self.user_password_incorrect = {
            'email': 'test@gmail.com',
            'password': 'incorrect_password'
        }
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
