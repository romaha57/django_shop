from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm, ProfileForm
from products.models import Basket


def loginn(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('products:index'))
    else:
        form = LoginForm()
    return render(request, 'app_users/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect(reverse('app_users:login'))
    else:
        form = RegistrationForm

    return render(request, 'app_users/registration.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('app_users:profile'))

    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'app_users/profile.html', {'form': form, 'basket': Basket.objects.filter(user=request.user)})


def logoutt(request):
    logout(request)
    return redirect(reverse('products:index'))