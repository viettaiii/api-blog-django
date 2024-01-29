def test_register(self, data):
    res = self.client.post(self.register_url, data=data)
    return res


def test_login(self, data):
    res = self.client.post(self.login_url, data=data)
    return res


def test_register_login(self, data):
    test_register(self, data)
    return test_login(self, data)
