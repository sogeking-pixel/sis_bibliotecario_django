from django import forms
from .models import Book, Copy

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'abstract', 'photo', 'num_page', 'author', 'publication_date',  'isbm' ]
        labels = {
            'title': 'Título',
            'abstract': 'Resumen',
            'photo': 'Portada',
            'num_page': 'Número de Páginas',
            'author': 'Autor',
            'publication_date': 'Fecha de Publicación',
            'isbm': 'ISBM',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el título del libro'
            }),
            'isbm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el isbm del libro'
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el resumen del libro',
                'rows': 4
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'num_page': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el número de páginas'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el autor'
            }),
            'publication_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Ingresa la fecha de publicación'
            }),
        }
        

class CopyForm(forms.ModelForm):
    class Meta:
        model = Copy
        fields = ['book', 'code_internal', 'comment','location']
        labels = {
            'book': 'Libro',
            'code_internal': 'Código Interno',
            'comment': 'Comentario',
            'location': 'Ubicación',
        }
        widgets = {
            'book': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el libro'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe la ubicación de la copia'
            })
            ,
            'code_internal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el código interno'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un comentario acerca de la copia(No obligatorio), puede ser estado, observaciones, etc.',
                'rows': 4
            }),
        }
