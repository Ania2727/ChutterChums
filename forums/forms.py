from django.forms import ModelForm
from forums.models import *

class CreateInForum(ModelForm):
    class Meta:
        model = Forum
        fields = "__all__"

class CreateInChat(ModelForm):
    class Meta:
        model = Chat
        fields = "__all__"