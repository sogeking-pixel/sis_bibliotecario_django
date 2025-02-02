from django.test import TestCase, Client
from django.urls import reverse

class TestView(TestCase):
    def test_login_index(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/login.html')