from http import HTTPStatus

from django.http import SimpleCookie
from django.test import TestCase
from django.urls import reverse

# from django.contrib.auth.models import User
from users.models import User


class loginAjaxViewTestCase(TestCase):
    fixtures = ['categories.json', 'feature.json', 'product.json']

    def setUp(self) -> None:
        self.client.cookies = SimpleCookie({'csrftoken': 'csrftoken'})
        self.user = User.objects.create(username='admin')
        self.user.set_password('admin')
        self.user.save()

    def test_user_login(self):
        data = {'username': 'admin', 'password': 'admin'}
        path = reverse('login_ajax')
        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(self.user.is_authenticated)
