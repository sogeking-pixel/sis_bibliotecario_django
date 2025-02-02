from django.test import TestCase, Client
from django.urls import reverse

class TestUserView(TestCase):
    def test_user_no_authentication_index(self):
        client = Client()
        # response = client.get(reverse('user.index'))
        # self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'home/User/main.html')