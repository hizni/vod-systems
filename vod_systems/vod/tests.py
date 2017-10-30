from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .user_forms import LoginForm


class RoutingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser = False
        self.user.is_staff = True

    def testRouteToNonLoginRequiredResource(self):
        self.client.login(username='testuser', password='testuserpassword')
        response = self.client.get(reverse('vod-login'))
        self.assertEqual(response.status_code, 200)

    def testRouteToLoginRequiredResourceFailing(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 302)

    def testLoginForm_completed(self):
        form = LoginForm(data={'username': 'john', 'password': 'johnpassword', })
        self.assertTrue(form.is_valid())

    def testLoginForm_incomplete1(self):
        form = LoginForm(data={'username': 'john', 'password': '', })
        self.assertFalse(form.is_valid())

    def testLoginForm_incomplete2(self):
        form = LoginForm(data={'username': '', 'password': 'johnpassword', })
        self.assertFalse(form.is_valid())

    def testLoginForm_correct(self):
        self.client.get('/vod-login/')
        self.client.login(username='john', password='johnpassword')
        form = LoginForm(data={'username': 'john', 'password': 'johnpassword1', })
        self.assertTrue(form.is_valid())
