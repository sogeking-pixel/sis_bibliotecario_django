from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from administraction.models import Student, Author, Sanction
from django.contrib.messages import get_messages
from django.urls import NoReverseMatch


class TestDashboardView(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a superuser that can be used across tests
        self.superuser = User.objects.create_user(
            username='admin',
            password='123456',
            email='admin@test.com',
            is_staff=True,
            is_superuser=True
        )
        # Create a regular user
        self.regular_user = User.objects.create_user(
            username='testuser',
            password='123456',
            email='user@test.com'
        )
        
    
    def test_user_no_authentication_index(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('index'))
        expected_redirect = f"{reverse('login')}?next={reverse('index')}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect)

    def test_user_authenticated_admin_index(self):
        """Test that authenticated superusers can access the index"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/main.html')

    def test_user_authenticated_regular_index(self):
        """Test that regular users cannot access the index"""
        self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'home/page-403.html')
    
    def test_error_403(self):
        """Test that 403 error page is displayed correctly"""
        self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'home/page-403.html')
    
    def test_error_404(self):
        """Test that 404 error page is displayed correctly"""
        # Try to access a non-existent URL
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'home/page-404.html')
    
    def test_error_500(self):
        """Test that 500 error page is displayed correctly"""
        # Login as superuser to ensure we have access
        self.client.login(username='admin', password='123456')
        
        # Force a 500 error by raising an exception in a view
        with self.assertRaises(Exception):
            response = self.client.get('/force-error/')
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, 'home/page-500.html')
    
    
        
