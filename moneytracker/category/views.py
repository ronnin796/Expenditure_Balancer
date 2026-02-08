from django.shortcuts import render
from .models import Category
# Create your views here.

def index(request):
    return render(request, 'category/index.html')

def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'category/category_list.html', context)