from django.db import models
from administraction.models import Author
from utils.utils import compress_img, delete_img

# Create your models here.


class Book(models.Model):
    title = models.CharField( max_length=255)
    abstract = models.TextField()
    photo =  models.ImageField( upload_to='imagenes/Author/', height_field=None, width_field=None, max_length=None)
    isbm = models.CharField( max_length=15, unique=True)
    num_page = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField(auto_now=False, auto_now_add=False)
    
    def save(self,*args, **kwargs):
        if self.photo:
            self.photo = compress_img(self.photo)       
        super().save(*args, **kwargs)
    
    def delete(self,*args, **kwargs):
        if self.photo:
            delete_img(self.photo)
        super().delete(self,*args, **kwargs)
        
    def __str__(self):
       return f"{self.title} -- {self.author.first_name} {self.author.last_name}"
    
    
    
class Copy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    code_internal = models.CharField( max_length=10, unique=True)
    comment = models.TextField(null=True, blank=True)
    location = models.CharField( max_length=255)
    availability_status = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now=True, auto_now_add=False)
    def __str__(self):
       return f"{self.book.title} -- {self.code_internal}"