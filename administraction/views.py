from django.shortcuts import render, redirect, get_object_or_404
# from django.core.paginator import Paginator
from .models import Student, Author, Sanction
from loadns.models import Loan
from books.models import Book
from .forms import StudentForm, AuthorForm, SanctionForm
from books.forms import BookForm
from loadns.forms import LoanForm
from django.contrib import messages
from utils.utils import admin_required



@admin_required
def user_main(request):
    """
    Handle the main user view.
    This view handles GET requests to display a list of students. It prepares
    the context with student data and renders the 'home/User/main.html' template.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered HTML page with the context data.
    """
    
    if request.method != 'GET':
        return
    
    students = Student.objects.all()
    
    context = {
        'title' : 'Tabla Usuario',
        'headers': ['Nombre','Apellidos','Codigo', 'correo'],
        'fields': ['first_name','last_name','code_student','email'],
        'data' : students,
        'accions':{
        'show': 'user.show',
        'delete': 'user.delete',
        },
        'form': StudentForm()
    }
        
    return render(request,'home/User/main.html' , context )        


@admin_required 
def user_create(request):
    if request.method != 'POST':
        return
    form = StudentForm(request.POST, request.FILES)
    if form.is_valid():
        # student = form.save(commit=False)
        try:
            form.save()
            messages.success(request, "Usuario creado exitosamente")
        except Exception as e:
            messages.error(request, "Error al crear el usuario")
    else:
        messages.error(request, f"Error en el formulario: {form.errors}")
        
    return redirect(request.META.get('HTTP_REFERER', 'user.index'))
    
    
@admin_required
def user_delete(request, id):
    if request.method != 'POST':
        return
    
    student = get_object_or_404(Student, id=id)    
    student.delete()
    messages.info(request, "Usuario eliminado exitosamente")
    return redirect(request.META.get('HTTP_REFERER', 'user.index'))


@admin_required
def user_show(request, id):
    if request.method != 'GET':
        return
    student = get_object_or_404(Student, id=id)
    form = StudentForm(instance=student)
    form.fields['dni'].widget.attrs['readonly'] = True
    form.fields['email'].widget.attrs['readonly'] = True
    
    
    loan_form = LoanForm(initial={'student': student})
    loan_form.fields['student'].queryset = Student.objects.filter(id=student.id)
    loan_form.fields['student'].empty_label = None
    loan_form.fields['student'].widget.attrs['readonly'] = True
    
    loans = Loan.objects.filter(student_id=student.id)
    
    table = {
        'title': 'Tabla de Prestamos',
        'headers': ['Codigo de Prestamo', 'Copia', 'Fecha de Prestamo',],
        'fields': ['code', 'copy', 'created_date'],
        'data': loans,
        'accions': {
            'show': 'loan.show',
        },
    }
    
    total_sanctions = Sanction.objects.filter(loan__in=loans).count()
    
    context = {
        'user': student,
        'form': form,
        'table': table,
        'loan_form': loan_form,
        'preview_loans': loans[:5],
        'count_loans': loans.count(),
        'total_returns': loans.filter(return_date__isnull=False).count(),
        'total_sanctions': total_sanctions,
    }
    return render(request, 'home/User/show.html', context)
    

@admin_required    
def user_update(request, id):
    if request.method != 'POST':
        return
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST, request.FILES, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado exitosamente")
        
    else:
        messages.error(request, f"Error al actualizar el usuario: {form.errors}")
    return redirect('user.show', id=id)
   
   
   
@admin_required   
def author_main(request):
    """
    Handle the main author view.
    This view handles GET requests to display a list of authors. It prepares
    the context with author data and renders the 'home/Author/main.html' template.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered HTML page with the context data.
    """
    
    if request.method != 'GET':
        return
    
    authors = Author.objects.all()
    table = {
        'title': 'Tabla Autor',
        'headers': ['Nombre', 'Apellidos', 'Nacionalidad'],
        'fields': ['first_name', 'last_name', 'nacionality'],
        'data': authors,
        'accions': {
            'show': 'author.show',
            'delete': 'author.delete',
        },
    }
    context = {
        'table' : table,
        'form': AuthorForm()
    }
        
    return render(request, 'home/Author/main.html', context)


@admin_required
def author_create(request):
    if request.method != 'POST':
        return
    
    form = AuthorForm(request.POST, request.FILES)
    if form.is_valid():        
        try:      
            form.save()
            messages.success(request, "Autor creado exitosamente")
        except Exception as e:
            messages.error(request, "Error al crear el autor")
    else:
        messages.error(request, f"Error en el formulario: {form.errors}")
        
    return redirect(request.META.get('HTTP_REFERER', 'author.index'))    
    

@admin_required
def author_delete(request, id):
    if request.method != 'POST':
        return
    author = get_object_or_404(Author, id=id)   
    author.delete()
    messages.info(request, "Autor eliminado exitosamente")
    return redirect(request.META.get('HTTP_REFERER', 'author.index'))    


@admin_required
def author_show(request, id):
    if request.method != 'GET':
        return
    author = get_object_or_404(Author, id=id)
    form = AuthorForm(instance=author)
    
    
    form_book = BookForm(initial={'author': author})
    form_book.fields['author'].queryset = Author.objects.filter(id=author.id)
    form_book.fields['author'].empty_label = None
    form_book.fields['author'].widget.attrs['readonly'] = True
    
    
    
    books = Book.objects.filter(author_id=author.id)
  
    table = {
        'title': 'Tabla de Libros',
        'headers': ['ID', 'Título', 'Fecha de Publicación', 'ISBM'],
        'fields': ['id', 'title', 'publication_date', 'isbm'],
        'data': books,
        'accions': {
            'show': 'book.show',
            'delete': 'book.delete',
        },
    }
    
    context = {
        'author': author,
        'form': form,
        'form_book': form_book,
        'table': table,
        'preview_books': books[:5],
        'count_books': books.count(),
    }
    return render(request, 'home/Author/show.html', context)
    

@admin_required    
def author_update(request, id):
    if request.method != 'POST':
        return
    author = get_object_or_404(Author, id=id)
    form = AuthorForm(request.POST, request.FILES, instance=author)
    if form.is_valid():
        form.save()
        messages.success(request, "Autor actualizado exitosamente")
    else:
        messages.error(request, f"Error al actualizar el autor: {form.errors}")
    return redirect('author.show', id=id)



@admin_required   
def sanction_main(request):
    """
    Handle the main sanction view.
    This view handles GET requests to display a list of sanctions. It prepares
    the context with sanction data and renders the 'home/Sanction/main.html' template.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered HTML page with the context data.
    """
    
    if request.method != 'GET':
        return
    
    sanctions = Sanction.objects.all()
    
    table = {
        'title': 'Tabla Sanciones',
        'headers': [ 'Titulo o Nombre', 'Descripcion'],
        'fields': [ 'name', 'description'],
        'data': sanctions,
        'accions': {
            'show': 'sanction.show',
            'delete': 'sanction.delete',
        },
    }
    
    context = {
        'table' : table,
        'form': SanctionForm()
    }
    
     
    return render(request, 'home/Sanction/main.html', context)


@admin_required
def sanction_create(request):
    if request.method != 'POST':
        return
    
    form = SanctionForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Sanción creada exitosamente")
    else:
        messages.error(request, f"Error en el formulario: {form.errors}")
    
    return redirect(request.META.get('HTTP_REFERER', 'sanction.index'))
        

@admin_required
def sanction_delete(request, id):
    if request.method != 'POST':
        return
    sanction = get_object_or_404(Sanction, id=id)
    sanction.delete()
    messages.info(request, "Sanción eliminada exitosamente")
    return redirect(request.META.get('HTTP_REFERER', 'sanction.index'))


@admin_required
def sanction_show(request, id):
    if request.method != 'GET':
        return
    sanction = get_object_or_404(Sanction, id=id)
    form = SanctionForm(instance=sanction)
    
    loans = Loan.objects.filter(sanctions__id=id)
  
    table = {
        'title': f'Prestamos con Sanciones',
        'headers': ['Codigo', 'Copia', 'Fecha de Prestamo', 'Fecha Limite', 'Fecha de Devolucion'],
        'fields': ['code', 'copy', 'created_date', 'due_date', 'return_date'],
        'data': loans,
        'accions': {
            'show': 'loan.show',
        },
    }
    
    context = {
        'sanction': sanction,
        'form': form,
        'table': table,
        'count_loands': loans.count(),
    }
    return render(request, 'home/Sanction/show.html', context)
    
    
@admin_required    
def sanction_update(request, id):
    if request.method != 'POST':
        return
    sanction = get_object_or_404(Sanction, id=id)
    form = SanctionForm(request.POST, instance=sanction)
    if form.is_valid():
        form.save()
        messages.success(request, "Sanción actualizada exitosamente")
    else:
        messages.error(request, f"Error al actualizar la sanción: {form.errors}")
    return redirect('sanction.show', id=id)

