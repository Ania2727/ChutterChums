from django.db import models

# Parent Post
class Forum(models.Model):
    name = models.CharField(max_length=50, default="Anonymous")
    link = models.CharField(max_length=100, null=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=750, blank=True)

    def __str__(self):
        return str(self.title)


# Child Post
class Chat(models.Model):
    forum = models.ForeignKey(Forum, blank=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=750)

    def __str__(self):
        return str(self.forum)
