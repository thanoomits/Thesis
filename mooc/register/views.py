from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User as AuthUser
from django.contrib import messages
from django.contrib.auth import authenticate,login
from catalog.models import UserBadge, User, Badges

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                user = form.cleaned_data.get('username')
                messages.info(request, "Thanks for registering. You are now logged in as " + user)
                new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
                login(request, new_user)

                return redirect('index')
        else:
            form = RegisterForm()
    
    context = {'form':form }
    return render(request, 'register/register.html', context)