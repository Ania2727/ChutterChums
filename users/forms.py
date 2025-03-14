from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
     email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'email'}), required=True
    )
     username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username'}), required=True
    )
     password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}), required=True
    )
     password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 're-enter password'}), required=True
    )
     class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2'] 

     def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user