from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('dashboard:index')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})





