
# Create your models here.
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.forms import Textarea
from django_pandas.managers import DataFrameManager
from Marketing_Research.models import UserInfo
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField



class SupplierInfo(models.Model):
    supplier = models.CharField(verbose_name='供应商',max_length=255, blank=True, null=True)
    contact = models.CharField(verbose_name='联系方式',max_length=255, blank=True, null=True)
    payterm = models.CharField(verbose_name='账期',max_length=255, blank=True, null=True)
    tax = models.CharField(verbose_name='税率',max_length=255, blank=True, null=True)
    delivery = models.CharField(verbose_name='配送方式',max_length=255, blank=True, null=True)
    project = models.CharField(verbose_name= '项目',max_length=255)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"Supplier_info'
        verbose_name_plural = '供应商基础信息汇总表'
    
    def __str__(self):
        return self.supplier


class XEY_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年销售额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '21年销售额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '21年销售额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '21年销售额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总销售额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='徐二院')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"XEY_Supplier_Rank'
        verbose_name_plural = '徐二院供应商销量排行'
    def __str__(self):
        return self.supplier



class XEY_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('XEY_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    contact = models.CharField(verbose_name= '联系方式',max_length=255)
    payterm = models.CharField(verbose_name= '账期',max_length=255)
    tax = models.CharField(verbose_name= '税率',max_length=255)
    delivery = models.CharField(verbose_name= '配送方式',max_length=255)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年销售额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '21年销售额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '21年销售额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '21年销售额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总销售额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='徐二院')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"XEY_Supplier_Product_Summary'
        verbose_name_plural = '徐二院供应商销量明细'
    def __str__(self):
        return self.supplier