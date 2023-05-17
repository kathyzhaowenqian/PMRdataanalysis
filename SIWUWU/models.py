from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.forms import Textarea
from django_pandas.managers import DataFrameManager
from multiselectfield import MultiSelectField
from Marketing_Research.models import UserInfo


def get_compmany_default_value():
    return Company.objects.get(id=8).company

class SWWUserInfo(UserInfo):   
    
    class Meta:
        proxy =True
        managed=False
        db_table =  'django_admin_v2\".\"auth_user'
        verbose_name = "用户"
        verbose_name_plural = "用户表"

    def __str__(self):
        if self.chinesename:
            # 如果不为空则返回中文用户名
            return self.chinesename
        else:
            # 如果用户名为空则返回不能为空的对象
            return self.username

class SWWSalesmanPosition(models.Model):
    # id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('SWWUserInfo', models.CASCADE, db_column='user',to_field='id') #settings.AUTH_USER_MODEL
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    position = models.CharField(verbose_name='岗位',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"SalesmanPosition'
        verbose_name_plural = '员工职位列表'



class Company(models.Model):
    # id = models.BigAutoField(primary_key=True)
    company = models.CharField(verbose_name='公司',max_length=255, blank=True, null=True,)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"Company'
        # verbose_name = '公司列表'
        verbose_name_plural = '公司列表'

    def __str__(self):
            return self.company
    
    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_active = False
        self.save()

class SWWSPDList(models.Model):
    # id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    salesman = models.ForeignKey('SWWUserInfo', models.CASCADE, db_column='salesman',to_field='id',related_name='salesmanSWW',verbose_name= '负责人')

    supplier = models.CharField(verbose_name='供应商',max_length=255, blank=True, null=True)
    brand = models.CharField(verbose_name='品牌',max_length=255, blank=True, null=True)
    department = models.CharField(verbose_name='科室',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品',max_length=255, blank=True, null=True)
    machinemodel = models.CharField(verbose_name='仪器型号',max_length=255, blank=True, null=True)
    listotal = models.DecimalField(verbose_name='LIS收入',max_digits=25, decimal_places=2, blank=True, null=True)
    salestotal = models.DecimalField(verbose_name='年开票额',max_digits=25, decimal_places=2, blank=True, null=True)
    salestotalpercent = models.DecimalField(verbose_name='开票占比',max_digits=25, decimal_places=6, blank=True, null=True)
    purchasetotal = models.DecimalField(verbose_name='年采购额',max_digits=25, decimal_places=2, blank=True, null=True)
    gppercent = models.DecimalField(verbose_name='毛利率',max_digits=25, decimal_places=6, blank=True, null=True)
    relation = models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)

    operator = models.ForeignKey('SWWUserInfo', models.CASCADE, db_column='operator',to_field='id',related_name='operatorSWW',verbose_name= '最后操作人')   
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    
    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"SPDList'
        verbose_name_plural = 'SPD战略地图'
    
    def __str__(self):
        return self.supplier


