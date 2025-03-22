from django.forms import ModelForm
from forums.models import *
from django import forms


class CreateInForum(ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description', 'link', 'name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateInForum, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateInForum, self).save(commit=False)
        if self.user:
            instance.creator = self.user
        if commit:
            instance.save()
            # Add the creator as a member automatically
            instance.members.add(self.user)
        return instance


class CreateInChat(ModelForm):
    class Meta:
        model = Chat
        fields = ['forum', 'discuss']
        widgets = {
            'discuss': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Start a conversation...'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateInChat, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateInChat, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance