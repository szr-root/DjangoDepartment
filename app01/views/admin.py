# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/02/07
# @File : admin.py
from django.shortcuts import render, redirect

from app01 import models
from app01.utls.pagination import Pagination


def admin_list(request):
    """ 管理员列表 """
    # 搜索
    data_dict = {}
    search_data = request.GET.get('q', '')

    if search_data:
        data_dict["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset, search_data)

    context = {
        'search_data': search_data,
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }

    return render(request, 'admin_list.html', context)


from django import forms
from django.core.exceptions import ValidationError
from app01.utls.btform import BootStrapModelForm
from app01.utls.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput()
        # render_value=True 不一致保留，不清空
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        comfirm = md5(self.cleaned_data.get('confirm_password'))
        if comfirm != pwd:
            raise ValidationError('两次输入的密码不一致')
        # 返回
        return comfirm


def admin_add(request):
    """ 添加管理员 """
    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, 'change.html', {'form': form, 'title': title})


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


def admin_edit(request, nid):
    """ 编辑管理员 """
    # None/obj
    row_objet = models.Admin.objects.filter(id=nid).first()
    if not row_objet:
        # return render(request , '自定义错误.html',{"msg"："自定义错误信息"})
        return redirect('admin/list')

    title = '编辑管理员'

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_objet)
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminEditModelForm(data=request.POST, instance=row_objet)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    """ 删除管理员 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list')


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        # 取数据库校验新输入密码与原密码
        exists = models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError('新密码不能与原密码相同')

        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        comfirm = md5(self.cleaned_data.get('confirm_password'))
        if comfirm != pwd:
            raise ValidationError('两次输入的密码不一致')
        # 返回
        return comfirm

def admin_reset(request, nid):
    """ 管理员重置密码 """
    row_objet = models.Admin.objects.filter(id=nid).first()

    title = '重置管理员{}的密码'.format(row_objet.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST,instance=row_objet)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, 'change.html', {'form': form, 'title': title})


