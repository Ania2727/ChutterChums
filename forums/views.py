from django.shortcuts import render, redirect
from django.http import Http404
from forums.forms import *

# Create your views here.
def home(request):
    forums=Forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.chat_set.all())

    context={'forums':forums,
              'count':count,
              'discussions':discussions
    }
    return render(request,'home.html', context)


def forum(request, forum_name):
    try:
        # First try to determine if it already exists by title

        forum_1 = Forum.objects.filter(title__iexact=forum_name).first()
        if not forum_1:
            # If not, try to find by ID if forum_name is a number
            if forum_name.isdigit():
                forum_1 = Forum.objects.filter(id=int(forum_name)).first()

        if not forum_1:
            raise Http404(f"Forum '{forum_name}' does not exist")

        # Get all chat discussions for this forum
        discussions = forum_1.chat_set.all()

        context = {
            'forum': forum_1,
            'discussions': discussions
        }
        return render(request, 'forum.html', context)
    except Exception as e:
        raise Http404(f"Error retrieving forum: {str(e)}")

def add_forum(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={'form':form}
    return render(request, 'addForum.html', context)

def add_chat(request):
    form = CreateInChat()
    if request.method == 'POST':
        form = CreateInChat(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={'form':form}
    return render(request, 'addChat.html', context)

