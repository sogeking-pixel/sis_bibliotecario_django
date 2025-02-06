from django.test import SimpleTestCase, TestCase
from administraction.forms import AuthorForm, SanctionForm, StudentForm
from administraction.models import Student, Sanction, Author
from django.core.files.uploadedfile import SimpleUploadedFile

class TestStudentForm(TestCase):  # Changed to TestCase since we're working with files
    
    def setUp(self):
        self.image_path = 'administraction/test/test.jpg'
        self.valid_data = {
            'first_name': 'test name',
            'last_name': 'test last_name',
            'number_phone': '123456789',
            'dni': '10004578',
            'email': 'test@gmail.com',
            'address': 'test address',
            'date_boarn': '2000-01-01'
        }
        
    def test_student_form_valid_data(self):
        with open(self.image_path, 'rb') as f:
            image_file = SimpleUploadedFile(
                name='test.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
            
        form = StudentForm(
            data=self.valid_data,
            files={'photo': image_file}
        )
            
        self.assertTrue(form.is_valid())
    
    def test_student_form_no_data(self):
        form = StudentForm(data={}, files={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 9)
        
        
    def tearDown(self):
        # Clean up any created files or test data
        Student.objects.all().delete()
        
        
        
class TestAuthorForm(TestCase):
    def setUp(self):
        self.image_path = 'administraction/test/test.jpg'
        self.valid_data = {
            'first_name': 'test name',
            'last_name': 'test last_name',
            'nacionality': 'test nacionality',
        }
    
    def test_sanction_form_valid_data(self):
        with open(self.image_path, 'rb') as f:
            image_file = SimpleUploadedFile(
                name='test.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
            
        form = AuthorForm(
            data=self.valid_data,
            files={'photo': image_file}
        )
            
        self.assertTrue(form.is_valid())    
        
    def test_student_form_no_data(self):
        form = AuthorForm(data={}, files={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def tearDown(self):
        # Clean up any created files or test data
        Author.objects.all().delete()        
        
        
        
class TestSanctionForm(TestCase):
    
    def test_sanction_form_valid_data(self):
        form =SanctionForm(
            data = {
                'name': 'test name',
                'description': 'test desciption',
            }
        )
        self.assertTrue(form.is_valid())    
        
    def test_student_form_no_data(self):
        form = SanctionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def tearDown(self):
        # Clean up any created files or test data
        Sanction.objects.all().delete()