from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.expense_list, name="expense_list"),
    path("create/", views.create_expense, name="create_expense"),
    path("settle/", views.settle_up, name="settle_up"),
]

