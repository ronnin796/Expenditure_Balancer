# Money Tracker

Money Tracker is a Django-based web application that allows users to track their expenses, categorize them, and settle shared expenses with other users. It supports user authentication, expense categorization, and group expense management.

## Features

- **User Authentication**: Users can sign up, log in, and log out.
- **Expense Tracking**: Users can add, view, and categorize their expenses.
- **Shared Expenses**: Users can share expenses with others and calculate how much they owe or are owed.
- **Expense Settlement**: The app calculates balances and provides a list of transactions to settle shared expenses.

## Project Structure
moneytracker/ ├── category/ # Handles expense categories ├── dashboard/ # Manages expenses and settlements ├── users/ # User authentication and management ├── moneytracker/ # Project settings and configurations ├── db.sqlite3 # SQLite database ├── manage.py # Django management script




### Key Components

#### 1. **Users**
- **Signup and Login**: Users can register and log in using the `SignupForm` and `LoginForm`.
- **Templates**:
  - `signup.html`: User registration form.
  - `loginform.html`: User login form.

#### 2. **Category**
- **Model**: `Category` model stores expense categories.
- **Views**:
  - `index`: Displays the homepage.
  - `category_list`: Lists all categories.
- **Templates**:
  - `index.html`: Base template for the app.
  - `category_list.html`: Displays a list of categories.

#### 3. **Dashboard**
- **Model**: `Expense` model stores expense details, including the payer, amount, category, and shared users.
- **Forms**: `ExpenseForm` allows users to add expenses and select shared users.
- **Views**:
  - `index`: Dashboard homepage.
  - `create_expense`: Add a new expense.
  - `expense_list`: View all expenses.
  - `settle_up`: Calculate balances and transactions for settling shared expenses.
- **Templates**:
  - `create.html`: Form for adding expenses.
  - `list.html`: Displays all expenses.
  - `settle.html`: Shows balances and transactions for settling expenses.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd moneytracker


pipenv install 

Apply migrations:
python manage.py migrate
Run the development server:
python manage.py runserver
Access the app at http://127.0.0.1:8000/.