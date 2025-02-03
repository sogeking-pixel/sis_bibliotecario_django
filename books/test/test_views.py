from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from administraction.models import Author
from books.models import Book, Copy
from django.contrib.messages import get_messages
from django.urls import NoReverseMatch

class TestBookView(TestCase):
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
        self.image = open('books/test/test.jpg', 'rb')
        # Create an author for the book
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author',
            nacionality = 'test nacionality',
            photo = 'xd.jpg'
        )
        # Create book data
        self.book_data = {
            'title': 'Test Book',
            'abstract': 'Test Abstract',
            'photo': self.image,
            'isbm': '978-3-16-148410',
            'num_page': 200,
            'author': self.author.id,
            'publication_date': '2023-01-01',
        }

    def test_book_no_authentication_index(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('book.index'))
        expected_redirect = f"{reverse('login')}?next={reverse('book.index')}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect)

    def test_book_authenticated_admin_index(self):
        """Test that authenticated superusers can access the index"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('book.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Book/main.html')

    def test_book_authenticated_regular_index(self):
        """Test that regular users cannot access the index"""
        self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('book.index'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'home/page-403.html')

    def test_book_get_invalid_id(self):
        """Test that update endpoint validates ID format and existence"""
        self.client.login(username='admin', password='123456')
        with self.assertRaises(NoReverseMatch):
            reverse('book.update', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('book.update', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('book.show', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('book.show', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('book.delete', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('book.delete', args=[-9])

    def test_book_get_create(self):
        """Test that authenticated superusers can access the create form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('book.create'))
        self.assertEqual(response.status_code, 405)

    def test_book_post_create(self):
        """Test that authenticated superusers can create a book"""
        self.client.login(username='admin', password='123456')
        response = self.client.post(reverse('book.create'), self.book_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Libro creado exitosamente")
        self.assertRedirects(response, reverse('book.index'))
        self.assertTrue(Book.objects.filter(isbm='978-3-16-148410').exists())

    def test_book_get_show(self):
        """Test that authenticated superusers can view book details"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('book.show', args=[0]))
        self.assertEqual(response.status_code, 404)

        self.book_data['photo'] = 'asd/xd.jpg'
        self.book_data['author'] = self.author
        
        
        book = Book.objects.create(**self.book_data)
        response = self.client.get(reverse('book.show', args=[book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Book/show.html')

    def test_book_get_update(self):
        """Test that authenticated superusers can access the update form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('book.update', args=[1]))
        self.assertEqual(response.status_code, 405)

    def test_book_post_update(self):
        """Test that authenticated superusers can update a book"""
        self.client.login(username='admin', password='123456')
        self.book_data['author'] = self.author
        self.book_data['photo'] = 's/xd.jpg'
        book = Book.objects.create(**self.book_data)

        update_data = self.book_data.copy()
        update_data['title'] = 'Updated Title'
        update_data['abstract'] = 'Updated Abstract'
        update_data['author'] = self.author.id

        response = self.client.post(reverse('book.update', args=[book.id]), update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book.show', args=[book.id]))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Libro actualizado exitosamente")

        updated_book = Book.objects.get(id=book.id)
        self.assertEqual(updated_book.title, 'Updated Title')
        self.assertEqual(updated_book.abstract, 'Updated Abstract')

    def test_book_get_delete(self):
        """Test that authenticated superusers can access the delete form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('book.delete', args=[0]))
        self.assertEqual(response.status_code, 405)

    def test_book_post_delete(self):
        """Test that authenticated superusers can delete a book"""
        self.client.login(username='admin', password='123456')

        response = self.client.post(reverse('book.delete', args=[0]))
        self.assertEqual(response.status_code, 404)

        self.book_data['photo'] = 's/xd.jpg'
        self.book_data['author'] = self.author
        book = Book.objects.create(**self.book_data)
        
        response = self.client.post(reverse('book.delete', args=[book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book.index'))
        self.assertFalse(Book.objects.filter(id=book.id).exists())
        
    def tearDown(self):
        # Clean up any files created during the tests
        Copy.objects.all().delete()
        Book.objects.all().delete()
        User.objects.all().delete()
        Author.objects.all().delete()


class TestCopyView(TestCase):
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
        # Create an author for the book
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author',
            nacionality='test nacionality',
            photo='xd.jpg'
        )
        # Create a book for the copy
        self.book = Book.objects.create(
            title='Test Book',
            abstract='Test Abstract',
            photo='test.jpg',
            isbm='978-3-16-148410',
            num_page=200,
            author=self.author,
            publication_date='2023-01-01'
        )
        # Create copy data
        self.copy_data = {
            'book': self.book.id,
            'code_internal': 'TEST001',
            'comment': 'Test Comment',
            'location': 'Test Location',
            'availability_status': True
        }

    def test_copy_no_authentication_index(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('copy.index'))
        expected_redirect = f"{reverse('login')}?next={reverse('copy.index')}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect)

    def test_copy_authenticated_admin_index(self):
        """Test that authenticated superusers can access the index"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('copy.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Copy/main.html')

    def test_copy_authenticated_regular_index(self):
        """Test that regular users cannot access the index"""
        self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('copy.index'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'home/page-403.html')

    def test_copy_get_invalid_id(self):
        """Test that update endpoint validates ID format and existence"""
        self.client.login(username='admin', password='123456')
        with self.assertRaises(NoReverseMatch):
            reverse('copy.update', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('copy.update', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('copy.show', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('copy.show', args=[-9])
        with self.assertRaises(NoReverseMatch):
            reverse('copy.delete', args=['abc'])
        with self.assertRaises(NoReverseMatch):
            reverse('copy.delete', args=[-9])

    def test_copy_get_create(self):
        """Test that authenticated superusers can access the create form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('copy.create'))
        self.assertEqual(response.status_code, 405)

    def test_copy_post_create(self):
        """Test that authenticated superusers can create a copy"""
        self.client.login(username='admin', password='123456')
        response = self.client.post(reverse('copy.create'), self.copy_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Copia creada exitosamente")
        self.assertRedirects(response, reverse('copy.index'))
        self.assertTrue(Copy.objects.filter(code_internal='TEST001').exists())

    def test_copy_get_show(self):
        """Test that authenticated superusers can view copy details"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('copy.show', args=[0]))
        self.assertEqual(response.status_code, 404)
        self.copy_data['book'] = self.book
        copy = Copy.objects.create(**self.copy_data)
        response = self.client.get(reverse('copy.show', args=[copy.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Copy/show.html')

    def test_copy_get_update(self):
        """Test that authenticated superusers can access the update form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('copy.update', args=[1]))
        self.assertEqual(response.status_code, 405)

    def test_copy_post_update(self):
        """Test that authenticated superusers can update a copy"""
        self.client.login(username='admin', password='123456')
        self.copy_data['book'] = self.book
        copy = Copy.objects.create(**self.copy_data)

        update_data = self.copy_data.copy()
        update_data['location'] = 'Updated Location'
        update_data['comment'] = 'Updated Comment'
        
        update_data['book'] = self.book.id
        response = self.client.post(reverse('copy.update', args=[copy.id]), update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('copy.show', args=[copy.id]))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Copia actualizada exitosamente")

        updated_copy = Copy.objects.get(id=copy.id)
        self.assertEqual(updated_copy.location, 'Updated Location')
        self.assertEqual(updated_copy.comment, 'Updated Comment')

    def test_copy_get_delete(self):
        """Test that authenticated superusers can access the delete form"""
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('copy.delete', args=[0]))
        self.assertEqual(response.status_code, 405)

    def test_copy_post_delete(self):
        """Test that authenticated superusers can delete a copy"""
        self.client.login(username='admin', password='123456')

        response = self.client.post(reverse('copy.delete', args=[0]))
        self.assertEqual(response.status_code, 404)

        self.copy_data['book'] = self.book
        copy = Copy.objects.create(**self.copy_data)
        
        self.copy_data['book'] = self.book.id
        response = self.client.post(reverse('copy.delete', args=[copy.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('copy.index'))
        self.assertFalse(Copy.objects.filter(id=copy.id).exists())
        
        
    def tearDown(self):
        # Clean up any files created during the tests
        Copy.objects.all().delete()
        Book.objects.all().delete()
        User.objects.all().delete()
        Author.objects.all().delete()