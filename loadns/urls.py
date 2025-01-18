from django.urls import path, include
from . import views


loan_patterns = [
    path('', views.loan_main, name='loan.index'),
    path('create/', views.loan_create, name='loan.create'),
    path('<int:id>/show/', views.loan_show, name='loan.show'),
    path('<int:id>/edit/', views.loan_update, name='loan.update'),
    path('<int:id>/delete/', views.loan_delete, name='loan.delete'),
    path('<int:id>/return/', views.loan_return, name='loan.return'),
    
]

urlpatterns = [
    path('prestamos/', include(loan_patterns)),
]