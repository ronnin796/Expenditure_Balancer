from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('category.urls', namespace='category')),
    path('dashboard/', include('dashboard.urls')),
    path('users/', include('users.urls', namespace='users')),
]
