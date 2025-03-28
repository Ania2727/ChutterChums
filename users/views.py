import json
import logging
import os
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from forums.models import Forum, Topic, Comment, Tag
from .forms import CustomUserCreationForm, UserProfileForm

logger = logging.getLogger(__name__)


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


@csrf_protect
@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user

        # Delete profile picture if it exists
        if hasattr(user, 'userprofile') and user.userprofile.profile_pic:
            try:
                # Get the file path
                profile_pic_path = user.userprofile.profile_pic.path

                # Delete the profile picture from storage
                if os.path.isfile(profile_pic_path):
                    os.remove(profile_pic_path)
                    logger.info(f"Deleted profile picture for user {user.username}")
            except Exception as e:
                logger.error(f"Error deleting profile picture for user {user.username}: {str(e)}")

        logout(request)
        user.delete()
        return redirect('home')  # Or redirect to a goodbye page
    return redirect('users:profile')


def settings_view(request):
    # Get the current theme from cookie or default to 'light'
    current_theme = request.COOKIES.get('theme', 'light')

    # Added in some AJAX to try and get dark mode working properly
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if 'theme' in request.GET:
        theme = request.GET.get('theme', 'light')

        if is_ajax:
            response = JsonResponse({'success': True, 'theme': theme})
            response.set_cookie('theme', theme, httponly=True, secure=True, max_age=31536000)
            return response

        response = render(request, 'settings.html', {'current_theme': theme})
        response.set_cookie('theme', theme, httponly=True, secure=True, max_age=31536000)
        return response

    return render(request, 'settings.html', {'current_theme': current_theme})


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

            # 2-Week Cookie
            request.session.set_expiry(1209600)

            return redirect('users:quiz')
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

    # Clear saved error messages on GET
    if request.method == 'GET':
        storage = messages.get_messages(request)
        for message in storage:
            pass  # Iterating through all the messages marks them as read
        storage.used = True  # Mark the storage as processed

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Starts session for user

            # Check if 'remember_me' was checked in POST data
            remember_me = request.POST.get('remember_me', False)
            if remember_me:
                request.session.set_expiry(1209600)  # Set session expiry to 2 weeks
            else:
                request.session.set_expiry(0)  # Session expires on browser close

            return redirect('users:profile')  # Redirect after successful login
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


# users/views.py
def quiz_view(request):
    tags = Tag.objects.all().order_by('name')
    return render(request, 'quiz.html', {'tags': tags})


# users/views.py
def explore_view(request):
    recommended_forums = []

    if request.user.is_authenticated:
        try:
            # Access interests through the userprofile
            user_interests = request.user.userprofile.interests.all()

            if user_interests:
                # Find forums with matching tags
                forums = Forum.objects.filter(tags__in=user_interests).distinct()

                # Convert to list of dictionaries for template
                for forum in forums:
                    common_tags = forum.tags.filter(id__in=user_interests.values_list('id', flat=True))
                    recommended_forums.append({
                        "id": forum.id,
                        "title": forum.title,
                        "description": forum.description,
                        "common_tags": list(common_tags.values_list('name', flat=True)),
                        "match_score": common_tags.count()
                    })

                # Sort by number of matching tags (match score)
                recommended_forums = sorted(recommended_forums, key=lambda x: x["match_score"], reverse=True)
                recommended_forums = recommended_forums[:5]
        except AttributeError:
            # Handle case where user doesn't have a profile or interests
            pass

    # If no recommendations or not logged in, use session-based recommendations
    if not recommended_forums:
        recommended_forums = request.session.get('recommended_forums', [])

    return render(request, 'explore.html', {'recommended_forums': recommended_forums})


@login_required
def save_interests(request):
    if request.method == 'POST':
        # Get the selected interest IDs from the form
        interest_ids = request.POST.getlist('interests')

        # Get the current user profile
        user_profile = request.user.userprofile

        # Save interests
        user_profile.interests.clear()
        for interest_id in interest_ids:
            try:
                tag = Tag.objects.get(id=interest_id)
                user_profile.interests.add(tag)
            except Tag.DoesNotExist:
                pass  # Skip if tag doesn't exist

        # Redirect to explore page
        return redirect('users:explore')

    # If not a POST request, redirect to the quiz
    return redirect('users:quiz')


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

        # Check if the user is removing their profile picture
        if 'profile_pic-clear' in request.POST and request.POST['profile_pic-clear'] == 'on':
            # Delete the old profile picture if it exists
            if profile.profile_pic:
                try:
                    # Get the file path
                    profile_pic_path = profile.profile_pic.path

                    # Clear the field first (important to do this before deleting the file)
                    profile.profile_pic = None
                    profile.save()

                    # Delete the file if it exists
                    if os.path.isfile(profile_pic_path):
                        os.remove(profile_pic_path)
                        logger.info(f"Deleted profile picture for user {request.user.username}")
                except Exception as e:
                    logger.error(f"Error deleting profile picture for user {request.user.username}: {str(e)}")

        # Check if user is replacing their profile picture
        elif 'profile_pic' in request.FILES and profile.profile_pic:
            try:
                # Get the old file path
                old_pic_path = profile.profile_pic.path

                # Check if old file exists and delete it
                if os.path.isfile(old_pic_path):
                    os.remove(old_pic_path)
                    logger.info(f"Deleted old profile picture for user {request.user.username}")
            except Exception as e:
                logger.error(f"Error deleting old profile picture for user {request.user.username}: {str(e)}")

        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})