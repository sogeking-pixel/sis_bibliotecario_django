from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from administraction.models import Author, Student, Sanction
from books.models import Book, Copy
from loadns.models import Loan
from django.contrib.messages import get_messages
from django.urls import NoReverseMatch
from datetime import date

class TestLoanView(TestCase):
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
        # Create a student
        self.student = Student.objects.create(
            first_name='Test',
            last_name='Student',
            email='student@test.com',
            dni='12345678',
            number_phone = '123456789',
            photo = 'xd.jpg',
            address = 'Test Address',
            date_boarn = '2000-01-01'
        )
        # Create necessary book and copy
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author',
            nacionality='test nacionality',
            photo='xd.jpg'
        )
        self.book = Book.objects.create(
            title='Test Book',
            abstract='Test Abstract',
            photo='test.jpg',
            isbm='978-3-16-148410',
            num_page=200,
            author=self.author,
            publication_date='2023-01-01'
        )
        self.copy = Copy.objects.create(
            book=self.book,
            code_internal='TEST001',
            comment = 'Test Comment',
            location = 'Test Location',
        )
        # Create loan data
        self.loan_data = {
            'student': self.student.id,
            'copy': self.copy.id,
            'created_by_admin': self.superuser.id,
            'due_date': '2028-01-01',
            'comment': 'Test comment'
        }

    def test_loan_no_authentication_index(self):
        response = self.client.get(reverse('loan.index'))
        expected_redirect = f"{reverse('login')}?next={reverse('loan.index')}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect)

    def test_loan_authenticated_admin_index(self):
        self.client.login(username='admin', password='123456')
        response = self.client.get(reverse('loan.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Loan/main.html')

    def test_loan_post_create(self):
        self.client.login(username='admin', password='123456')
        response = self.client.post(reverse('loan.create'), self.loan_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Préstamo creado exitosamente")
        self.assertRedirects(response, reverse('loan.index'))
        self.assertTrue(Loan.objects.filter(copy=self.copy).exists())

    def test_loan_get_show(self):
        self.client.login(username='admin', password='123456')
        loan = Loan.objects.create(
            student=self.student,
            copy=self.copy,
            created_by_admin=self.superuser,
            due_date=date(2024, 1, 1)
        )
        response = self.client.get(reverse('loan.show', args=[loan.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/Loan/show.html')

    def test_loan_post_return(self):
        self.client.login(username='admin', password='123456')
        loan = Loan.objects.create(
            student=self.student,
            copy=self.copy,
            created_by_admin=self.superuser,
            due_date=date(2024, 1, 1)
        )
        response = self.client.post(reverse('loan.return', args=[loan.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loan.index'))
        
        updated_loan = Loan.objects.get(id=loan.id)
        self.assertIsNotNone(updated_loan.return_date)
        self.assertEqual(updated_loan.received_by_admin, self.superuser)

    def tearDown(self):
        # Clean up any files created during the tests
        Loan.objects.all().delete()
        Copy.objects.all().delete()
        Book.objects.all().delete()
        Student.objects.all().delete()
        User.objects.all().delete()

