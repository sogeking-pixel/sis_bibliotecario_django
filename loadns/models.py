from django.db import models
from administraction.models import Student, Sanction
from books.models import Copy
from django.contrib.auth.models import User
from utils.utils import generate_qr, generate_code


# Create your models here.
class Loan(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, unique=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes', null=True, blank=True)
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    created_by_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans_created')
    received_by_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='loans_received')
    sanctions = models.ManyToManyField(Sanction, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateTimeField(null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only when creating a new instance
            self.copy.availability_status = False
            self.copy.save()
            self.code = generate_code(length=12)
            self.qr_code = generate_qr(self.code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.code} - {self.student}"



