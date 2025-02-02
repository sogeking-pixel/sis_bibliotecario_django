"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('', include('administraction.urls')),
    path('', include('books.urls')),
    path('', include('loadns.urls')),
    path('', include('dashboard.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', lambda request: redirect('index', permanent=True)),
]

from django.conf.urls import handler403, handler404, handler500

# Registrar las páginas de error
handler403 = 'dashboard.views.error_403'
handler404 = 'dashboard.views.error_404'
handler500 = 'dashboard.views.error_500'


