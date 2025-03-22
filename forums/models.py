from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Parent Post
class Forum(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_forums')
    name = models.CharField(max_length=50, default="Anonymous")
    link = models.CharField(max_length=100, null=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=750, blank=True)
    members = models.ManyToManyField(User, related_name='joined_forums', blank=True)

    def __str__(self):
        return str(self.title)


# Child Post
class Chat(models.Model):
    forum = models.ForeignKey(Forum, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=750)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.forum.title}"
