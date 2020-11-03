
from django.contrib.auth.models import User
from main.tests import BaseClassTestCase


class MainPageTestCase(BaseClassTestCase):
    """Test that main page returns HTTP 200"""

    def setUp(self):
        self.url = self.reverse('index')
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 's3cr37')
        self.user = User.objects.create_user('user', 'user@test.com', 'qwerty')
    
    def test_page_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_logged_as_user_response(self):
        self.client.login(username='user', password='qwerty')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_logged_as_admin_response(self):
        self.client.login(username='admin', password='s3cr37')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class NextPrevMatchTestCase(BaseClassTestCase):
    pass
