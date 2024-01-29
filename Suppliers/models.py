
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

#================================================================




class XEY_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='徐二院')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"XEY_Supplier_Product_Summary'
        verbose_name_plural = '徐二院供应商销量明细'
    def __str__(self):
        return self.supplier
    

class XEY_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='徐二院')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"XEY_Product_Rank'
        verbose_name_plural = '徐二院产品排行'
    def __str__(self):
        return self.productname
    


#================================================================


class NQ_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='南桥')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"NQ_Supplier_Rank'
        verbose_name_plural = '南桥供应商销量排行'
    def __str__(self):
        return self.supplier



class NQ_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('NQ_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='南桥')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"NQ_Supplier_Product_Summary'
        verbose_name_plural = '南桥供应商销量明细'
    def __str__(self):
        return self.supplier
    

class NQ_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='南桥')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"NQ_Product_Rank'
        verbose_name_plural = '南桥产品排行'
    def __str__(self):
        return self.productname
    
#================================================================



class PZX_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='普中心')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"PZX_Supplier_Rank'
        verbose_name_plural = '普中心供应商采购排行'
    def __str__(self):
        return self.supplier



class PZX_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('PZX_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='普中心')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"PZX_Supplier_Product_Summary'
        verbose_name_plural = '普中心供应商采购明细'
    def __str__(self):
        return self.supplier
    

class PZX_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='普中心')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"PZX_Product_Rank'
        verbose_name_plural = '普中心产品排行'
    def __str__(self):
        return self.productname

#================================================================



class XINYI_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='新沂')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"XINYI_Supplier_Rank'
        verbose_name_plural = '新沂供应商采购排行'
    def __str__(self):
        return self.supplier



class XINYI_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('XINYI_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='新沂')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"XINYI_Supplier_Product_Summary'
        verbose_name_plural = '新沂供应商采购明细'
    def __str__(self):
        return self.supplier
    

class XINYI_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='新沂')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"XINYI_Product_Rank'
        verbose_name_plural = '新沂产品排行'
    def __str__(self):
        return self.productname
    
    #================================================================



class PIZHOU_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='邳州')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"PIZHOU_Supplier_Rank'
        verbose_name_plural = '邳州供应商采购排行'
    def __str__(self):
        return self.supplier



class PIZHOU_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('PIZHOU_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='邳州')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"PIZHOU_Supplier_Product_Summary'
        verbose_name_plural = '邳州供应商采购明细'
    def __str__(self):
        return self.supplier
    

class PIZHOU_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='邳州')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"PIZHOU_Product_Rank'
        verbose_name_plural = '邳州产品排行'
    def __str__(self):
        return self.productname
    

    #================================================================



class ANTING_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='安亭')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"ANTING_Supplier_Rank'
        verbose_name_plural = '安亭供应商采购排行'
    def __str__(self):
        return self.supplier



class ANTING_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('ANTING_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='安亭')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"ANTING_Supplier_Product_Summary'
        verbose_name_plural = '安亭供应商采购明细'
    def __str__(self):
        return self.supplier
    

class ANTING_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='安亭')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"ANTING_Product_Rank'
        verbose_name_plural = '安亭产品排行'
    def __str__(self):
        return self.productname
    
    #================================================================



class QIXIAN_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='齐贤')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"QIXIAN_Supplier_Rank'
        verbose_name_plural = '齐贤供应商采购排行'
    def __str__(self):
        return self.supplier



class QIXIAN_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('QIXIAN_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='齐贤')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"QIXIAN_Supplier_Product_Summary'
        verbose_name_plural = '齐贤供应商采购明细'
    def __str__(self):
        return self.supplier
    

class QIXIAN_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='齐贤')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"QIXIAN_Product_Rank'
        verbose_name_plural = '齐贤产品排行'
    def __str__(self):
        return self.productname
    


    #================================================================



class SHENYANG_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='申养')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"SHENYANG_Supplier_Rank'
        verbose_name_plural = '申养供应商采购排行'
    def __str__(self):
        return self.supplier



class SHENYANG_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('SHENYANG_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='申养')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"SHENYANG_Supplier_Product_Summary'
        verbose_name_plural = '申养供应商采购明细'
    def __str__(self):
        return self.supplier
    

class SHENYANG_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='申养')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"SHENYANG_Product_Rank'
        verbose_name_plural = '申养产品排行'
    def __str__(self):
        return self.productname
    
    #================================================================



class SITUAN_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='四团')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"SITUAN_Supplier_Rank'
        verbose_name_plural = '四团供应商采购排行'
    def __str__(self):
        return self.supplier



class SITUAN_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('SITUAN_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='四团')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"SITUAN_Supplier_Product_Summary'
        verbose_name_plural = '四团供应商采购明细'
    def __str__(self):
        return self.supplier
    

class SITUAN_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='四团')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"SITUAN_Product_Rank'
        verbose_name_plural = '四团产品排行'
    def __str__(self):
        return self.productname
    

    #================================================================



class TINGLIN_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='亭林')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"TINGLIN_Supplier_Rank'
        verbose_name_plural = '亭林供应商采购排行'
    def __str__(self):
        return self.supplier



class TINGLIN_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('TINGLIN_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='亭林')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"TINGLIN_Supplier_Product_Summary'
        verbose_name_plural = '亭林供应商采购明细'
    def __str__(self):
        return self.supplier
    

class TINGLIN_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='亭林')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"TINGLIN_Product_Rank'
        verbose_name_plural = '亭林产品排行'
    def __str__(self):
        return self.productname
    
    #================================================================



class XIDU_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='西渡')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"XIDU_Supplier_Rank'
        verbose_name_plural = '西渡供应商采购排行'
    def __str__(self):
        return self.supplier



class XIDU_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('XIDU_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='西渡')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"XIDU_Supplier_Product_Summary'
        verbose_name_plural = '西渡供应商采购明细'
    def __str__(self):
        return self.supplier
    

class XIDU_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='西渡')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"XIDU_Product_Rank'
        verbose_name_plural = '西渡产品排行'
    def __str__(self):
        return self.productname
    
    #================================================================



class ZHIXIAO_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='直销')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"ZHIXIAO_Supplier_Rank'
        verbose_name_plural = '直销供应商采购排行'
    def __str__(self):
        return self.supplier



class ZHIXIAO_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('ZHIXIAO_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='直销')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"ZHIXIAO_Supplier_Product_Summary'
        verbose_name_plural = '直销供应商采购明细'
    def __str__(self):
        return self.supplier
    

class ZHIXIAO_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='直销')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"ZHIXIAO_Product_Rank'
        verbose_name_plural = '直销产品排行'
    def __str__(self):
        return self.productname
    

    #================================================================



class NANXIANG_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='南翔')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"NANXIANG_Supplier_Rank'
        verbose_name_plural = '南翔供应商采购排行'
    def __str__(self):
        return self.supplier



class NANXIANG_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('NANXIANG_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='南翔')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"NANXIANG_Supplier_Product_Summary'
        verbose_name_plural = '南翔供应商采购明细'
    def __str__(self):
        return self.supplier
    

class NANXIANG_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='南翔')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"NANXIANG_Product_Rank'
        verbose_name_plural = '南翔产品排行'
    def __str__(self):
        return self.productname
    
    #================================================================



class SIWUWU_Supplier_Rank(models.Model):
    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='四五五')
    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"SIWUWU_Supplier_Rank'
        verbose_name_plural = '四五五供应商采购排行'
    def __str__(self):
        return self.supplier



class SIWUWU_Supplier_Product_Summary(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    supplierrank = models.ForeignKey('SIWUWU_Supplier_Rank', models.CASCADE, db_column='supplierrank',to_field='id',verbose_name= '供应商排行表')
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
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='四五五')

    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"SIWUWU_Supplier_Product_Summary'
        verbose_name_plural = '四五五供应商采购明细'
    def __str__(self):
        return self.supplier
    

class SIWUWU_Product_Rank(models.Model):
    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    recentdate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    project = models.CharField(verbose_name= '项目',max_length=255, default='四五五')
    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"SIWUWU_Product_Rank'
        verbose_name_plural = '四五五产品排行'
    def __str__(self):
        return self.productname
    

#================================================================

class Total_Supplier_Rank(models.Model):
    # id = models.BigAutoField(primary_key=True)

    rank = models.SmallIntegerField(verbose_name= '排行',null=False)
    project = models.CharField(verbose_name= '项目',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)

    
    class Meta:
        managed=False
        db_table = 'SUPPLIERS\".\"supplierrankcombine'
        verbose_name_plural = '所有项目供应商采购排行'
    def __str__(self):
        return self.supplier



class Total_Product_Rank(models.Model):
    # id = models.BigAutoField(primary_key=True)

    rank = models.BigIntegerField(verbose_name= '排行',null=False)
    project = models.CharField(verbose_name= '项目',max_length=255)
    productcode = models.CharField(verbose_name= '产品编码',max_length=255)
    productname = models.CharField(verbose_name= '产品名称',max_length=255)
    spec = models.CharField(verbose_name= '规格',max_length=255)
    unit = models.CharField(verbose_name= '单位',max_length=255)
    supplier = models.CharField(verbose_name= '供应商',max_length=255)
    brand = models.CharField(verbose_name= '品牌',max_length=255)
    invoicedate = models.DateField(verbose_name= '最近发票日期')
    price = models.DecimalField(verbose_name= '单价',max_digits=25, decimal_places=2)
    qty21 = models.DecimalField(verbose_name= '21年数量',max_digits=25, decimal_places=2, null=True) 
    qty22 = models.DecimalField(verbose_name= '22年数量',max_digits=25, decimal_places=2, null=True)
    qty23 = models.DecimalField(verbose_name= '23年数量',max_digits=25, decimal_places=2, null=True)
    qty24 = models.DecimalField(verbose_name= '24年数量',max_digits=25, decimal_places=2, default=0)
    totalqty = models.DecimalField(verbose_name= '总数量',max_digits=25, decimal_places=2, null=True)
    sum21 = models.DecimalField(verbose_name= '21年采购额',max_digits=25, decimal_places=2, null=True)
    sum22 = models.DecimalField(verbose_name= '22年采购额',max_digits=25, decimal_places=2, null=True)
    sum23 = models.DecimalField(verbose_name= '23年采购额',max_digits=25, decimal_places=2, null=True)
    sum24 = models.DecimalField(verbose_name= '24年采购额',max_digits=25, decimal_places=2, default=0)
    totalsum = models.DecimalField(verbose_name= '总采购额',max_digits=25, decimal_places=2, null=True)

    
    class Meta:
        managed=False
        db_table ='SUPPLIERS\".\"productrankcombine'
        verbose_name_plural = '所有项目产品排行'

    def __str__(self):
        return self.productname    