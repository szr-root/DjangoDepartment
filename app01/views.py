from django.shortcuts import render, redirect
from app01 import models


# Create your views here.

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


def user_list(request):
    """用户列表"""
    queryset = models.UserInfo.objects.all()

    # 获取数据
    # for obj in queryset:
    #     # print(obj.id,obj.name,obj.account,obj.create_time.strftime('%Y-%m-%d'),obj.get_gender_display())
    #     title = obj.depart.title  # 获取关联表的一行数据对象。
    #     print(obj.name,title)
    return render(request, 'user_list.html', {'queryset': queryset})


# formmodel
from django import forms


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']
        # widgets = {
        #     "name":forms.TextInput(attrs={"class": "form-control"})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            #     field.widgets.attrs = {"class": "form-control"}


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
        print(form.errors)
