
from django.contrib import admin
from django.urls import path , include
from . import views  
app_name = 'category'
urlpatterns = [
    path('',views.index, name='index'),
    path('category_list/',views.category_list, name='category_list'),
    
]