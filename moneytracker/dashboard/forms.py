# expenses/forms.py
from django import forms
from .models import Expense
from django.contrib.auth.models import User
from django.forms import ModelForm

INPUT_CLASS = (
    "w-full py-3 px-4 rounded-xl border border-slate-200 "
    "focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 outline-none transition-all"
)

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'shared_with']
        widgets = {
            'description': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. Dinner at restaurant'}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
            'category': forms.Select(attrs={'class': INPUT_CLASS}),
            'shared_with': forms.CheckboxSelectMultiple(attrs={'class': 'rounded border-slate-300 text-brand-500 focus:ring-brand-500'}),
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
