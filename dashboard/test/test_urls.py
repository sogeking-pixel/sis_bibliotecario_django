from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard import views

class TestUrls(SimpleTestCase):
    
    def test_dashboard_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)


