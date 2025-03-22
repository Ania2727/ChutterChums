from django.urls import path
from . import views

app_name = 'forums'

urlpatterns = [
    path('', views.user_forums, name='user_forums'),
    path('add/', views.add_forum, name='add_forum'),
    path('chat/add/', views.add_chat, name='add_chat'),
    path('chat/add/<int:forum_id>/', views.add_chat, name='add_chat_to_forum'),
    path('join/<int:forum_id>/', views.join_forum, name='join_forum'),
    path('leave/<int:forum_id>/', views.leave_forum, name='leave_forum'),
    path('<str:forum_name>/', views.forum, name='forum'),
]
