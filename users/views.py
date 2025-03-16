from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def profile_view(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

def signup_view(request):
     if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile after signup
     else:
        form = CustomUserCreationForm()
     return render(request, 'signup.html', {'form': form})

def login_view(request):
     if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile after signup
     else:
        form = AuthenticationForm()
     return render(request, 'login.html', {'form': form})