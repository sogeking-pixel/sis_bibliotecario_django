from django.test import TestCase

from administraction.models import Student, Sanction, Author
from books.models import Book, Copy

from django.core.files.uploadedfile import SimpleUploadedFile
from books.forms import BookForm, CopyForm

class TestBookForm(TestCase):  # Changed to TestCase since we're working with files
    
    def setUp(self):
        self.image_path = 'administraction/test/test.jpg'
        self.author = Author.objects.create(
            first_name = 'test name',
            last_name = 'test last name',
            nacionality = 'test nacionality',
            photo = 'xd.jpg'
        )
        self.valid_data = {
            'title': 'test title',
            'description': 'test description',
            'abstract': 'test abstract',
            'isbm': '100045781298765',
            'num_page': '500',
            'publication_date': '2000-01-01',
            'author': self.author.id,
        }
        
    def test_student_form_valid_data(self):
        with open(self.image_path, 'rb') as f:
            image_file = SimpleUploadedFile(
                name='test.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
            
        form = BookForm(
            data=self.valid_data,
            files={'photo': image_file}
        )
        self.assertTrue(form.is_valid())
    
    def test_book_form_no_data(self):
        form = BookForm(data={}, files={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)
        
        
    def tearDown(self):
        # Clean up any created files or test data
        Student.objects.all().delete()
        Author.objects.all().delete()
        
        
        
class TestCopyForm(TestCase):  # Changed to TestCase since we're working with files
    
    def setUp(self):
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
        self.valid_data = {
            'book': self.book.id,
            'code_internal': '0123456789',
            'comment': 'test comment', #can be null
            'location': 'xddxddx',
        }
        
    def test_student_form_valid_data(self):
            
        form = CopyForm(
            data=self.valid_data
        )
        self.assertTrue(form.is_valid())
    
    def test_book_form_no_data(self):
        form = CopyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
        
        
    def tearDown(self):
        # Clean up any created files or test data
        Copy.objects.all().delete()
        Student.objects.all().delete()
        Author.objects.all().delete()
        