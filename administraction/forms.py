from django import forms
from .models import Student, Author, Sanction

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name','number_phone', 'dni', 'email', 'address', 'photo', 'date_boarn']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'dni': 'Dni',
            'number_phone': 'Numero de telefono',
            'email': 'Email',
            'address': 'Direccion',
            'photo': 'Subir imagen de perfil',
            'date_boarn': 'Fecha de nacimiento',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tus nombres'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tus apellidos'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu dni'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu email'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu direccion'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'date_boarn': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Ingresa tu fecha de nacimiento'
            }),
            'number_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu numero de telefono'
            }),
        }
        
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'nacionality', 'photo']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'nacionality': 'Nacionalidad',
            'photo': 'Subir imagen del autor',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe sus nombres'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe sus apellidos'
            }),
            'nacionality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe su nacionalidad'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class SanctionForm(forms.ModelForm):
    class Meta:
        model = Sanction
        fields = ['name', 'description']
        labels = {
            'name': 'Nombre o Titulo de la sancion',
            'description': 'Descripcion de la sancion',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el titulo de la sanción'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control m-2',
                'placeholder': 'Escribe la descripcion de la sanción',
                'rows': 4,
            }),
        }
