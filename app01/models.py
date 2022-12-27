from django.db import models


# Create your models here.
class Department(models.Model):
    """ 部门表 """
    # id = models.BigAutoField(verbose_name='ID', primary_key=True)
    title = models.CharField(verbose_name='部门名', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')

    # -to:与哪张表关联
    # -to_field：与表中哪一列关联

    # 不删除，置空
    # depart = models.ForeignKey(to='Department', to_field='id',null=True,blank=True, on_delete=models.SET_NULL())
    # django自动生成 ,写的depart，自动生成depart_id
    # -on_delete=models.CASCADE :级联删除，部门删除，员工也删除
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', on_delete=models.CASCADE)

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)

    level_choices = (
        (1, '白银'),
        (2, '黄金'),
        (3, '铂金'),
        (4, '钻石')
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)

    status_choices = (
        (1, '已占用'),
        (2, '未占用')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)