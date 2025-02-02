from django.db import models
from administraction.models import Student, Sanction
from books.models import Copy
from django.contrib.auth.models import User
from utils.utils import generate_qr, generate_code, compress_img
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from cloudinary.models import CloudinaryField
# Create your models here.

class Loan(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, unique=True, null=True)
    qr_code = CloudinaryField('photo', transformation={'quality': 'auto:eco'} , folder="Loans_Qrs" )
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    created_by_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans_created')
    received_by_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='loans_received')
    sanctions = models.ManyToManyField(Sanction, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateTimeField(null=True)
    

    def __str__(self):
        return f"Loan {self.code} - {self.student}"
    
    @property
    def is_returned(self):
        return self.return_date is not None
    
    @property
    def is_active(self):
        return not self.is_returned
    
    @property
    def is_late(self):
        return date.today() < self.due_date
    
    @property
    def is_pending(self):
        return self.is_active and not self.is_late   
    
    @property
    def is_late_return(self):
        return self.is_returned and self.return_date.date() > self.due_date
    

    def clean(self):
        if self.due_date < date.today() and not self.pk:
            raise ValidationError('La fecha de devolución no puede ser menor a la fecha actual')       
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only when creating a new instance
            self.copy.availability_status = False
            self.copy.save()
            self.code = generate_code(length=12)
            self.qr_code = generate_qr(self.code)
        super().save(*args, **kwargs)


