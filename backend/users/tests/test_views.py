from .test_setup import TestSetUp
from rest_framework import status
# import pdb
# pdb.set_trace()


class TestRegisterView(TestSetUp):
    def test_register_invalid_email(self):
        res = self.client.post(self.register_url, self.user_invalid_email)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_password(self):
        res = self.client.post(self.register_url, self.user_invalid_password)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_success(self):
        res = self.client.post(self.register_url, self.user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get('email'), self.user.get('email'))


class TestLoginView(TestSetUp):
    def test_login_email_not_found(self):
        self.client.post(self.register_url, self.user)
        res_login = self.client.post(self.login_url, self.user_email_not_found)
        self.assertEqual(res_login.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_password_incorrect(self):
        self.client.post(self.register_url, self.user)
        res_login = self.client.post(self.login_url, self.user_password_incorrect)
        self.assertEqual(res_login.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_success(self):
        self.client.post(self.register_url, self.user)
        res_login = self.client.post(self.login_url, self.user)
        self.assertEqual(res_login.status_code, status.HTTP_200_OK)
