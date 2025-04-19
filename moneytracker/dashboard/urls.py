
from django.contrib import admin
from django.urls import path , include
from .views import index
from . import views  
app_name = 'dashboard'
urlpatterns = [
     path('', views.index, name='index'),  # dashboard/ → index view
    path('list/', views.expense_list, name='expense_list'),
    path('create/', views.create_expense, name='create_expense'),
    path('settle/', views.settle_up, name='settle_up'),
    
]

