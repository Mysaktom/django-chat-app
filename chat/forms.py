from django import forms

class SupportForm(forms.Form):
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Subject of your message'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe your issue or suggestion...', 'rows': 6})
    )