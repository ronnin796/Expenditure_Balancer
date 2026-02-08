"""
Business logic for expense settlement calculations.
"""
from collections import defaultdict
from heapq import heappush, heappop


def calculate_settlement(expenses):
    """
    Calculate balances and minimal settlement transactions from expenses.

    Returns a dict with:
        - balances: {username: net_balance}  # positive = owed money, negative = owes money
        - balance_details: {username: {total_paid, total_share, balance}}
        - transactions: [{from_user, to_user, amount}]
        - transaction_explanations: {index: {from_detail, to_detail, reason}}
    """
    balances = defaultdict(float)
    total_paid = defaultdict(float)
    total_share = defaultdict(float)

    for expense in expenses:
        amount = float(expense.amount)
        payer = expense.payer.username
        shared_users = [u.username for u in expense.shared_with.all()]
        num_users = len(shared_users)

        if num_users == 0:
            continue

        share = amount / num_users

        total_paid[payer] += amount
        for user in shared_users:
            total_share[user] += share
            balances[user] -= share
        balances[payer] += amount

    balances = dict(balances)
    total_paid = dict(total_paid)
    total_share = dict(total_share)

    balance_details = {}
    balance_entries = []
    for user in set(total_paid.keys()) | set(total_share.keys()) | set(balances.keys()):
        paid = total_paid.get(user, 0)
        share = total_share.get(user, 0)
        balance = balances.get(user, 0)
        detail = {
            "total_paid": round(paid, 2),
            "total_share": round(share, 2),
            "balance": round(balance, 2),
        }
        balance_details[user] = detail
        balance_entries.append({"user": user, "amount": balance, **detail})

    creditors = []
    debtors = []
    for person, amount in balances.items():
        if amount > 0:
            heappush(creditors, (-amount, person))
        elif amount < 0:
            heappush(debtors, (amount, person))

    transactions = []
    transaction_explanations = []

    while creditors and debtors:
        credit_amount, creditor = heappop(creditors)
        debit_amount, debtor = heappop(debtors)
        settle_amount = min(-credit_amount, -debit_amount)

        from_detail = balance_details.get(debtor, {})
        to_detail = balance_details.get(creditor, {})

        transactions.append({
            "from_user": debtor,
            "to_user": creditor,
            "amount": round(settle_amount, 2),
            "from_paid": from_detail.get("total_paid", 0),
            "from_share": from_detail.get("total_share", 0),
            "to_paid": to_detail.get("total_paid", 0),
            "to_share": to_detail.get("total_share", 0),
        })

        if -credit_amount > settle_amount:
            heappush(creditors, (credit_amount + settle_amount, creditor))
        if -debit_amount > settle_amount:
            heappush(debtors, (debit_amount + settle_amount, debtor))

    return {
        "balances": balances,
        "balance_details": balance_details,
        "balance_entries": balance_entries,
        "transactions": transactions,
    }
