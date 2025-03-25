import requests
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.contrib import messages
from forums.models import Forum, Topic, Comment


@login_required
def profile_view(request):
    created_forums = Forum.objects.filter(creator=request.user)
    joined_forums = Forum.objects.filter(members=request.user).exclude(creator=request.user)
    recent_topics = Topic.objects.filter(author=request.user).order_by('-created_at')[:3]
    recent_comments = Comment.objects.filter(author=request.user).order_by('-created_at')[:5]

    context = {
        'created_forums': created_forums,
        'joined_forums': joined_forums,
        'recent_topics': recent_topics,
        'recent_comments': recent_comments,
    }
    return render(request, 'profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout


def signup_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:quiz')  # Redirect to profile after signup
        else:
            # Non-field errors first
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)

            # Field-specific errors
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form[field].label if field in form.fields else field
                    messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('users:profile')

    # This prevents error messages that are saved from showing.
    if request.method == 'GET':
        storage = messages.get_messages(request)
        for message in storage:
            pass  # Iterating through all the messages marks them as read
        storage.used = True  # Mark the storage as processed

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:profile')
        else:
            # Non-field errors first
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)

            # Field-specific errors
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form[field].label if field in form.fields else field
                    messages.error(request, f"{error}")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def quiz_view(request):
    return render(request, 'quiz.html')

def get_forum_recommendations(request):
    interests = request.GET.getlist("interests") 
    
    response = requests.post("http://localhost:5000/get-recommendations", json={"interests": interests})

    return JsonResponse(response.json())
