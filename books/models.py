from django.db import models
from administraction.models import Author
from utils.utils import compress_img, delete_img
from datetime import date
from cloudinary.models import CloudinaryField

# Create your models here.


class Book(models.Model):
    title = models.CharField( max_length=255)
    abstract = models.TextField()
    photo =  CloudinaryField( 'imagenes/Book/', default='imagenes/Book/default.jpg')
    isbm = models.CharField( max_length=15, unique=True)
    num_page = models.PositiveIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField(auto_now=False, auto_now_add=False)
    
    def save(self,*args, **kwargs):
        if self.photo:
            self.photo = compress_img(self.photo, folder="books")       
        super().save(*args, **kwargs)
    
    def delete(self,*args, **kwargs):
        if self.photo:
            delete_img(self.photo)
        super().delete(self,*args, **kwargs)
        
    def __str__(self):
       return f"{self.title} -- {self.author.first_name} {self.author.last_name}"
    
    def is_recent_publication(self):
        return date.today().year - self.publication_date.year <= 1
    
    
class Copy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    code_internal = models.CharField( max_length=10, unique=True)
    comment = models.TextField(null=True, blank=True)
    location = models.CharField( max_length=255)
    availability_status = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now=True, auto_now_add=False)
    def __str__(self):
       return f"{self.book.title} -- {self.code_internal}"
   