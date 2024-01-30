from .test_setup import TestSetUp
from django.urls import reverse
from rest_framework import status
# import pdb
# pdb.set_trace()
from __Common.utils.tests import test_auth


class TestCreateCommentView(TestSetUp):
    def test_create_comment_unauthenticated(self):
        res = self.client.post(self.create_comment_url, data=self.comment)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment_post_not_found(self):
        test_auth.test_register_login(self, data=self.user)
        res = self.client.post(self.create_comment_url, data=self.comment_post_not_found)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment_invalid_data(self):
        test_auth.test_register_login(self, data=self.user)
        res = self.client.post(self.create_comment_url, data=self.comment_invalid)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_success(self):
        test_auth.test_register_login(self, data=self.user)
        res = self.client.post(self.create_comment_url, data=self.comment)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class TestGetAllCommentView(TestSetUp):
    def test_get_all_comments(self):
        res = self.client.get(self.list_comment_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_comments_with_page(self):
        res = self.client.get(self.list_comment_url, params={'page': 2})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_comments_with_limit(self):
        res = self.client.get(self.list_comment_url, params={'limit': 2})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_comments_with_page_and_limit(self):
        res = self.client.get(self.list_comment_url, params={'limit': 2, 'page': '1'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_comments_with_page_and_limit(self):
        res = self.client.get(self.list_comment_url, params={'limit': 2, 'page': '1'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestDeleteCommentView(TestSetUp):
    def test_success(self):
        test_auth.test_register_login(self, data=self.user)
        res_comment = self.client.post(self.create_comment_url, data=self.comment)
        res = self.client.delete(reverse('delete-comment',  kwargs={'pk': res_comment.data['data'].get('id')}))
        self.assertEqual(res_comment.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthenticated(self):
        self.client.post(self.register_url, self.user)
        # self.client.post(self.login_url, self.user)
        res = self.client.post(self.create_comment_url, data=self.comment)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        test_auth.test_register_login(self, data=self.user)
        res_comment = self.client.post(self.create_comment_url, data=self.comment)
        res = self.client.delete(reverse('delete-comment',  kwargs={'pk': 100000000000}))
        self.assertEqual(res_comment.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_permission_denied(self):
        test_auth.test_register_login(self, data=self.user)
        res_comment = self.client.post(self.create_comment_url, data=self.comment)

        test_auth.test_register_login(self, data=self.user2)
        res = self.client.delete(reverse('delete-comment',  kwargs={'pk':  res_comment.data['data'].get('id')}))
        self.assertEqual(res_comment.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TestUpdateCommentView(TestSetUp):
    def test_success(self):
        test_auth.test_register_login(self, data=self.user)
        res_comment = self.client.post(self.create_comment_url, data=self.comment)
        res = self.client.put(reverse('update-comment',  kwargs={'pk': res_comment.data['data'].get('id')}), data=self.comment_update)
        self.assertEqual(res_comment.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_permission_denied(self):
        test_auth.test_register_login(self, data=self.user)
        res_comment = self.client.post(self.create_comment_url, data=self.comment)
        test_auth.test_register_login(self, data=self.user2)
        res = self.client.put(reverse('update-comment',  kwargs={'pk': res_comment.data['data'].get('id')}), data=self.comment_update)
        self.assertEqual(res_comment.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        test_auth.test_register_login(self, data=self.user)
        res_comment = self.client.post(self.create_comment_url, data=self.comment)
        res = self.client.put(reverse('update-comment',  kwargs={'pk': 1000000}))
        self.assertEqual(res_comment.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated(self):
        test_auth.test_register(self, data=self.user)
        # self.client.post(self.login_url, self.user)
        res = self.client.post(self.create_comment_url, data=self.comment)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
