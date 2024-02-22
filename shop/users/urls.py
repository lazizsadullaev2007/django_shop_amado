from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]