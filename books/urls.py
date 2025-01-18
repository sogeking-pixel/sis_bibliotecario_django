from django.urls import path, include
from . import views



copy_patterns = [
    path('', views.copy_main, name='copy.index'),
    path('create/', views.copy_create, name='copy.create'),
    path('<int:id>/show/', views.copy_show, name='copy.show'),
    path('<int:id>/edit/', views.copy_update, name='copy.update'),
    path('<int:id>/delete/', views.copy_delete, name='copy.delete'),
]


book_patterns = [
    path('', views.book_main, name='book.index'),
    path('create/', views.book_create, name='book.create'),
    path('<int:id>/show/', views.book_show, name='book.show'),
    path('<int:id>/edit/', views.book_update, name='book.update'),
    path('<int:id>/delete/', views.book_delete, name='book.delete'),
]


urlpatterns = [
    path('libros/', include(book_patterns)),
    path('copias/', include(copy_patterns)),
]