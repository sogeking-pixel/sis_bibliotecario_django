from django.db import models
import random
from django.utils import timezone
from utils.utils import compress_img, delete_img
from datetime import date
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField



class Student(models.Model):
    code_student = models.CharField( max_length=10)
    first_name =  models.CharField( max_length=50)
    last_name = models.CharField( max_length=50)
    dni = models.CharField( max_length=8, unique=True)
    number_phone = models.CharField(max_length=9)
    address = models.CharField( max_length=255)
    email = models.EmailField( max_length=255, unique=True)
    photo = CloudinaryField('photo')
    date_boarn  = models.DateField( )
    create_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    
    def save(self,*args, **kwargs):
        if not self.pk:
            self.code_student = generar_code(self.dni)
        if self.photo:
            self.photo = compress_img(self.photo, folder="students")       
        super().save(*args, **kwargs)
    
    def delete(self,*args, **kwargs):
        if self.photo:
            delete_img(self.photo)
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_boarn.year - ((today.month, today.day) < (self.date_boarn.month, self.date_boarn.day))
    
    def clean(self):
        if not self.dni.isdigit() or len(self.dni) != 8:
            raise ValidationError('El DNI debe ser un número')
        if self.number_phone and not self.number_phone.isdigit():
            raise ValidationError('El número de teléfono debe ser un número')  

    
class Author(models.Model):
    first_name =  models.CharField( max_length=50)
    last_name = models.CharField( max_length=50)
    nacionality =  models.CharField( max_length=50)
    photo =  CloudinaryField('authors')
    
    def delete(self,*args, **kwargs):
        if self.photo:
            delete_img(self.photo)
        super().delete(*args, **kwargs)
    
    def save(self,*args, **kwargs):
        if self.photo:
            self.photo = compress_img(self.photo, folder="authors")       
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Sanction(models.Model):
    name = models.CharField( max_length=50)
    description = models.TextField()
    def __str__(self):
        return f"{self.name}"
    
    
def generar_code(dni):
    year = timezone.now().year
    year_str = str(year)[-2:]
    dni_part = dni[:2]
    random_part =''.join([str(random.randint(0, 9)) for _ in range(6)])
    unique_code = f"{dni_part}{random_part}{year_str}"
    while Student.objects.filter(code_student=unique_code).exists():
        random_part = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        unique_code = f"{dni_part}{year_str}{random_part}"
    return unique_code