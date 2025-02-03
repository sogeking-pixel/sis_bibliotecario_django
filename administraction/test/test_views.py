from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from administraction.models import Student
from django.contrib.messages import get_messages
from django.urls import NoReverseMatch


class TestView(TestCase):
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
        # Create a photo
        self.image = open('administraction/test/test.jpg', 'rb')
        # Create a student data
        self.student_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'example@gmail.com',
            'dni': '12345678',
            'number_phone': '123456789',
            'photo':self.image,
            'address': 'Test Address',
            'date_boarn': '2000-01-01',
        } 
    
    def test_user_no_authentication_index(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('user.index'))
        expected_redirect = f"{reverse('login')}?next={reverse('user.index')}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect)

    def test_user_authenticated_admin_index(self):
        """Test that authenticated superusers can access the index"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('user.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/User/main.html')

    def test_user_authenticated_regular_index(self):
        """Test that regular users cannot access the index"""
        self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('user.index'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'home/page-403.html')
        
    def test_user_get_invalid_id (self):
        """Test that update endpoint validates ID format and existence:
        - Rejects non-numeric IDs
        - Rejects negative IDs
        """
        self.client.login(username='admin', password='123456')
        with self.assertRaises(NoReverseMatch):
            reverse('user.update', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('user.update', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('user.show', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('user.show', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('user.delete', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('user.delete', args=[-9])
            
    def test_user_get_create(self):
        """Test that authenticated superusers can access the create form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('user.create'))
        self.assertEqual(response.status_code, 405)
    
    def test_user_post_create(self):
        """Test that authenticated superusers can create a user"""
        self.client.login(username='admin', password='123456')
        response = self.client.post(reverse('user.create'), self.student_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Usuario creado exitosamente")
        self.assertRedirects(response, reverse('user.index'))
        self.assertTrue(Student.objects.filter(dni='12345678').exists())
    
    def test_user_get_show(self):
        """Test that authenticated superusers can access the update form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('user.show', args=[0]))
        self.assertEqual(response.status_code, 404)
        
        del self.student_data['photo']
        student = Student.objects.create(**self.student_data)
        response = self.client.get(reverse('user.show', args=[student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/User/show.html')
        
        
    def test_user_get_update(self):
        """Test that authenticated superusers can access the update form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('user.update', args=[1]))
        self.assertEqual(response.status_code, 405)
        
    def test_user_post_update(self):
        """Test that authenticated superusers can access the update form"""
        self.client.login(username='admin', password='123456')
        self.student_data['photo'] = 's/xd.jpg'
        student = Student.objects.create(**self.student_data)
        
        update_data = self.student_data.copy()
        update_data['first_name'] = 'Updated'
        update_data['last_name'] = 'Name'
        
        response = self.client.post(reverse('user.update', args=[student.id]), update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user.show', args=[student.id]))
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Usuario actualizado exitosamente")
        
        updated_student = Student.objects.get(id=student.id)
        self.assertEqual(updated_student.first_name, 'Updated')
        self.assertEqual(updated_student.last_name, 'Name')
    
    def test_user_get_delete(self):
        """Test that authenticated superusers can access the delete form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('user.delete', args=[0]))
        self.assertEqual(response.status_code, 405)
        
    def test_user_post_delete(self):
        """Test that authenticated superusers can delete a user"""
        self.client.login(username='admin', password='123456')
        
        response = self.client.post(reverse('user.delete', args=[0]))
        self.assertEqual(response.status_code, 404)
        
        self.student_data['photo'] = 's/xd.jpg'
        student = Student.objects.create(**self.student_data)
        response = self.client.post(reverse('user.delete', args=[student.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user.index'))
        self.assertFalse(Student.objects.filter(id=student.id).exists())
        

    
    
        
        
        
        
        