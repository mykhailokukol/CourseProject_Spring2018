"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from appmain import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main page'),
    path('home/', views.index, name='main page'),
    path('login/', views.login_page, name='login page'),
    path('signup/', views.signup, name='signing up page'),
    path('tasks/', views.tasks, name='tasks page'),
    path('profile/', views.profile, name='profile page'),
    path('profile/settings/', views.profile_settings, name='profile settings page'),
    # control pages urls here:
    # I KNOW I SHOULD BETTER CREATE NEW APP, BUT I'M TOO LAZY AND I DON'T HAVE ENOUGH TIME TO DO THAT.
    path('control/', views.control, name='control page'),
    path('control/accs_info/', views.accs_info, name='accs_info page'),
    path('control/fixate_accident/', views.fixate_accident, name='fixate_accident page'),
    path('control/fixate_violation/', views.fixate_violation, name='fixate_violation page'),
    path('control/owners_info/', views.owners_info, name='owners_info page'),
    path('control/send_email/', views.send_email, name='send_email page'),
    path('control/top_cars/', views.top_cars, name='top_cars page'),
    path('control/top_streets_vio/', views.top_streets_vio, name='top_streets_vio page'),
    path('control/top_streets_acc/', views.top_streets_acc, name='top_streets_acc page'),
    path('control/violators/', views.violators, name='violators page'),
    path('control/vios_info/', views.vios_info, name='vios_info page'),

]
