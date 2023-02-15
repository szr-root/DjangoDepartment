# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/01/28
# @File : forms.py


from app01 import models
from django import forms

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01.utls.btform import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(label='用户名', max_length=6, widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']


class PrettyModelForm(BootStrapModelForm):
    # 验证方式1：
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile','price','level','status']
        # exclude = ['level']  排除某个字段
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         # print(name, field)
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # # 验证方式2：
    # def clean_mobile(self):
    #     text_mobile = self.cleaned_data['mobile']
    #     # 验证不通过
    #     if len(text_mobile) != 11:
    #         raise ValidationError('格式错误')
    #
    #     # 验证通过，把输入值返回
    #     return text_mobile
    def clean_mobile(self):
        text_mobile = self.cleaned_data['mobile']
        exits = models.PrettyNum.objects.filter(mobile=text_mobile).exists()

        if exits:
            raise ValidationError('手机号已存在')

        return text_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # 验证方式1：
    mobile = forms.CharField(
        disabled=True,  # 设置为仅查看，无法修改
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile','price','level','status']
        # exclude = ['level']  排除某个字段
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         # print(name, field)
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        text_mobile = self.cleaned_data['mobile']
        # 排除自己外，手机号不能重复
        exits = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=text_mobile).exists()

        if exits:
            raise ValidationError('手机号已存在')
        return text_mobile
