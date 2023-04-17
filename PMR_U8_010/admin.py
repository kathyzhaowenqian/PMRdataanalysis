from django.contrib import admin
from PMR_U8_010.models import *
from django.db.models import Avg,Sum,Count,Max,Min

class SalesorderdetailInline(admin.TabularInline):
    model = Salesorderdetail
    fk_name = "code"
    extra = 0
    readonly_fields =['code', 'date','deptname','personname','cusname','inventoryname','invstd','unitname','quantity','unitprice','taxunitprice','money','sum']
    fields=['code', 'date','deptname','personname','cusname','inventoryname','invstd','unitname','quantity','unitprice','taxunitprice','money','sum'] 

@admin.register(Salesorderlist)
class SalesorderlistAdmin(admin.ModelAdmin):
    inlines=[SalesorderdetailInline]
    list_per_page = 20
    list_display = ('code', 'date','deptname','personname','cusname','money','sum')
    ordering =('-code','-date')
    fields=['code', 'date','deptname','personname','cusname','money','sum'] 
    readonly_fields=['code', 'date','deptname','personname','cusname','money','sum'] 

@admin.register(Salesorderdetail)
class SalesorderdetailAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display_links =('code',)
    list_per_page = 20
    list_display = ('code', 'date','deptname','personname','cusname','inventoryname','invstd','unitname','quantity','unitprice','taxunitprice','money','sum')
    ordering =('-code','-date')
    search_fields = ['cusname','personname','inventoryname']
    list_filter = ['personname','deptname',]


@admin.register(Consignments)
class ConsignmentsAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display_links =('code',)
    list_per_page = 20
    list_display = ('code', 'date','personname','cusname','inventory_name','invstd','cinvm_unit','totalquantity','totalsum','noinvoiceqty','noinvoicesum',)
    ordering =('-code','-date')
    search_fields = ['cusname','code','inventory_name']
    list_filter = ['free1','deptname','cusname']
    fields=('code', 'date', 'socode','deptname','personname','custcode','cusname','warehouse_name','inventory_code','inventory_name','invstd','batch','cinvm_unit','totalquantity','totalsum','noinvoiceqty','noinvoicesum','free1','define12')


