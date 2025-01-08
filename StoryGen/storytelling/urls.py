from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.landing_page, name='landing_page'), 
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='storytelling/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('history/', views.history, name='history'),
]
