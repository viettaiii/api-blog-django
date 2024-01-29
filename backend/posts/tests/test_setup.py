from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
import numpy as np


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.create_post_url = reverse('create-post')
        self.list_post_url = reverse('list-post')
        self.user = {
            'id': 1,
            'email': 'test@gmail.com',
            'password': '123123'
        }
        self.user_2 = {
            'id': 2,
            'email': 'test2@gmail.com',
            'password': '123123'
        }

        self.post = {
            'id': 1,
            'title': 'title 1',
            'content': ' content1',
            'category': 'fashion'
        }
        self.post_update = {
            'title': 'title update',
            'content': ' content1 update',
            'category': 'fashion'
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
