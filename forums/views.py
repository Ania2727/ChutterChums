from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from forums.forms import *
from forums.models import *


@login_required
def user_forums(request):
    # Show all forums
    forums = Forum.objects.all().order_by('-date_posted')

    # Get forums the user has joined
    user_fs = Forum.objects.filter(members=request.user)

    # Get discussions (using prefetch_related would be more efficient in production)
    discussions = []
    for f in forums:
        discussions.append(f.chat_set.all().order_by('-created_at')[:5])  # Get latest 5 chats

    context = {
        'forums': forums,
        'count': forums.count(),
        'discussions': discussions,
        'user_forums': user_fs
    }
    return render(request, 'user_forums.html', context)


@login_required
def forum(request, forum_name):
    try:
        # First try to determine if it already exists by title
        forum_obj = Forum.objects.filter(title__iexact=forum_name).first()
        if not forum_obj:
            # If not, try to find by ID if forum_name is a number
            if forum_name.isdigit():
                forum_obj = Forum.objects.filter(id=int(forum_name)).first()

        if not forum_obj:
            raise Http404(f"Forum '{forum_name}' does not exist")

        # Check if user is a member
        is_member = request.user in forum_obj.members.all()

        # Get all chat discussions for this forum ordered by newest first
        discussions = forum_obj.chat_set.all().order_by('-created_at')

        context = {
            'forum': forum_obj,
            'discussions': discussions,
            'is_member': is_member
        }
        return render(request, 'forum.html', context)
    except Exception as e:
        raise Http404(f"Error retrieving forum: {str(e)}")


@login_required
def add_forum(request):
    if request.method == 'POST':
        form = CreateInForum(request.POST, user=request.user)
        if form.is_valid():
            f = form.save()
            return redirect('forums:forum', forum_name=f.title)
    else:
        form = CreateInForum(user=request.user)

    context = {'form': form}
    return render(request, 'addForum.html', context)


@login_required
def add_chat(request, forum_id=None):
    forum_instance = None
    if forum_id:
        forum_instance = get_object_or_404(Forum, id=forum_id)
        # Check if user is a member of the forum
        if request.user not in forum_instance.members.all():
            return redirect('join_forum', forum_id=forum_id)

    if request.method == 'POST':
        form = CreateInChat(request.POST, user=request.user)
        if form.is_valid():
            chat = form.save()
            return redirect('forums:forum', forum_name=chat.forum.title)
    else:
        initial_data = {}
        if forum_instance:
            initial_data = {'forum': forum_instance}
        form = CreateInChat(user=request.user, initial=initial_data)
        if forum_instance:
            form.fields['forum'].widget = forms.HiddenInput()

    context = {'form': form, 'forum': forum_instance}
    return render(request, 'addChat.html', context)


@login_required
def join_forum(request, forum_id):
    forum_obj = get_object_or_404(Forum, id=forum_id)

    # Add user to forum members
    forum_obj.members.add(request.user)

    return redirect('forums:forum', forum_name=forum_obj.title)


@login_required
def leave_forum(request, forum_id):
    forum_obj = get_object_or_404(Forum, id=forum_id)

    # Remove user from forum members
    forum_obj.members.remove(request.user)

    return redirect('forums:user_forums')


def home(request):
    # Get 3 forums with the most members
    forums = Forum.objects.annotate(member_count=Count('members')).order_by('-member_count')[:3]
    return render(request, 'home.html', {'forums': forums})

