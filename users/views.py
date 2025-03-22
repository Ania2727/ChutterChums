from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from forums.models import Forum

@login_required
def profile_view(request):
    # Get forums created by the user
    created_forums = Forum.objects.filter(creator=request.user)

    # Get forums the user has joined
    joined_forums = Forum.objects.filter(members=request.user)

    # Get user's recent chat messages
    from forums.models import Chat
    recent_chats = Chat.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'created_forums': created_forums,
        'joined_forums': joined_forums,
        'recent_chats': recent_chats,
    }
    return render(request, 'profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile')  # Redirect to profile after signup
        else:
            print(form.errors)
            # Debug output goes here
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:profile')
        else:
            print(form.errors)
            # Debug output goes here
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
