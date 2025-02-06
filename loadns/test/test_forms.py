import datetime
from django.test import TestCase, Client

from administraction.models import Student, Author, Sanction
from books.models import Book, Copy
from django.contrib.auth.models import User

from loadns.forms import LoanForm, LoanReturnForm
from loadns.models import Loan
        
        
class TestLoanForm(TestCase):  # Changed to TestCase since we're working with files
    
    def setUp(self):
        self.client = Client()
        
        self.superuser = User.objects.create_user(
            username='admin',
            password='123456',
            email='admin@test.com',
            is_staff=True,
            is_superuser=True
        )
        self.student = Student.objects.create(
            first_name = 'test name',
            last_name = 'test last name',
            dni = '12345678',
            number_phone = '123456789',
            address = 'test address',
            photo = 'xd.jpg',
            date_boarn = '2000-11-11'
        )
        self.author = Author.objects.create(
            first_name = 'test name',
            last_name = 'test last name',
            nacionality = 'test nacionality',
            photo = 'xd.jpg'
        )
        self.book = Book.objects.create(
            title = 'test title',
            abstract = 'test abstract',
            isbm = '100045781298765',
            num_page = '500',
            publication_date = '2000-01-01',
            author =  self.author,
            photo = 'xd.jpg'
        )
        
        self.copy = Copy.objects.create(
            book = self.book,
            code_internal = '0123456789',
            comment = 'test comment',
            location = 'xddxddx',
        )
        
        self.sanction = Sanction.objects.create(
            name = 'test name',
            description = 'test description'
        )
        
        
        self.valid_data = {
            'student': self.student.id,
            'copy': self.copy.id,
            'comment': 'test comment',
            'due_date': '2050-01-01', #can be null
        }
        
        self.valid_data_return = {
            'comment': 'test comment',
            'sanctions': [self.sanction.id],
        }
        
    def test_loan_create_form_valid_data(self):
        # self.client.login(username='admin', password='123456')
           
        form = LoanForm(
            data=self.valid_data
        )
        self.assertTrue(form.is_valid())
    
    def test_loan_create_form_no_data(self):
        form = LoanForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
    
    def test_loan_return_form_valid_data(self):
        # Create a loan first
        
        loan = Loan.objects.create(
            student=self.student,
            copy=self.copy,
            comment='test loan',
            due_date=datetime.date(2050, 1, 1),
            created_by_admin=self.superuser
        )
        
        # Now create the form with the loan instance
        form = LoanReturnForm(
            data=self.valid_data_return,
            instance=loan  # Pass the loan instance here
        )
        self.assertTrue(form.is_valid())
    
    def test_loan_return_form_no_data(self):
        self.client.login(username='admin', password='123456')
        
        loan = Loan.objects.create(
            student=self.student,
            copy=self.copy,
            comment='test loan',
            due_date=datetime.date(2050, 1, 1),
            created_by_admin=self.superuser
        )
        form = LoanReturnForm(
            data={},
            instance=loan)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    
    def tearDown(self):
        # Clean up any created files or test data
        Copy.objects.all().delete()
        Student.objects.all().delete()
        Author.objects.all().delete()
        Sanction.objects.all().delete()
        Book.objects.all().delete()
        