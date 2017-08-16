from django.test import TestCase


class TestCalls(TestCase):

    def test_landing(self):
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'vod_systems/landing.html')