from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    pwd = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

class RegisterForm(forms.Form):
    username = forms.EmailField(required=True)
    pwd = forms.CharField(required=True)

class ForgetForm(forms.Form):
    username = forms.EmailField(required=True)

class ResetPwdForm(forms.Form):
    username = forms.EmailField(required=True)
    pwd = forms.CharField(required=True)

class ChangePwdForm(forms.Form):
    pwd = forms.CharField(required=True)

class UserInfoForm(forms.Form):
    name = forms.CharField(required=True)
    address = forms.CharField(required=False)
    gender = forms.CharField()

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']