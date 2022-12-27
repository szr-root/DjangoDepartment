from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01 import models


# Create your views here.
def index(request):
    return render(request, 'index.html')
    # return HttpResponse('Hello!')


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


# formmodel 用户创建
from django import forms


class UserModelForm(forms.ModelForm):
    name = forms.CharField(label='用户名', max_length=6)

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']
        # widgets = {
        #     "name":forms.TextInput(attrs={"class": "form-control"})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
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


def pretty_list(request):
    quertset = models.PrettyNum.objects.all().order_by('-level')
    return render(request, 'pretty_list.html', {'queryset': quertset})


from django.core.validators import RegexValidator


class PrettyModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile','price','level','status']
        # exclude = ['level']  排除某个字段
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def pretty_add(request):
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    return render(request, 'pretty_add.html', {'form': form})
