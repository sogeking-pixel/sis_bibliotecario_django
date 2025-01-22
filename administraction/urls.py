from django.urls import path, include
from . import views



user_patterns = [
    path('', views.user_main, name='user.index'),
    path('create/', views.user_create, name='user.create'),
    path('<int:id>/show/', views.user_show, name='user.show'),
    path('<int:id>/edit/', views.user_update, name='user.update'),
    path('<int:id>/delete/', views.user_delete, name='user.delete'),
]



author_patterns = [
    path('', views.author_main, name='author.index'),
    path('create/', views.author_create, name='author.create'),
    path('<int:id>/show/', views.author_show, name='author.show'),
    path('<int:id>/edit/', views.author_update, name='author.update'),
    path('<int:id>/delete/', views.author_delete, name='author.delete'),
]


sanction_patterns = [
    path('', views.sanction_main, name='sanction.index'),
    path('create/', views.sanction_create, name='sanction.create'),
    path('<int:id>/show/', views.sanction_show, name='sanction.show'),
    path('<int:id>/edit/', views.sanction_update, name='sanction.update'),
    path('<int:id>/delete/', views.sanction_delete, name='sanction.delete'),
]


urlpatterns = [
    path('user/', include(user_patterns)),
    path('autor/', include(author_patterns)),
    path('sanciones/', include(sanction_patterns)),    
]
