from django import forms

from user.models import UserMsg

from django.contrib.auth import get_user_model

Sys_User = get_user_model()


# 注册
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'max_length': '输入2~8字符',
        'min_length': '输入2~8字符',
        'required': '请输入用户名',
    })
    password = forms.CharField(max_length=11)
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': "邮箱格式有误！"})


# 登录
class LoginForm(forms.Form):
    password = forms.CharField(max_length=11)
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': "邮箱格式有误！"})


