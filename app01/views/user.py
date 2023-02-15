# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/01/28
# @File : user.py


from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01 import models

from app01.utls.pagination import Pagination

from app01.utls.forms import UserModelForm, PrettyModelForm, PrettyEditModelForm


def user_list(request):
    """用户列表"""
    queryset = models.UserInfo.objects.all()

    # 获取数据
    # for obj in queryset:
    #     # print(obj.id,obj.name,obj.account,obj.create_time.strftime('%Y-%m-%d'),obj.get_gender_display())
    #     title = obj.depart.title  # 获取关联表的一行数据对象。
    #     print(obj.name,title)
    return render(request, 'user_list.html', {'queryset': queryset})


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # models.UserInfo.objects.create(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'user_add.html', {'form': form})


# 用户编辑
def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    # 数据校验
    if form.is_valid():
        form.save()
        return redirect('/user/list')
    # 校验失败
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request):
    nid = request.GET.get('nid')
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')
