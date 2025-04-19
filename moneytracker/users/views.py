from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from .forms import SignupForm
# Create your views here.






def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST  )

        if form.is_valid():
            form.save()
            return redirect('dashboard/login/')
    else:
        form = SignupForm()

    return render(request , 'users/signup.html', {'form':form})





