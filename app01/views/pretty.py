# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/01/28
# @File : pretty.py
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01 import models

from app01.utls.pagination import Pagination

from app01.utls.forms import UserModelForm, PrettyModelForm, PrettyEditModelForm


def pretty_list(request):
    data_dict = {}
    search_data = request.GET.get('q', '')

    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')
    page_object = Pagination(request, queryset=queryset, search_data=search_data)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    return render(request, 'pretty_add.html', {'form': form})


def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row_object)
        # form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list')
