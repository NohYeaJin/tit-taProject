# forms.py
from django import forms
from .models import Users
from django.contrib.auth.forms import AuthenticationForm
class SignupForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['user_id', 'user_email', 'user_password', 'user_phone', 'user_address', 'user_nickname']
        widgets = {
            'user_password': forms.PasswordInput(),  # 비밀번호 입력 시에는 비밀번호 형태로 보이도록 설정
        }

class LoginForm(AuthenticationForm):
    pass