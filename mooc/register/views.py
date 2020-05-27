from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User as AuthUser
from django.contrib import messages


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')
        else:
            form = RegisterForm()
    
    context = {'form':form }
    return render(request, 'register/register.html', context)