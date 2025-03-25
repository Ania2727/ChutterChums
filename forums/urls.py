from django.urls import path
from . import views

app_name = 'forums'

urlpatterns = [
    # Forum URLs
    path('', views.forum_list, name='forum_list'),
    path('user-forums/', views.user_forums, name='user_forums'),
    path('add-forum/', views.add_forum, name='add_forum'),
    path('<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('<int:forum_id>/join/', views.join_forum, name='join_forum'),
    path('<int:forum_id>/leave/', views.leave_forum, name='leave_forum'),

    # Topic URLs
    path('<int:forum_id>/create-topic/', views.create_topic, name='create_topic'),
    path('<int:forum_id>/topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('<int:forum_id>/topic/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),

    # Comment URLs
    path('<int:forum_id>/topic/<int:topic_id>/add-comment/', views.add_comment, name='add_comment'),
    path('<int:forum_id>/topic/<int:topic_id>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
]
