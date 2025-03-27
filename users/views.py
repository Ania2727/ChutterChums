import requests
import json
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.contrib import messages
from forums.models import Forum, Topic, Comment
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from django.http import JsonResponse, HttpResponseRedirect

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
    return render(request, 'users/profile.html', context)

@csrf_protect
@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')  # Or redirect to a goodbye page
    return redirect('users:profile')

@login_required
def settings_view(request):
    return render(request, 'settings.html')

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
            return redirect('users:quiz')  # Redirect to quiz after signup
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
            pass
        storage.used = True

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



def explore_view(request):
    # retrieves recommended forums stored in session
    recommended_forums = request.session.get('recommended_forums', [])
    return render(request, 'explore.html', {'recommended_forums': recommended_forums})



@csrf_exempt
def forum_recommendations(request):
    if request.method == "POST":
        try:
            logger.info("Request body: %s", request.body)
            data = json.loads(request.body)
            selected_interests = data.get("interests", [])

            
            forums = Forum.objects.all()
            logger.info("Forums retrieved: %s", forums)

            
            if not selected_interests:
                return JsonResponse({"success": False, "error": "No interests selected"}, status=400)

            recommended_forums = []
            selected_interests_cleaned = [interest.lower().strip() for interest in selected_interests]
            
            for forum in forums:
                forum_keywords = set(forum.title.lower().split()) 
                common_keywords = set(selected_interests_cleaned) & forum_keywords  
                common_count = len(common_keywords)

                if common_count > 0:  
                    recommended_forums.append({
                        "id": forum.id,
                        "title": forum.title,
                        "description": forum.description,
                        "common_keywords": list(common_keywords),  # Store common keywords for reference
                        "match_score": common_count  # Rank by the number of common keywords
                    })

            recommended_forums = sorted(recommended_forums, key=lambda x: x["match_score"], reverse=True)

            recommended_forums = recommended_forums[:5]

            request.session['recommended_forums'] = recommended_forums

            logger.info("Recommendations: %s", recommended_forums)  

            return JsonResponse({"success": True, "recommendations": recommended_forums})

        except Exception as e:
            logger.error("Error: %s", str(e))  
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def edit_profile_view(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})
