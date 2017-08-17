from django.test import TestCase


class TestCalls(TestCase):

    def test_login(self):
        response = self.client.get('/vod/login', follow=True)
        self.assertTemplateUsed(response, './vod/login.html')