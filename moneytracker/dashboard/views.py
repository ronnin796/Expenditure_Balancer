from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from heapq import heappush, heappop

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')


@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(payer=request.user)
            return redirect('dashboard:expense_list')
    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'dashboard/create.html', {'form': form})

@login_required
def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'dashboard/list.html', {'expenses': expenses})

@login_required



def settle_up(request):
    expenses = Expense.objects.all().prefetch_related('shared_with').select_related('payer')
    balances = defaultdict(float)

    for expense in expenses:
        amount = float(expense.amount)
        payer = expense.payer.username
        shared_users = [user.username for user in expense.shared_with.all()]
        num_users = len(shared_users)

        if num_users == 0:
            continue  # skip invalid expense

        share = amount / num_users

        # The payer pays the full amount
        balances[payer] += amount

        # All shared users (including payer) owe their share
        for user in shared_users:
            balances[user] -= share

    balances = dict(balances)
    creditors, debtors, transactions = [], [], []

    for person, amount in balances.items():
        if amount > 0:
            heappush(creditors, (-amount, person))  # max heap
        elif amount < 0:
            heappush(debtors, (amount, person))  # min heap

    while creditors and debtors:
        credit_amount, creditor = heappop(creditors)
        debit_amount, debtor = heappop(debtors)
        settle_amount = min(-credit_amount, -debit_amount)

        transactions.append({
            'from_user': debtor,
            'to_user': creditor,
            'amount': round(settle_amount, 2)
        })

        if -credit_amount > settle_amount:
            heappush(creditors, (credit_amount + settle_amount, creditor))
        if -debit_amount > settle_amount:
            heappush(debtors, (debit_amount + settle_amount, debtor))

    return render(request, 'dashboard/settle.html', {
        'balances': balances,
        'transactions': transactions
    })
