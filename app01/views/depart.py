# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/01/28
# @File : depart.py

from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01 import models

from app01.utls.pagination import Pagination

from app01.utls.forms import UserModelForm, PrettyModelForm, PrettyEditModelForm


def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """添加部门 """
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    # 获取数据（如果为空，后面再判断）
    title = request.POST.get('title')
    # 保存数据
    models.Department.objects.create(title=title)

    # 重定向
    return redirect('/depart/list/')


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()

    return redirect('/depart/list/')


def depart_edit(request, nid):
    """编辑部门"""
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()

        # title = row_object.title

        return render(request, 'depart_edit.html', {'row_object': row_object})

    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')
