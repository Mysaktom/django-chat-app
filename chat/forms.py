from django import forms
from django.contrib.auth.models import User 

class SupportForm(forms.Form):
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Subject of your message'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe your issue or suggestion...', 'rows': 6})
    )

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User # Říkáme, že tento formulář pracuje s modelem User
        fields = ['email'] # Chceme upravovat pouze pole 'email'