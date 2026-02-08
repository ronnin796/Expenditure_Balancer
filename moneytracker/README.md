# ExpenseTracker

A Django web application for tracking shared expenses and settling up between friends, roommates, or groups. Split bills, track who paid what, and see exactly who owes whom—with clear explanations for every transaction.

## Features

- **User Authentication** — Sign up, log in, and log out with a clean, modern UI
- **Expense Tracking** — Add expenses with description, amount, category, and who shared the cost
- **Shared Expenses** — Split expenses equally among selected users; the payer is automatically included
- **Settlement Algorithm** — Calculates minimal transactions to settle everyone up (e.g., instead of A→B and B→C, you get A→C directly)
- **Debt Explanations** — Each settlement transaction includes a "Why?" breakdown: who overpaid vs underpaid, with paid/share amounts
- **Balance Breakdown** — See per-person: total paid, fair share, and net balance (owed/owing)
- **Categories** — Organize expenses by category
- **Responsive UI** — Works on desktop and mobile with Tailwind CSS and Alpine.js

## Tech Stack

- **Backend:** Django 6.x
- **Frontend:** Tailwind CSS, Alpine.js
- **Database:** SQLite (default)
- **Package Manager:** uv (or pip)

## Project Structure

```
moneytracker/
├── category/          # Expense categories, home page
│   ├── models.py      # Category model
│   ├── views.py
│   └── templates/
├── dashboard/         # Core expense & settlement logic
│   ├── models.py      # Expense model
│   ├── forms.py       # ExpenseForm
│   ├── views.py       # Dashboard, create, list, settle views
│   ├── services.py    # Settlement calculation (balances, transactions)
│   └── templates/
├── users/             # Authentication
│   ├── forms.py       # LoginForm, SignupForm
│   ├── views.py
│   └── templates/
├── moneytracker/      # Project settings
│   ├── settings.py
│   └── urls.py
├── templates/         # Base template
├── manage.py
├── pyproject.toml
└── README.md
```

### Key Components

| Module | Purpose |
|--------|---------|
| `dashboard/services.py` | `calculate_settlement()` — computes balances, balance details (paid/share), and minimal settlement transactions from expenses |
| `dashboard/views.py` | Thin views that delegate business logic to services |
| `dashboard/forms.py` | `ExpenseForm` with shared_with checkboxes, category select |

## Installation

### Prerequisites

- Python 3.14+ (or 3.10+)
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Steps

1. **Clone the repository and enter the project:**
   ```bash
   git clone <repository-url>
   cd Expenditure_Balancer/moneytracker
   ```

2. **Install dependencies (with uv):**
   ```bash
   uv sync
   ```

   Or with pip:
   ```bash
   pip install django
   ```

3. **Run migrations:**
   ```bash
   uv run python manage.py migrate
   ```

4. **Create a superuser (optional, for admin):**
   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Start the development server:**
   ```bash
   uv run python manage.py runserver
   ```

6. **Open the app:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage

1. **Sign up** — Create an account at `/users/signup/`
2. **Add expenses** — Go to Dashboard → Add Expense. Enter description, amount, category, and select who shared the cost (including yourself via "Shared with")
3. **View expenses** — See all expenses in a table with date, description, category, amount, payer, and shared users. "(you)" badges highlight your involvement.
4. **Settle up** — Go to Settle Up to see:
   - **Balances:** Each person's paid amount, fair share, and net balance
   - **Transactions:** Minimal list of who pays whom how much
   - **Why?** — Expandable explanation for each transaction (overpaid vs underpaid)

## How Settlement Works

- **Balance** = What you paid − Your fair share of all group expenses
- **Positive balance** → You're owed money (you overpaid)
- **Negative balance** → You owe money (you underpaid)
- The algorithm produces the **minimum number of payments** to settle everyone (e.g., if A owes B and B owes C, it simplifies to A owes C when amounts allow).

## Configuration

- `LOGIN_URL` — Where unauthenticated users are sent (default: `/users/login/`)
- `LOGIN_REDIRECT_URL` — Where users go after login (default: `dashboard:index`)
- Database: Edit `moneytracker/settings.py` for PostgreSQL, MySQL, etc.

## License

MIT (or your preferred license)
