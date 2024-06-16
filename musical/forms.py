# forms.py
from django import forms
from .models import Users
class SignupForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['user_id', 'user_email', 'user_password', 'user_phone', 'user_address', 'user_nickname']
        widgets = {
            'user_password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    user_id = forms.CharField(label='User ID', max_length=50)
    user_password = forms.CharField(label='Password', widget=forms.PasswordInput)
