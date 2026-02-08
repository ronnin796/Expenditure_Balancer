from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ExpenseForm
from .models import Expense
from .services import calculate_settlement


@login_required
def index(request):
    return render(request, 'dashboard/index.html')


@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(payer=request.user)
            messages.success(request, 'Expense added successfully.')
            return redirect('dashboard:expense_list')
    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'dashboard/create.html', {'form': form})

@login_required
def expense_list(request):
    expenses = Expense.objects.select_related('category', 'payer').prefetch_related('shared_with').order_by('-date')
    total = sum(e.amount for e in expenses)
    return render(request, 'dashboard/list.html', {'expenses': expenses, 'total': total})

@login_required
def settle_up(request):
    expenses = Expense.objects.all().prefetch_related('shared_with').select_related('payer')
    settlement = calculate_settlement(expenses)
    return render(request, 'dashboard/settle.html', settlement)
