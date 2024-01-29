from .test_setup import TestSetUp
from rest_framework import status
# import pdb
# pdb.set_trace()
from django.urls import reverse
from __Common.utils.tests import test_auth


class TestCreatePostView(TestSetUp):

    def test_unauthenticated(self):
        res = self.client.post(self.create_post_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_with_no_data(self):
        test_auth.test_register_login(self, data=self.user)

        res = self.client.post(self.create_post_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_success(self):

        # Generate random pixel values for the image

        test_auth.test_register_login(self, data=self.user)
        with open('posts/tests/dsa.png', '+rb') as file:
            self.post['image'] = file
            res_post = self.client.post(self.create_post_url, self.post)
            self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)


class TestListPostView(TestSetUp):
    def test_list_post_no_query(self):
        res = self.client.get(self.list_post_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestGetPostDetailView(TestSetUp):
    def test_post_detail(self):
        test_auth.test_register_login(self, data=self.user)
        with open('posts/tests/dsa.png', '+rb') as file:
            self.post['image'] = file
            res_create_post = self.client.post(self.create_post_url, self.post)
        res = self.client.get(reverse('detail-post',  kwargs={'pk': res_create_post.data['post'].get('id')}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_create_post.status_code, status.HTTP_201_CREATED)


class TestDeletePostView(TestSetUp):
    def test_post_delete(self):
        test_auth.test_register_login(self, data=self.user)
        with open('posts/tests/dsa.png', '+rb') as file:
            self.post['image'] = file
            res_create_post = self.client.post(self.create_post_url, self.post)
        res = self.client.delete(reverse('delete-post',  kwargs={'pk': res_create_post.data['post'].get('id')}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_create_post.status_code, status.HTTP_201_CREATED)

    def test_post_delete_fail_permission_denied(self):
        test_auth.test_register_login(self, data=self.user_2)
        with open('posts/tests/dsa.png', '+rb') as file:
            self.post['image'] = file
            res_create_post = self.client.post(self.create_post_url, self.post)
        test_auth.test_register_login(self, data=self.user)
        res = self.client.delete(reverse('delete-post',  kwargs={'pk': res_create_post.data['post'].get('id')}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_create_post.status_code, status.HTTP_201_CREATED)

    def test_post_not_found(self):
        test_auth.test_register_login(self, data=self.user)
        with open('posts/tests/dsa.png', '+rb') as file:
            self.post['image'] = file
            res_create_post = self.client.post(self.create_post_url, self.post)
        res = self.client.delete(reverse('delete-post',  kwargs={'pk': 100000000}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res_create_post.status_code, status.HTTP_201_CREATED)


class TestUpdatePostView(TestSetUp):
    def test_post_update_fail_permission_denied(self):
        test_auth.test_register_login(self, data=self.user_2)
        with open('posts/tests/dsa.png', '+rb') as file:
            self.post['image'] = file
            res_create_post = self.client.post(self.create_post_url, self.post)
        test_auth.test_register_login(self, data=self.user)
        res = self.client.put(reverse('update-post', kwargs={'pk': res_create_post.data['post'].get('id')}), data=self.post_update,)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_create_post.status_code, status.HTTP_201_CREATED)

    def test_post_update_success(self):
        test_auth.test_register_login(self, data=self.user_2)
        with open('posts/tests/dsa.png', '+rb') as file:
            self.post['image'] = file
            res_create_post = self.client.post(self.create_post_url, self.post)
        res = self.client.put(reverse('update-post', kwargs={'pk': res_create_post.data['post'].get('id')}), data=self.post_update,)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_create_post.status_code, status.HTTP_201_CREATED)

    def test_post_update_not_found(self):
        test_auth.test_register_login(self, data=self.user_2)
        with open('posts/tests/dsa.png', '+rb') as file:
            self.post['image'] = file
            res_create_post = self.client.post(self.create_post_url, self.post)
        res = self.client.put(reverse('update-post', kwargs={'pk': 100000}), data=self.post_update,)
        self.assertEqual(res_create_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class TestListPostMeView(TestSetUp):
    def test_post_list_unauthenticated(self):
        res = self.client.get(reverse('list-post-me'))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_list_success(self):
        test_auth.test_register_login(self, data=self.user_2)
        res = self.client.get(reverse('list-post-me'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
