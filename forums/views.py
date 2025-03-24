from django.shortcuts import render, redirect
from django.http import Http404
from forums.forms import *
from django.http import HttpResponse

# Create your views here.
def home(request):
    forums=Forum.objects.all()
    count=forums.count()
    username = request.session.get('username', 'Guest')
    discussions=[]
    for i in forums:
        discussions.append(i.chat_set.all())

     # for cookies
    language = 'en-gb'
    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    context={'forums':forums,
              'count':count,
              'discussions':discussions,
              'username' : username ,
    }

    return render(request,'home.html', context)


def language(request, language = 'en-gb'):
    #to render action into browser window
    response = HttpResponse(f"Setting language to {language}")
    response.set_cookie('lang', language)
    return response

def login_user(request, username):
    request.session['username'] = username
    return HttpResponse(f"Logged in as {username}")

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

