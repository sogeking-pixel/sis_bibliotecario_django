from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Book, Copy
from .forms import BookForm, CopyForm
from loadns.models import Loan
from loadns.forms import LoanForm
from utils.utils import admin_required


# Create your views here.


@admin_required
def book_main(request):
    """
    Handle the main book view.
    This view handles GET requests to display a list of books. It prepares
    the context with book data and renders the 'home/Book/main.html' template.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered HTML page with the context data.
    """
    
    if request.method != 'GET':
        return
    
    books = Book.objects.all()
    
    table = {
        'title' : 'Tabla Libros',
        'headers': ['Titulo','ISBM','Autor',],
        'fields': ['title', 'isbm','author',],
        'data' : books,
        'accions':{
        'show': 'book.show',
        'delete': 'book.delete',
        }
    }
    
    
    context = {
        'table': table,
        'form': BookForm()
    }
        
    return render(request,'home/Book/main.html' , context )        


@admin_required
def book_create(request):
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', 'book.index'))
    
    form = BookForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            
            form.save()
            messages.success(request, "Libro creado exitosamente")
        except Exception as e:
            messages.error(request, "Error al crear el libro")
    else:
        messages.error(request, f"Error en el formulario: {form.errors}")
        
    return redirect(request.META.get('HTTP_REFERER', 'book.index'))
    

@admin_required
def book_delete(request, id):
    if request.method != 'POST':
        return
    book = get_object_or_404(Book, id=id)
    book.delete()
    messages.info(request, "Libro eliminado exitosamente")
    return redirect(request.META.get('HTTP_REFERER', 'book.index'))


@admin_required
def book_show(request, id):
    if request.method != 'GET':
        return
    book = get_object_or_404(Book, id=id)
    form = BookForm(instance=book)
    
    form_copy = CopyForm(initial={'book': book})
    form_copy.fields['book'].queryset = Book.objects.filter(id=book.id)
    form_copy.fields['book'].empty_label = None
    form_copy.fields['book'].widget.attrs['readonly'] = True
    
    
    copies = Copy.objects.filter(book_id=book.id)
    cant_loan = Loan.objects.filter(copy__book_id=book.id).count()
    table = {
        'title': 'Tabla de Copias',
        'headers': ['ID', 'Código Interno', 'Ubicación', 'Comentario', 'Disponibilidad'],
        'fields': ['id', 'code_internal', 'location', 'comment', 'availability_status'],
        'data': copies,
        'accions': {
            'show': 'copy.show',
            'delete': 'copy.delete',
        },
    }
    
    context = {
        'book': book,
        'form': form,
        'table': table,
        'count_copies': copies.count(),
        'count_loands': cant_loan,
        'form_copy': form_copy
    }
    return render(request, 'home/Book/show.html', context)   
    

@admin_required    
def book_update(request, id):
    if request.method != 'POST':
        return
    book = get_object_or_404(Book, id=id)
    form = BookForm(request.POST, request.FILES, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, "Libro actualizado exitosamente")
        
    else:
        messages.error(request, f"Error al actualizar el libro: {form.errors}")
    return redirect('book.show', id=id)




@admin_required
def copy_main(request):
    """
    Handle the main copy view.
    This view handles GET requests to display a list of copies. It prepares
    the context with copy data and renders the 'home/Copy/main.html' template.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered HTML page with the context data.
    """
    
    if request.method != 'GET':
        return
    
    copies = Copy.objects.all()
    
    table = {
        'title' : 'Tabla Copias',
        'headers': ['Title', 'Código Interno', 'Ubicacion','Comentario', 'Disponibilidad'],
        'fields': ['book', 'code_internal','location', 'comment', 'availability_status'],
        'data' : copies,
        'accions':{
            'show': 'copy.show',
            'delete': 'copy.delete',
        }
    }
    
    context = {
        'table': table,
        'form': CopyForm()
    }
        
    return render(request,'home/Copy/main.html' , context )        


@admin_required
def copy_create(request):
    if request.method != 'POST':
        return
    
    form = CopyForm(request.POST)
    if form.is_valid():
        copy = form.save(commit=False)
        copy.save()
        messages.success(request, "Copia creada exitosamente")
    else:
        messages.error(request, f"Error en el formulario: {form.errors}")
    
    return redirect(request.META.get('HTTP_REFERER', 'copy.index'))    
    

@admin_required
def copy_delete(request, id):
    if request.method != 'POST':
        return
    copy = get_object_or_404(Copy, id=id)
    copy.delete()
    messages.info(request, "Copia eliminada exitosamente")
    return redirect(request.META.get('HTTP_REFERER', 'copy.index'))    


@admin_required
def copy_show(request, id):
    if request.method != 'GET':
        return
    copy = get_object_or_404(Copy, id=id)
    form = CopyForm(instance=copy)
    loan_form = LoanForm(initial={'copy': copy})
    loan_form.fields['copy'].queryset = Copy.objects.filter(id=copy.id)
    loan_form.fields['copy'].empty_label = None
    loan_form.fields['copy'].widget.attrs['readonly'] = True
    
    loans = Loan.objects.filter(copy_id=copy.id)
    table = {
        'title': 'Tabla de Prestamos',
        'headers': ['Codigo de Prestamo', 'Estudiante', 'Fecha de Prestamo',],
        'fields': ['code', 'student', 'created_date'],
        'data': loans,
        'accions': {
            'show': 'loan.show',
        },
    }
    
    context = {
        'copy': copy,
        'form': form,
        'loan_form': loan_form,
        'table': table,
        'count_loands': loans.count(),
    }
    

    return render(request, 'home/Copy/show.html', context)   
    

@admin_required    
def copy_update(request, id):
    if request.method != 'POST':
        return
    copy = get_object_or_404(Copy, id=id)
    form = CopyForm(request.POST, instance=copy)
    if form.is_valid():
        form.save()
        messages.success(request, "Copia actualizada exitosamente")
        
    else:
        messages.error(request, f"Error al actualizar la copia: {form.errors}")
    return redirect('copy.show', id=id)

   