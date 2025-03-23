from django.urls import path
from .views import *

app_name = 'users' 

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('quiz/', quiz_view, name='quiz'),
    path("recommendations/", get_forum_recommendations, name="forum-recommendations"),
]
