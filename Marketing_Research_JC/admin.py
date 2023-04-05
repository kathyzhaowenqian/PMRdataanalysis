from django.contrib import admin

# Register your models here.
from django.contrib import admin
from Marketing_Research_JC.models import *

from django.contrib import admin
# Register your models here.
from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms
from django.db.models import Q
from django.contrib.admin.widgets import AutocompleteSelect
from datetime import date,timedelta,datetime
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from django.core.exceptions import (
    FieldDoesNotExist, FieldError, PermissionDenied, ValidationError,
)
from Marketing_Research.tools.calculate_Quater_target import result_of_Quatar_display,calculate_quarter_start_end_day
from django.db.models import Avg,Sum,Count,Max,Min

from django.contrib.admin import SimpleListFilter


#admin中的delete优先,具体admin中的更优先,针对inline没有用！！！！！
class GlobalAdmin(admin.ModelAdmin):
    def delete_queryset(self,request, queryset):
        print('im in global delete_queryset')
        queryset.update(is_active=False)
        queryset.update(operator=request.user)

    def delete_model(self, request, obj):
        print('im in global delete_model')
        obj.is_active = False 
        obj.operator=request.user
        obj.save()

    def get_queryset(self, request):
        print('im in global get_queryset')
        return super().get_queryset(request).filter(is_active=True)
    


@admin.register(Hospital)  
class HospitalAdmin(GlobalAdmin):   
    search_fields=['hospitalname']
    exclude = ('id','createtime','updatetime','is_active')

    #使得pmrresearchlist中的的autocompletefield被下面的代码过滤
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            queryset=queryset.filter(is_active=True).order_by('id')
        return queryset,use_distinct 


@admin.register(Brand)  
class BrandAdmin(GlobalAdmin):   
    search_fields=['brand']
    exclude = ('id','createtime','updatetime','is_active')
    
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            queryset=queryset.filter(is_active=True).order_by('id')
        return queryset,use_distinct 
    


@admin.register(JCResearchList)
class JCResearchListAdmin(GlobalAdmin):
    exclude = ('id','createtime','updatetime','is_active','operator')
    search_fields=['hospital__hospitalname','brand__brand']
    list_filter = ['hospital__district','hospital__hospitalclass','jcornot']


    list_display_links =('list_hospitalname',)
    empty_value_display = '--'
    list_per_page = 10
    list_display = ('list_district','list_hospitalclass','list_hospitalname','director','sizeofclinicallab','jcornot',
                    'jccompany','jcstartdate','jcenddate','jcmemo','sizeofsystem','brand','systemstartdate','systemenddate','systemmemo','relation',
                    )
    autocomplete_fields=['hospital','brand']
    ordering = ('-id',)


# ------delete_model内层的红色删除键------------------------------
    def delete_model(self, request, obj):
        print('JCJCJC delete_model')
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='JC':             
            obj.is_active = False 
            obj.operator=request.user   
            obj.save()

    def delete_queryset(self,request, queryset):        
            print('我在delete_queryset')
            for delete_obj in queryset:     
                print('delete_queryset delete_obj',delete_obj)                    
                if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='JC':     
                    delete_obj.is_active=False
                    print('list 已假删')
                    delete_obj.operator=request.user
                    delete_obj.save()

    def save_model(self, request, obj, form, change):
        obj.operator = request.user
        super().save_model(request, obj, form, change)

    #只显示未被假删除的项目
    #------get_queryset-----------查询-------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print('我在PMRResearchDetailAdmin-get_queryset')
        #通过外键连list中的负责人名称
        if request.user.is_superuser  or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='JC' or request.user.groups.values()[0]['name'] =='JConlyview': 
            return qs.filter(is_active=True)


    @admin.display(ordering="-hospital__district",description='区域')
    def list_district(self, obj):
        return obj.hospital.district

    @admin.display(ordering="hospital__hospitalclass",description='级别')
    def list_hospitalclass(self, obj):
        return obj.hospital.hospitalclass
    
    @admin.display(description='医院名称')
    def list_hospitalname(self, obj):
        return obj.hospital.hospitalname
    
