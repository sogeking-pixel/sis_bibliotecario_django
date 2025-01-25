from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from administraction.models import Student, Author, Sanction
from .models import Loan
from books.models import Book, Copy
from .forms import LoanForm, LoanUpdateForm, LoanReturnForm
from django.contrib import messages
from utils.utils import admin_required
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.


@admin_required
def loan_main(request):
    """
    Handle the main loan view.
    This view handles GET requests to display a list of loans. It prepares
    the context with loan data and renders the 'home/Loan/main.html' template.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered HTML page with the context data.
    """
    
    if request.method != 'GET':
        return
    
    loans = Loan.objects.all()
    
    table = {
        'title' : 'Tabla Prestamos',
        'headers': ['Codigo de Prestamo', 'Copia','Empretador?', 'Fecha de Prestamos', 'Fecha Limite' ],
        'fields': ['code', 'copy','student','created_date', 'due_date'],
        'data' : loans,
        'accions':{
            'show': 'loan.show',
            'delete': 'loan.delete',
            'return': 'loan.return'
        },
       
    }
    
    context = {
        'table': table,
        'form': LoanForm(),
        'form_return': LoanReturnForm(),
        'today': datetime.now()
    }
        
    return render(request, 'home/Loan/main.html', context)        


@admin_required
def loan_create(request):
    if request.method != 'POST':
        return
    
    form = LoanForm(request.POST, request.FILES)
    
    if not form.is_valid():
        messages.error(request, f"Error en el formulario: {form.errors}")
        return redirect(request.META.get('HTTP_REFERER', 'loan.index'))    

    if not form.cleaned_data['copy'].availability_status:
        messages.error(request, f"Error en el formulario: La copia no esta disponible") 
        return redirect(request.META.get('HTTP_REFERER', 'loan.index'))    
        
    loan = form.save(commit=False)
    loan.created_by_admin = request.user
    loan.save()
    messages.success(request, "Prestamo creado exitosamente")
        
    return redirect(request.META.get('HTTP_REFERER', 'loan.index'))
    
    
    
def process_loan_return(loan, user):
    loan.return_date = timezone.now()
    loan.received_by_admin = user
    
    if loan.return_date.date() > loan.due_date:
        sanction, _ = Sanction.objects.get_or_create(name='Tardanza')
        loan.sanctions.add(sanction)

def update_copy_status(copy):
    copy.availability_status = True
    copy.save()



@admin_required
def loan_return(request, id):
    if request.method != 'POST':
        return
    loan = get_object_or_404(Loan, id=id)
    
    if loan.return_date:
        messages.error(request, "El préstamo ya ha sido devuelto anteriormente.")
        return redirect(request.META.get('HTTP_REFERER', 'loan.index'))
    
    process_loan_return(loan, request.user)
    
    form = LoanReturnForm(request.POST, instance=loan)
    
    if not form.is_valid():
        messages.error(request, f"Error en el formulario: {form.errors}")
        return redirect(request.META.get('HTTP_REFERER', 'loan.index'))    
    copy =  loan.copy
    update_copy_status(copy)
    
    form.save()
    
    messages.success(request, "Préstamo devuelto exitosamente")
    
    return redirect(request.META.get('HTTP_REFERER', 'loan.index'))
    


@admin_required
def loan_delete(request, id):
    if request.method != 'POST':
        return
    
    loan = get_object_or_404(Loan, id=id)
    
    if loan.return_date:
        messages.danger(request, "No se puede eliminar un prestamo que ya se ha devuelto")
        return redirect(request.META.get('HTTP_REFERER', 'loan.index'))
    
    copy = loan.copy
    copy.availability_status = True
    copy.save()
    loan.delete()
    messages.info(request, "Prestamo eliminado exitosamente")
    return redirect(request.META.get('HTTP_REFERER', 'loan.index'))


@admin_required
def loan_show(request, id):
    if request.method != 'GET':
        return
    loan = get_object_or_404(Loan, id=id)
    form = LoanUpdateForm(instance=loan)  
    context = {
        'loan': loan,
        'form': form,
    }
    return render(request, 'home/Loan/show.html', context)   
    

@admin_required    
def loan_update(request, id):
    if request.method != 'POST':
        return
    loan = get_object_or_404(Loan, id=id)
    form = LoanUpdateForm(request.POST, request.FILES, instance=loan)
    if form.is_valid():
        form.save()
        messages.success(request, "Prestamo actualizado exitosamente")
        
    else:
        messages.error(request, f"Error al actualizar el prestamo: {form.errors}")
    return redirect('loan.show', id=id)
   