from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from administraction.models import Student, Author, Sanction
from django.contrib.messages import get_messages
from django.urls import NoReverseMatch


class TestUserView(TestCase):
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
        
    def tearDown(self):
        # Clean up any files created during the tests
        Student.objects.all().delete()
        User.objects.all().delete()   

class TestAuthorView(TestCase):
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
        # Create author data
        self.author_data = {
            'first_name': 'Test',
            'last_name': 'Author',
            'photo': self.image,
            'nacionality': 'Test nationality'
        }

    def test_author_no_authentication_index(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('author.index'))
        expected_redirect = f"{reverse('login')}?next={reverse('author.index')}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect)

    def test_author_authenticated_admin_index(self):
        """Test that authenticated superusers can access the index"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('author.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Author/main.html')

    def test_author_authenticated_regular_index(self):
        """Test that regular users cannot access the index"""
        self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('author.index'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'home/page-403.html')
        
    def test_author_get_invalid_id(self):
        """Test that update endpoint validates ID format and existence"""
        self.client.login(username='admin', password='123456')
        with self.assertRaises(NoReverseMatch):
            reverse('author.update', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('author.update', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('author.show', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('author.show', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('author.delete', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('author.delete', args=[-9])
            
    def test_author_get_create(self):
        """Test that authenticated superusers can access the create form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('author.create'))
        self.assertEqual(response.status_code, 405)
    
    def test_author_post_create(self):
        """Test that authenticated superusers can create an author"""
        self.client.login(username='admin', password='123456')
        response = self.client.post(reverse('author.create'), self.author_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Autor creado exitosamente")
        self.assertRedirects(response, reverse('author.index'))
        author = Author.objects.latest("id")
        self.assertIsNotNone(author)
        self.assertTrue(Author.objects.filter(id=author.id).exists())
        self.assertEqual(
            f"{author.first_name} {author.last_name}".strip(),
            f"{self.author_data['first_name']} {self.author_data['last_name']}".strip()
        )
        
    
    def test_author_get_show(self):
        """Test that authenticated superusers can view author details"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('author.show', args=[0]))
        self.assertEqual(response.status_code, 404)
        
        self.author_data['photo'] = 's/xd.jpg'
        author = Author.objects.create(**self.author_data)
        response = self.client.get(reverse('author.show', args=[author.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Author/show.html')
        
    def test_author_get_update(self):
        """Test that authenticated superusers can access the update form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('author.update', args=[1]))
        self.assertEqual(response.status_code, 405)
        
    def test_author_post_update(self):
        """Test that authenticated superusers can update an author"""
        self.client.login(username='admin', password='123456')
        self.author_data['photo'] = 's/xd.jpg'
        author = Author.objects.create(**self.author_data)
        
        update_data = self.author_data.copy()
        update_data['first_name'] = 'Updated'
        update_data['last_name'] = 'Name'
        
        response = self.client.post(reverse('author.update', args=[author.id]), update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('author.show', args=[author.id]))
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Autor actualizado exitosamente")
        
        updated_author = Author.objects.get(id=author.id)
        self.assertEqual(updated_author.first_name, 'Updated')
        self.assertEqual(updated_author.last_name, 'Name')
    
    def test_author_get_delete(self):
        """Test that authenticated superusers can access the delete form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('author.delete', args=[0]))
        self.assertEqual(response.status_code, 405)
        
    def test_author_post_delete(self):
        """Test that authenticated superusers can delete an author"""
        self.client.login(username='admin', password='123456')
        
        response = self.client.post(reverse('author.delete', args=[0]))
        self.assertEqual(response.status_code, 404)
        
        self.author_data['photo'] = 's/xd.jpg'
        author = Author.objects.create(**self.author_data)
        response = self.client.post(reverse('author.delete', args=[author.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('author.index'))
        self.assertFalse(Author.objects.filter(id=author.id).exists())
        
    def tearDown(self):
        Author.objects.all().delete()
        User.objects.all().delete()    
    
class TestSanctionView(TestCase):
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
        # Create sanction data
        self.sanction_data = {
            'name': 'Test Sanction',
            'description': 'Test Description'
        }

    def test_sanction_no_authentication_index(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('sanction.index'))
        expected_redirect = f"{reverse('login')}?next={reverse('sanction.index')}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect)

    def test_sanction_authenticated_admin_index(self):
        """Test that authenticated superusers can access the index"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('sanction.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Sanction/main.html')

    def test_sanction_authenticated_regular_index(self):
        """Test that regular users cannot access the index"""
        self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('sanction.index'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'home/page-403.html')
        
    def test_sanction_get_invalid_id(self):
        """Test that update endpoint validates ID format and existence"""
        self.client.login(username='admin', password='123456')
        with self.assertRaises(NoReverseMatch):
            reverse('sanction.update', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('sanction.update', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('sanction.show', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('sanction.show', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('sanction.delete', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('sanction.delete', args=[-9])
            
    def test_sanction_get_create(self):
        """Test that authenticated superusers can access the create form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('sanction.create'))
        self.assertEqual(response.status_code, 405)
    
    def test_sanction_post_create(self):
        """Test that authenticated superusers can create a sanction"""
        self.client.login(username='admin', password='123456')
        response = self.client.post(reverse('sanction.create'), self.sanction_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Sanción creada exitosamente")
        self.assertRedirects(response, reverse('sanction.index'))
        sanction = Sanction.objects.latest("id")
        self.assertIsNotNone(sanction)
        self.assertTrue(Sanction.objects.filter(id=sanction.id).exists())
        self.assertEqual(sanction.name, self.sanction_data['name'])
    
    def test_sanction_get_show(self):
        """Test that authenticated superusers can view sanction details"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('sanction.show', args=[0]))
        self.assertEqual(response.status_code, 404)
        
        sanction = Sanction.objects.create(**self.sanction_data)
        response = self.client.get(reverse('sanction.show', args=[sanction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Sanction/show.html')
        
    def test_sanction_get_update(self):
        """Test that authenticated superusers can access the update form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('sanction.update', args=[1]))
        self.assertEqual(response.status_code, 405)
        
    def test_sanction_post_update(self):
        """Test that authenticated superusers can update a sanction"""
        self.client.login(username='admin', password='123456')
        sanction = Sanction.objects.create(**self.sanction_data)
        
        update_data = self.sanction_data.copy()
        update_data['name'] = 'Updated Name'
        update_data['description'] = 'Updated Description'
        
        response = self.client.post(reverse('sanction.update', args=[sanction.id]), update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('sanction.show', args=[sanction.id]))
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Sanción actualizada exitosamente")
        
        updated_sanction = Sanction.objects.get(id=sanction.id)
        self.assertEqual(updated_sanction.name, 'Updated Name')
        self.assertEqual(updated_sanction.description, 'Updated Description')
    
    def test_sanction_get_delete(self):
        """Test that authenticated superusers can access the delete form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('sanction.delete', args=[0]))
        self.assertEqual(response.status_code, 405)
        
    def test_sanction_post_delete(self):
        """Test that authenticated superusers can delete a sanction"""
        self.client.login(username='admin', password='123456')
        
        response = self.client.post(reverse('sanction.delete', args=[0]))
        self.assertEqual(response.status_code, 404)
        
        sanction = Sanction.objects.create(**self.sanction_data)
        response = self.client.post(reverse('sanction.delete', args=[sanction.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('sanction.index'))
        self.assertFalse(Sanction.objects.filter(id=sanction.id).exists())
        
    def tearDown(self):
        Sanction.objects.all().delete()
        User.objects.all().delete() 
        
        
        