from rest_framework.test import APITestCase
from django.urls import reverse
from posts.models import Post
from users.models import User


class TestSetUp(APITestCase):
    def setUp(self):
        self.create_comment_url = reverse('create-comment')
        self.list_comment_url = reverse('list-comment')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        # Set up user
        self.user = {
            'id': 1,
            'email': 'test@gmail.com',
            'password': '123123'
        }
        self.user2 = {
            'id': 2,
            'email': 'test2@gmail.com',
            'password': '123123'
        }
        self.user_one = User.objects.create(email='user_one@gmail.com', password='123123')
        self.user_two = User.objects.create(email='user_two@gmail.com', password='123123')

        # Set up the post
        self.post_one = Post.objects.create(title='title 1', content='content1', category='fashion', user=self.user_one, image="images/1.pgn")
        self.post_two = Post.objects.create(title='title 2', content='content 2', category='fashion', user=self.user_two, image='images/1.png')

        self.comment = {
            'content': " comment 1",
            'user_id': self.user.get('id'),
            'post_id': self.post_one.id
        }
        self.comment_update = {
            'content': " comment 1",
            'user_id': self.user.get('id'),
        }
        self.comment_update_fail = {
            'content': " comment 1",
            'user_id': self.user2.get('id'),

        }
        self.comment_invalid = {
            'user_id': self.user.get('id'),
            'post_id': self.post_one.id
        }
        self.comment_post_not_found = {
            'content': " comment 1",
            'user_id': self.user.get('id'),
        }
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
