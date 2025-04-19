from django.db import models

from category.models import Category
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date  = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paid_expenses")
    shared_with = models.ManyToManyField(User, related_name="shared_expenses")

    def __str__(self):
       return f"{self.description} - {self.amount} ({self.payer.username if self.payer else 'No payer'})"