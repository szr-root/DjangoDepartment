# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/02/15
# @File : account.py

from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

# from app01.utls.code import check_code
from app01 import models
from app01.utls.btform import BootStrapForm
from app01.utls.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
