from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from django import forms
from django.utils import timezone
import openpyxl
from django.http import HttpResponse

class SalesmanFilter(SimpleListFilter):
    title = '负责人' 
    parameter_name = 'ReportUserInfo'

    def lookups(self, request, model_admin):

        salesmans = ReportUserInfo.objects.filter(Q(username__in= ['jy', 'fzj','wh','zjm','gjb','gsj','admin']))
        return [(salesman.id, salesman.chinesename) for salesman in salesmans]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(salesman__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset

class CompanyFilter(SimpleListFilter):
    title = '医院' 
    parameter_name = 'Company'

    def lookups(self, request, model_admin):

        companys = Company.objects.filter(Q(company__in= ['普中心', '十院','公卫','市一南','市一北','普美瑞']))
        return [(company.id, company.company) for company in companys]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(company__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset
        

class MyModelForm(forms.ModelForm):
    class Meta:
        model = SalesReport
        fields = '__all__'
        widgets = {
            'stage': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        print('today::::',today)
        if self.instance.pk is not None:  # 如果是编辑模式
            if self.instance.date1 != today:
                # 将所有字段设置为不可编辑
                for field in self.fields:
                    self.fields[field].disabled = True



def export_to_excel(modeladmin, request, queryset):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = '集成日报'

    # 添加表头
    columns = ['填报日期','医院','填报人', '项目','主要人员','工作简述','工作类型','最新推进状态','已完成阶段','上一阶段反馈时间','最近计划反馈时间']  # 替换为您模型的字段名
    worksheet.append(columns)

    # 添加数据
    for obj in queryset:
        # print('obj:::::',obj.date1,obj.company.company, obj.salesman.chinesename, obj.project, obj.type)
        worksheet.append([obj.date1, obj.company.company, obj.salesman.chinesename,obj.project, obj.name,obj.desc,obj.type,obj.state,obj.stage,obj.date2,obj.date3])  # 替换为模型字段

    # 设置响应
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="JC_Report.xlsx"'
    workbook.save(response)
    return response

from django.utils.html import format_html
import textwrap

@admin.register(SalesReport)
class JcReportAdmin(admin.ModelAdmin):
    form = MyModelForm
    date_hierarchy = 'date1'
    exclude = ('id','createtime','updatetime','operator','is_active')
    search_fields=['salesman__chinesename','project','company__company']
    readonly_fields= ('salesman','date1','company')
    list_filter = [CompanyFilter,SalesmanFilter]
    list_display_links =('project',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('formatted_date1','company','salesman_chinesename', 'project','name','desc','type','state','stage','date2','date3')
    ordering = ('-date1','salesman')
    JcReport_view_group_list = ['boss','JCboss']
    actions = [export_to_excel]  

    def has_add_permission(self,request,obj=None):
        return False
    
    @admin.display(ordering="salesman__chinesename",description='责任人')
    def salesman_chinesename(self, obj):
        name= obj.salesman.chinesename
        wrapped_name = textwrap.fill(name, width=10)
        return  format_html('<div style="width:50px;">{}</div>', wrapped_name)
    
    @admin.display(ordering="desc",description='工作简述')
    def update_desc(self, obj):
        project= obj.project
        wrapped_name = textwrap.fill(project, width=50)
        return  format_html('<div style="width:50px;">{}</div>', wrapped_name)
    

    @admin.display(ordering="date1",description='填报日期')
    def formatted_date1(self, obj):
        date= obj.date1.strftime("%m月%d日")  
        return date
    
 
 


    # 如果不是当天，所有字段都是只读
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj is not None:  # 如果是编辑模式
            today = timezone.now().date()
            if obj.date1 != today:
                readonly_fields = [field.name for field in self.model._meta.fields]  # 所有字段都设置为只读
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.date1 != timezone.now().date():
            return False  # 不允许删除
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] == 'JCboss':
                return False
        return super().has_delete_permission(request, obj)

   

    def has_change_permission(self,request, obj=None):
        if obj is not None and obj.date1 != timezone.now().date():
            return False
        
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] == 'JCboss':
                return False
        if obj is not None and obj.date1 == timezone.now().date() and  obj.salesman==request.user or request.user.is_superuser or request.user.username == 'zwq8zhj':
 
             return True
        

    def get_queryset(self, request):
        qs = super(JcReportAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.username == 'zwq8zhj':
            return qs
        user_in_group_list = request.user.groups.values('name')
        # print(user_in_group_list)
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.JcReport_view_group_list:
                return qs
            
        #普通销售的话:
        qs= qs.filter(salesman=request.user)   
        return qs   
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        # 修改导出到 Excel 的动作名称
        if 'export_to_excel' in actions:
            actions['export_to_excel'] = (export_to_excel, 'export_to_excel', '下载')  # 自定义按钮名称
        return actions