from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from . import views
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
     
     
     path('signup/', views.signup , name='signup'),
     path('login/', auth_views.LoginView.as_view(template_name='users/loginform.html',authentication_form=LoginForm) , name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
 
     
]
