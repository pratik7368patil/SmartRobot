"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from mysite.core import views

urlpatterns = [
	path('', views.home, name='home'),
	path('signup/', views.signup, name='signup'),
    path('play/', views.play, name='play'),
	path('secret/', views.secret_page, name='secret'),
    path('how_work/', views.how_work, name='how_work'),
    path('get_cmd/', views.get_cmd, name='get_cmd'),
	path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('user_form/', views.user_form, name='user_form'),
    path('profile/', views.user_data, name='profile'),
]
