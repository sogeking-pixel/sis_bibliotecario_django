from django.shortcuts import render
from datetime import datetime
from administraction.models import Student, Author, Sanction
from loadns.models import Loan
from books.models import Book, Copy

from django.conf import settings
from utils.utils import admin_required
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from django.db.models import Q
from datetime import timedelta

# Create your views here.
def error_403(request, exception):
    return render(request, 'home/page-403.html', status=403)

def error_404(request, exception):
    return render(request, 'home/page-404.html', status=404)

def error_500(request):
    return render(request, 'home/page-500.html', status=500)

def calculate_percentage(current, previous):
    return ((current - previous) / previous * 100) if previous else 0

@admin_required
def index(request):
    
    cards = return_cards()
    
    graphic = loan_time_stack() 
    
    graphic_time = loan_time_line()
   
    context = {
        'cards': cards,
        'graphic_stack': graphic,
        'graphic_line_time': graphic_time
    }
    return render(request, 'home/main.html', context)



def return_cards():
    now = datetime.now()
    current_month = now.month
    last_month = current_month - 1 or 12

    total_loans = Loan.objects.count()
    
    new_users = Student.objects.filter(create_at__month=current_month).count()
    available_copies = Copy.objects.filter(availability_status=True).count()
    pending_returns = Loan.objects.filter(return_date__isnull=True).count()

    last_month_loans = Loan.objects.filter(created_date__month=last_month).count()
    last_month_users = Student.objects.filter(create_at__month=last_month).count()
    last_month_copies = Copy.objects.filter(availability_status=True, created_at__month=last_month).count()
    last_month_returns = Loan.objects.filter(return_date__isnull=True, created_date__month=last_month).count()


    card_data = [
        ('Prestamos Totales', total_loans, last_month_loans),
        ('Nuevos Usuarios', new_users, last_month_users),
        ('Copias Disponibles', available_copies, last_month_copies),
        ('Devoluciones Pendientes', pending_returns, last_month_returns)
    ]

    cards = [
        {
            'title': title,
            'num': current,
            'porcent': calculate_percentage(current, previous),
            'subtitle_range': 'Since last month'
        }
        for title, current, previous in card_data
    ]

    return cards


def get_last_n_months_labels(n):
    now = datetime.now()
    return [(now - timedelta(days=i * 30)).strftime('%B') for i in reversed(range(n))]


def get_monthly_counts(loans, months_back, filter_conditions):
    now = datetime.now()
    return [
        loans.filter(
            created_date__month=(now - timedelta(days=i * 30)).month,
            **filter_conditions
        ).count()
        for i in reversed(range(months_back))
    ]
    

def loan_time_stack():
    now = datetime.now()
    
    number_of_months = 4
    
    loans = Loan.objects.filter(created_date__gte=now - timedelta(days=number_of_months * 30))

    labels = get_last_n_months_labels(n=number_of_months)

    datasets = [
        {
            'label': 'Pendiente',
            'data': get_monthly_counts(loans, number_of_months, {'return_date__isnull': True}),
            'backgroundColor': 'rgba(255, 206, 86, 0.5)',
        },
        {
            'label': 'Retornado',
            'data': get_monthly_counts(loans, number_of_months, {'return_date__isnull': False}),
            'backgroundColor': 'rgba(75, 192, 192, 0.5)',
        },
        {
            'label': 'Atrasado',
            'data': get_monthly_counts(loans, number_of_months, {'due_date__lt': now, 'return_date__isnull': True}),
            'backgroundColor': 'rgba(255, 99, 132, 0.5)',
        }
    ]
    
    return {'labels': labels, 'datasets': datasets}


def get_loans_grouped_by(loans, trunc_field, date_format, range_steps, delta, start_date):
    grouped_loans = loans.annotate(period=trunc_field).values('period').annotate(count=Count('id')).order_by('period')
    labels = [(start_date - i * delta).strftime(date_format) for i in reversed(range(range_steps))]
    data = [
        next((entry['count'] for entry in grouped_loans if entry['period'].strftime(date_format) == label), 0)
        for label in labels
    ]
    return labels, data


def loan_time_line():
    now = datetime.now()
    loans = Loan.objects.all()

    # Configuración de rangos y formatos
    daily_labels, daily_data = get_loans_grouped_by(
        loans.filter(created_date__gte=now - timedelta(days=14)),
        TruncDay('created_date'),
        '%d-%m',
        14,
        timedelta(days=1),
        now
    )

    weekly_labels, weekly_data = get_loans_grouped_by(
        loans.filter(created_date__gte=now - timedelta(weeks=7)),
        TruncWeek('created_date'),
        'Semana %U',
        7,
        timedelta(weeks=1),
        now
    )
    
    # Adjust weekly labels to start from 'Semana 01' instead of 'Semana 00'
    weekly_labels = ['Semana {:02d}'.format(int(label.split()[1]) + 1) for label in weekly_labels]

    monthly_labels, monthly_data = get_loans_grouped_by(
        loans.filter(created_date__gte=now - timedelta(days=6 * 30)),
        TruncMonth('created_date'),
        '%B',
        6,
        timedelta(days=30),
        now
    )

    return {
        'daily': {
            'labels': daily_labels,
            'data': daily_data
        },
        'weekly': {
            'labels': weekly_labels,
            'data': weekly_data
        },
        'monthly': {
            'labels': monthly_labels,
            'data': monthly_data
        }
    }

    monthly_labels, monthly_data = get_loans_grouped_by(
        loans.filter(created_date__gte=now - timedelta(days=6 * 30)),
        TruncMonth('created_date'),
        '%B',
        6,
        timedelta(days=30),
        now
    )

    return {
        'daily': {
            'labels': daily_labels,
            'data': daily_data
        },
        'weekly': {
            'labels': weekly_labels,
            'data': weekly_data
        },
        'monthly': {
            'labels': monthly_labels,
            'data': monthly_data
        }
    }
