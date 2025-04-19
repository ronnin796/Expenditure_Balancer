# expenses/forms.py
from django import forms
from .models import Expense
from django.contrib.auth.models import User
from django.forms import ModelForm
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'shared_with']
        widgets = {
            'shared_with': forms.CheckboxSelectMultiple()
        }
        labels = {
            'description': 'Description',
            'amount': 'Amount',
            'category': 'Category',
            'shared_with': 'Shared With'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['shared_with'].queryset = User.objects.exclude(id=user.id)
        else:
            self.fields['shared_with'].queryset = User.objects.all()
    
    def save(self, commit=True, payer=None):
        expense = super().save(commit=False)
        if payer:
            expense.payer = payer  # Assign the payer (logged-in user)

        if commit:
            expense.save()
            self.save_m2m()
            expense.shared_with.add(payer)  # Ensure payer is included in the split

        return expense
