from django import forms
from .models import Loan
from datetime import datetime, timedelta
from books.models import Copy

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['student', 'copy', 'comment', 'due_date']
        labels = {
            'student': 'Estudiante',
            'copy': 'Copia',
            'comment': 'Comentario',
            'due_date': 'Fecha Limite de devolucion',
        }
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'copy': forms.Select(attrs={
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un comentario',
                'rows': 3,
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Fecha que se tiene que devolver',
                'min': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'value': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            }),
            
        }
        error_messages = {
            'due_date': {
                'invalid': "Introduce una fecha válida.",
                'required': "Este campo es obligatorio.",
            }
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_copies = Copy.objects.filter(availability_status=True)
        if not available_copies.exists():
            self.fields['copy'].choices = [('', 'No hay copias disponibles')]
        else:
            self.fields['copy'].queryset = available_copies
        # add a condition to filter sanctioned students
            
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < datetime.now().date() + timedelta(days=1):
            raise forms.ValidationError("La fecha de devolución no puede ser anterior a mañana.")
        return due_date


class LoanUpdateForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['comment', 'sanctions', 'due_date', 'code']
        labels = {
            'comment': 'Comentario',
            'sanctions': 'Sanciones',
          
            'due_date': 'Fecha Limite de devolucion',
            'code': 'Código',
        }
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un comentario',
                'rows': 3,
            }),
            'sanctions': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'readonly': True,
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
        }


class LoanReturnForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['comment', 'sanctions']
        labels = {
            'comment': 'Comentario',
            'sanctions': 'Sanciones',
        }
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un comentario',
                'rows': 3,
            }),
            'sanctions': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }
