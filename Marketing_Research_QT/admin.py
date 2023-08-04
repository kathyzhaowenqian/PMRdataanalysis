from django.contrib import admin
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone
from import_export import formats
# Register your models here.
from django.shortcuts import render
from Marketing_Research_QT.models import *
from Marketing_Research_QT.models_delete import *
from import_export.formats import base_formats
from import_export import resources
from django.utils.encoding import smart_str
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
from django.db.models import Case, When, Value, IntegerField
from import_export.admin import ExportMixin
from Marketing_Research_QT.resource import *
from django.http import JsonResponse,HttpResponse






class ProjectFilter(SimpleListFilter):
    title = '项目' 
    parameter_name = 'project'

    def lookups(self, request, model_admin):

        projects = Project.objects.filter(company_id=2)
        return [(project.id, project.project) for project in projects]

        # projects = set([c.project for c in model_admin.model.objects.all()])#为什么这个方法可以直接过滤？？？
        # print([(c.id, c.project) for c in projects])
        # return [(c.id, c.project) for c in projects]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(project__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset

class ProjectFilterforDetail(SimpleListFilter):
    title = '项目' 
    parameter_name = 'project'

    def lookups(self, request, model_admin):

        projects = Project.objects.filter(company_id=2)
        return [(project.id, project.project) for project in projects]

        # projects = set([c.project for c in model_admin.model.objects.all()])#为什么这个方法可以直接过滤？？？
        # print([(c.id, c.project) for c in projects])
        # return [(c.id, c.project) for c in projects]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(researchlist__project__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset

class IfTargetCustomerFilter(SimpleListFilter):
    title = '是否填写目标'
    parameter_name = 'iftarget'

    def lookups(self, request, model_admin):
        return [(1, '已填目标额/任何季度'), (2, 'Q2已填目标额'),(3, 'Q3已填目标额'),(4, 'Q4已填目标额'),(5, '未填目标额')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter((Q(salestarget3__q1target__gt= 0)|Q(salestarget3__q2target__gt =0)|Q(salestarget3__q3target__gt =0)|Q(salestarget3__q4target__gt=0)) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
        if self.value() == '2':
            return queryset.filter(Q(salestarget3__q2target__gt= 0) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
        if self.value() == '3':
            return queryset.filter(Q(salestarget3__q3target__gt =0) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
        if self.value() == '4':
            return queryset.filter(Q(salestarget3__q4target__gt =0) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
  
        elif self.value() == '5':
            return queryset.filter(Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') & Q(salestarget3__q1target = 0)& Q(salestarget3__q2target =0) & Q(salestarget3__q3target =0)& Q(salestarget3__q4target=0))



class CustomerProjectTypeFilter(SimpleListFilter):
    title = '医院项目分类'
    parameter_name = 'customerprojecttype'

    def lookups(self, request, model_admin):
        return [(1, '老项目(22年已开票)'),(2, '丢失的项目(22年已开票、23年至今未开票)'), (3, 'Q1新项目(22年未开票、23Q1已开票)'), (4, 'Q2新项目(22-23Q1未开票、23Q2已开票)'),(5, 'Q3新项目(22-23Q2未开票、23Q3已开票)'),(6, 'Q4新项目(22-23Q3未开票、23Q4已开票)'),(7, '潜在项目(至今未曾开票)'),(8, '潜在项目和今年新项目(22年未开票)')]


    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':#老客户(去年已开票)
            return queryset.filter(Q(detailcalculate3__totalsumpermonth__gt = 0))
 
        elif self.value() == '2':#丢失的老客户(22年已开票、23年至今未开票)
            return queryset.filter(Q(detailcalculate3__totalsumpermonth__gt = 0) &  Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') & Q(salestarget3__q1actualsales= 0) & Q(salestarget3__q2actualsales= 0) & Q(salestarget3__q3actualsales= 0) & Q(salestarget3__q4actualsales= 0)) 

        elif self.value() == '3': #Q1新客户(22年未开票、23Q1已开票)
            return queryset.filter(Q(detailcalculate3__totalsumpermonth = 0) & ( Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') &  Q(salestarget3__q1actualsales__gt= 0)) )
        
        elif self.value() == '4': #Q2新客户(22-23Q1未开票、23Q2已开票
            return queryset.filter(Q(detailcalculate3__totalsumpermonth = 0) & ( Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') &  Q(salestarget3__q1actualsales= 0) &  Q(salestarget3__q2actualsales__gt= 0)) )
        
        elif self.value() == '5': #Q3新客户(22-23Q2未开票、23Q3已开票)'
            return queryset.filter(Q(detailcalculate3__totalsumpermonth = 0) & ( Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') &  Q(salestarget3__q1actualsales= 0) &  Q(salestarget3__q2actualsales= 0) & Q(salestarget3__q3actualsales__gt= 0)) )
        
        elif self.value() == '6': #Q4新客户(22-23Q3未开票、23Q4已开票)
            return queryset.filter(Q(detailcalculate3__totalsumpermonth = 0) & ( Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') &  Q(salestarget3__q1actualsales= 0) &  Q(salestarget3__q2actualsales= 0) &  Q(salestarget3__q3actualsales= 0) & Q(salestarget3__q4actualsales__gt= 0)) )
        
        elif self.value() == '7': #潜在客户  
            return queryset.filter(Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') & Q(salestarget3__q1actualsales = 0)& Q(salestarget3__q2actualsales =0) & Q(salestarget3__q3actualsales =0)& Q(salestarget3__q4actualsales=0) & Q(detailcalculate3__totalsumpermonth = 0) )
        elif self.value() == '8': #潜在客户 + 今年新客户， 22年未开票客户 
            return queryset.filter(Q(detailcalculate3__totalsumpermonth = 0))



class IfActualSalesFilter(SimpleListFilter):
    title = '23年是否开票'
    parameter_name = 'ifactualsales'
    def lookups(self, request, model_admin):
        return [(1, '23年已开票'), (2, 'Q1已开票'),(3, 'Q2已开票'),(4, 'Q3已开票'),(5, 'Q4已开票'),(6, '23年未开票')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':#23年已开票
            return queryset.filter((Q(salestarget3__q1actualsales__gt= 0)|Q(salestarget3__q2actualsales__gt =0)|Q(salestarget3__q3actualsales__gt =0)|Q(salestarget3__q4actualsales__gt=0)) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
        if self.value() == '2': #Q1已开票
            return queryset.filter(Q(salestarget3__q1actualsales__gt= 0) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
        if self.value() == '3':#Q2已开票
            return queryset.filter(Q(salestarget3__q2actualsales__gt =0) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
        if self.value() == '4':#Q3已开票
            return queryset.filter(Q(salestarget3__q3actualsales__gt =0) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
        if self.value() == '5':#Q4已开票
            return queryset.filter(Q(salestarget3__q4actualsales__gt=0) & Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') )
        elif self.value() == '6':#23年未开票
            return queryset.filter(Q(salestarget3__is_active=True) & Q(salestarget3__year='2023') & Q(salestarget3__q1actualsales = 0)& Q(salestarget3__q2actualsales =0) & Q(salestarget3__q3actualsales =0)& Q(salestarget3__q4actualsales=0))

class IfSalesChannelFilter(SimpleListFilter):
    title = '销售路径/所需支持/进展'
    parameter_name = 'ifsaleschannel'

    def lookups(self, request, model_admin):
        return [(1, '已填写销售路径/所需支持/进展'), (2, '未填写')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter((Q(saleschannel__isnull=False) & ~Q(saleschannel=''))|(Q(support__isnull=False) & ~Q(support=''))|(Q(progress__isnull=False) & ~Q(progress='')))
 
        elif self.value() == '2':
            return queryset.filter((Q(saleschannel__isnull=True) | Q(saleschannel=''))&(Q(support__isnull=True) | Q(support=''))&(Q(progress__isnull=True) | Q(progress='')))

# class IfSupportFilter(SimpleListFilter):
#     title = '所需支持'
#     parameter_name = 'ifsupport'

#     def lookups(self, request, model_admin):
#         return [(1, '已填写所需支持'), (2, '未填写所需支持')]

#     def queryset(self, request, queryset):
#         # pdb.set_trace()
#         if self.value() == '1':
#             return queryset.filter(Q(support__isnull=False) & ~Q(support=''))
 
#         elif self.value() == '2':
#             return queryset.filter(Q(support__isnull=True) | Q(support=''))


class SalesmanFilter(SimpleListFilter):
    title = '第一负责人' 
    parameter_name = 'userinfo'

    def lookups(self, request, model_admin):

        salesmans = UserInfo3.objects.filter(Q(username__in= ['ybb', 'fzj','zxl','wh','zjm','gjb','gsj','jll','yy','hfj']))
        # print([(salesman.id, salesman.chinesename) for salesman in salesmans])
        return [(salesman.id, salesman.chinesename) for salesman in salesmans]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(salesman1__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset

class SalesmanFilter2(SimpleListFilter):
    title = '第二负责人' 
    parameter_name = 'userinfo2'

    def lookups(self, request, model_admin):

        salesmans = UserInfo3.objects.filter(Q(username__in= ['ybb', 'fzj','zxl','wh','zjm','gjb','gsj','jll','yy','hfj']))
        # print([(salesman.id, salesman.chinesename) for salesman in salesmans])
        return [(salesman.id, salesman.chinesename) for salesman in salesmans]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(salesman2__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset
        
class SalesmanFilterforDetail(SimpleListFilter):
    title = '负责人' 
    parameter_name = 'userinfo'

    def lookups(self, request, model_admin):

        salesmans = UserInfo3.objects.filter(Q(username__in= ['ybb', 'fzj','zxl','wh','zjm','gjb','gsj','jll','yy','hfj']))
        # print([(salesman.id, salesman.chinesename) for salesman in salesmans])
        return [(salesman.id, salesman.chinesename) for salesman in salesmans]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(researchlist__salesman1__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset


#admin中的delete优先,具体admin中的更优先,针对inline没有用！！！！！
class GlobalAdmin(admin.ModelAdmin):
    def delete_queryset(self,request, queryset):
        print('im in global delete_queryset')
        queryset.update(is_active=False)
        # queryset.update(operator=request.user)

    def delete_model(self, request, obj):
        print('im in global delete_model')
        obj.is_active = False 
        # obj.operator=request.user
        obj.save()

    def get_queryset(self, request):
        print('im in global get_queryset')
        return super().get_queryset(request).filter(is_active=True)

###------------------FORM---------------------------------------------------------------------------------------------------------------
# 验证数据手机号
def validate(value): # 验证数据
    try:
        v = int(value)
    except:
        raise forms.ValidationError(u'请输入正确手机号')
    if len(value) != 11:
        raise forms.ValidationError(u'请输入正确手机号')
    

class PMRResearchDetailInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print('self.fields',self.fields['ownbusiness'])
        # print(self.fields['brand'].queryset)
        # self.fields['brand'].queryset =  Brand.objects.filter(is_active=True)
        # print(self)
        #在没有autocomplete的前提下，只有在这个form里面修改才能保证过滤isactive
        self.fields['competitionrelation'].queryset =  CompetitionRelation.objects.filter(is_active=True)
 
    class Meta: 
            model = PMRResearchDetail3
            exclude = ['id']
            widgets = {
                'machinemodel': forms.TextInput(attrs={'size':'15'}),
                'machineseries': forms.TextInput(attrs={'size':'15'}),
                'testprice': forms.TextInput(attrs={'size':'10'}),
                'endsupplier': forms.TextInput(attrs={'size':'15'}),
                'machinenumber' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),
                'detailedproject': AutocompleteSelect(
                    model._meta.get_field('detailedproject'),
                    admin.site,
                    attrs={'style': 'width: 20ch'}),
                'brand': AutocompleteSelect(
                    model._meta.get_field('brand'),
                    admin.site,
                    attrs={'style': 'width: 20ch'}),
            }


class PMRResearchListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         #限制新增list表中这些外键的显示
        # self.fields['company'].queryset =  Company.objects.filter(is_active=True,id=1)#限制此app中的调研表中的company只显示PMR
        # self.fields['hospital'].queryset =  Hospital.objects.filter(is_active=True)
        # self.fields['project'].queryset =  Project.objects.filter(is_active=True,company_id=1)#限制此app中的调研表中的project只显示PMR公司相关的project
        #!!!!!!!!!!!!!!!要判断一下，如果是自己只能选自己,建立group
        # self.fields['salesman1'].queryset =  UserInfo.objects.filter(Q(is_active=True) & ~Q(username= 'admin'))
        # self.fields['salesman2'].queryset =  UserInfo.objects.filter(Q(is_active=True) & ~Q(username= 'admin'))
    contactmobile = forms.CharField(validators=[validate], widget=forms.TextInput(attrs={'placeholder': u'输入11位手机号'}),label='手机号',required=False)
    class Meta: 
        model = PMRResearchList3
        exclude = ['id']
   

###------------------INLINE------------------------------------------------------------------------------------------------------------

class SalesmanPositionInline(admin.TabularInline):
    model = SalesmanPosition3
    fk_name = "user"
    extra = 0
    fields=['user','company','position'] 
    verbose_name = verbose_name_plural = ('员工职位列表')
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request).filter(is_active=True)
    #     print(queryset,1)
    #     return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Company.objects.filter(is_active=True)    
        return super(SalesmanPositionInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    

class SalesmanPositionInline3(admin.TabularInline):
    model = SalesmanPosition3
    fk_name = "company"
    extra = 0
    fields=['user','company','position'] 
    verbose_name = verbose_name_plural = ('员工职位列表')
    # def get_queryset(self, request):       
    #     queryset = super().get_queryset(request).filter(company__is_active=True)
    #     print(queryset,2)
    #     return queryset
    

class ProjectInline(admin.TabularInline):
    model = Project
    fk_name = "company"
    extra = 0
    fields=['project','company'] 
    verbose_name = verbose_name_plural = ('项目列表')

    def get_queryset(self, request):
        queryset = super().get_queryset(request).filter(is_active=True)        
        return queryset


class PMRResearchDetailInline(admin.TabularInline):
    form=PMRResearchDetailInlineForm
    model = PMRResearchDetail3
    fk_name = "researchlist"
    extra = 0
    fields=['detailedproject','ownbusiness','brand','machinemodel','machinenumber','installdate', 'endsupplier','competitionrelation','machineseries','testprice'] 
    # readonly_fields = ('sumpermonth',)
    autocomplete_fields=['detailedproject','brand']
    verbose_name = verbose_name_plural = ('市场调研仪器详情表')
    QT_view_group_list = ['boss','pmrmanager','QTmanager','allviewonly']
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.QT_view_group_list:
                return qs.filter(is_active=True)
            
       #普通销售的话:
        return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)))




    def has_add_permission(self,request,obj):
        print('我在PMRResearchDetailInline has add permission:::obj',obj,request.user) 
        if obj==None:
            if request.POST.get('salesman1'):                
                if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                    return True
                elif request.POST.get('salesman1')!= str(request.user.id):
                    print('我在PMRResearchDetailInline has add permission:: :obj==None FALSE request.POST.get(salesman1)',request.POST.get('salesman1'),request.user)
                    return False
                else:
                    return True
            else:    
                print('我在PMRResearchDetailInline has add permission:: obj==None True 没有request.POST.get(salesman1)')
                return True

        else:    
            if request.user.is_superuser or obj.salesman1==request.user  or request.POST.get('salesman1')==str(request.user.id) or request.user.groups.values()[0]['name'] =='boss':
                print('我在inline has add permission:::,obj.salesman1 if ',True)
                return True
            else:
                print('我在inline has add permission:::,obj.salesman1 else',False)
                return False

    def has_change_permission(self,request, obj=None):
        print('我在PMRResearchDetailInline has change permission:: obj',obj)
        if obj==None:
                print('我在PMRResearchDetailInline has change permission:::obj,request.POST.get(salesman1)',True,request.POST.get('salesman1'))
                return True            
        elif obj.salesman1==request.user or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            print('我在PMRResearchDetailInline has change permission:::obj',True,obj.salesman1)
            return True
        else:
            print('我在PMRResearchDetailInline has change permission:::obj',False)
            return False

    def has_delete_permission(self,request, obj=None):
        print('我在inline has_delete_permission:::obj',obj)        
        return True
    



class SalesTargetInline(admin.StackedInline):
    model = SalesTarget3
    fk_name = "researchlist"
    extra = 0
    readonly_fields = result_of_Quatar_display(settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS,settings.MARKETING_RESEARCH_TARGET_AUTO_DELAYED_DAYS)[1]

    # readonly_fields = ('q1actualsales','q2actualsales','q3actualsales','q4actualsales','q1finishrate','q2finishrate','q3finishrate','q4finishrate')
    # fieldsets =  ('year','q1target','q1completemonth','q2target','q2completemonth','q3target','q3completemonth','q4target','q4completemonth'),       
    fields =  ('year',('q1target','q1completemonth','q1actualsales','q1finishrate'),
                      ('q2target','q2completemonth','q2actualsales','q2finishrate'),
                      ('q3target','q3completemonth','q3actualsales','q3finishrate'),
                      ('q4target','q4completemonth','q4actualsales','q4finishrate'),
                                            )                              
    
    verbose_name = verbose_name_plural = ('作战计划和成果')
    QT_view_group_list = ['boss','pmrmanager','QTmanager','allviewonly']

    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        today=datetime.now().date()
        # today = date(2024, 2, 11)
        thisyear= datetime.now().year
        print('我在SalesTargetInline-get_queryset')
        # self.readonly_fields = result_of_Quatar_display(settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS,settings.MARKETING_RESEARCH_TARGET_AUTO_DELAYED_DAYS)[1]
        #如果在2023年并且今天日期小于2024.1.1减掉30天
        if today<=calculate_quarter_start_end_day(1,thisyear+1)[0]-timedelta(days=settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS) and thisyear==2023:

            if request.user.is_superuser:
                return qs.filter(is_active=True,year='2023')    
            
            user_in_group_list = request.user.groups.values('name')
            for user_in_group_dict in user_in_group_list:
                if user_in_group_dict['name'] in self.QT_view_group_list:
                    return qs.filter(is_active=True,year='2023')
                
            #普通销售的话:
            return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user)&Q(year='2023'))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)&Q(year='2023')))
        
        #如果大于2024.1.1减掉30天
        if today > calculate_quarter_start_end_day(1,thisyear+1)[0]-timedelta(days=settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS):
            if request.user.is_superuser :
                return qs.filter(is_active=True)  
              
            user_in_group_list = request.user.groups.values('name')
            for user_in_group_dict in user_in_group_list:
                if user_in_group_dict['name'] in self.QT_view_group_list:
                    return qs.filter(is_active=True)

            #普通销售的话:
            return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)))

    #普通销售不允许删除目标inline
    def has_delete_permission(self,request, obj=None):
        print('我在SalesTargetInline has_delete_permission:::obj',obj)        
        if request.user.is_superuser :
            return True
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.QT_view_group_list:
                return True
        else:
            return False



class DetailCalculateInline(admin.StackedInline):
    model = DetailCalculate3
    fk_name = "researchlist"
    extra = 0
    readonly_fields =  ('totalmachinenumber','ownmachinenumber','ownmachinepercent','newold','totalsumpermonth')#,'detailedprojectcombine','ownbusinesscombine','brandscombine','machinenumbercombine','machinemodelcombine','machineseriescombine','installdatescombine','competitionrelationcombine',)                    
    verbose_name = verbose_name_plural = ('仪器情况汇总')
    fields =  (('totalmachinenumber','ownmachinenumber','ownmachinepercent','totalsumpermonth','newold'),
            #    ('detailedprojectcombine'),
            #    ('ownbusinesscombine'),
            #    ('brandscombine'),
            #    ('machinenumbercombine'),
            #    ('machinemodelcombine'),
            #    ('machineseriescombine'),
            #    ('installdatescombine'),
            #    ('competitionrelationcombine'),
               )
                                           

###------------------ADMIN-----------------------------------------------------------------------------------------------------------------------------------

@admin.register(UserInfo3)  
class User3Admin(UserAdmin):  
        
    inlines=[SalesmanPositionInline]
    list_display = ('username','chinesename','first_name','last_name','email','is_staff','is_superuser','date_joined','last_login')
    # exclude = ('id','createtime','updatetime','is_active')
 
    fieldsets = (
        # 此处保留UserAdmin中的password字段，以此保证在新增用户时避免出现明文存储的问题
         (None, {u'fields': ('username', 'password')}),
        (gettext_lazy('基本信息'), {'fields': (
         'chinesename', 'first_name', 'last_name', 'email',)}),

        (gettext_lazy('权限信息'), {'fields': ('is_superuser', 'is_staff',  'groups', 'user_permissions','is_active')}),

        (gettext_lazy('日期信息'), {'fields': ('last_login', 'date_joined')}),
    )
 




@admin.register(SalesmanPosition3)  
class SalesmanPositionAdmin(GlobalAdmin):   
    exclude = ('id','createtime','updatetime')

    # 外键company只显示active的  定死普美瑞
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['adminform'].form.fields['company'].queryset = Company.objects.filter(is_active=True)
        return super(SalesmanPositionAdmin, self).render_change_form(request, context, add, change, form_url, obj)


@admin.register(Company)  
class CompanyAdmin(GlobalAdmin):   
    inlines=[SalesmanPositionInline3,ProjectInline]
    exclude = ('id','createtime','updatetime','is_active')

 


@admin.register(PMRResearchList3)
class PMRResearchListAdmin(GlobalAdmin): #ExportMixin,
    # resource_class = PMRResearchListResource
    form=PMRResearchListForm
    inlines=[SalesTargetInline,PMRResearchDetailInline,DetailCalculateInline]
    empty_value_display = '--'
    list_display_links =('hospital',)
    exclude = ('operator','is_active')
    search_fields=['uniquestring']
    list_per_page = 12
    list_display = result_of_Quatar_display(settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS,settings.MARKETING_RESEARCH_TARGET_AUTO_DELAYED_DAYS)[0]#+('detail_qtysum','detail_own_qtysum','detail_ownbusiness','detail_brands','detail_machinemodel','detail_machineseries','detail_installdate','detail_competitor',)
    # ('hospital_district','hospital_hospitalclass','hospital','colored_project','salesman1_chinesename','salesman2_chinesename',
    #                 'detailcalculate_totalmachinenumber','detailcalculate_ownmachinenumberpercent','detailcalculate_newold',
    #                'testspermonth','saleschannel','support',)
                #    'salestarget_23_q1','completemonth_23_q1','actualsales_23_q1','finishrate_23_q1',
                #    'salestarget_23_q2','completemonth_23_q2','actualsales_23_q2','finishrate_23_q2',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 
    autocomplete_fields=['project','hospital']       
    ordering = ('-hospital__district',
                Case(
                        When(hospital__hospitalclass='三级', then=Value(1)),
                        When(hospital__hospitalclass='二级', then=Value(2)),
                        When(hospital__hospitalclass='一级', then=Value(3)),
                        When(hospital__hospitalclass='未定级', then=Value(4)),
                        output_field=IntegerField(),
                    ),
                'hospital__hospitalname','salesman1','project',)
    # ordering = ('-hospital__district','hospital__hospitalclass','hospital__hospitalname','salesman1','project',) #('-id',)#
    list_filter = [ProjectFilter,'hospital__district','hospital__hospitalclass',SalesmanFilter,SalesmanFilter2,'detailcalculate3__newold',IfTargetCustomerFilter,IfActualSalesFilter,IfSalesChannelFilter,CustomerProjectTypeFilter]
    search_fields = ['hospital__hospitalname','pmrresearchdetail3__brand__brand','pmrresearchdetail3__machinemodel','pmrresearchdetail3__machineseries']
    fieldsets = (('作战背景', {'fields': ('company','hospital','project','salesman1','salesman2',
                                        'testspermonth','owntestspermonth','contactname','contactmobile','salesmode',),
                              'classes': ('wide','extrapretty',),
                              'description': format_html(
                '<span style="color:{};font-size:10.0pt;">{}</span>','blue','注意："第一负责人"只允许填登录用户自己的姓名')}),

                 ('作战路径及需求', {'fields': ('saleschannel','support','progress','adminmemo'),
                              'classes': ('wide',)}),                
                )
    QT_view_group_list = ['boss','pmrmanager','QTmanager','allviewonly']


    # def has_export_permission(self, request):
    #     if request.user.is_superuser:
    #         return True
    #     user_in_group_list = request.user.groups.values('name')
    #     for user_in_group_dict in user_in_group_list:
    #         if user_in_group_dict['name'] in ['pmrdirectsales','pmrmanager','QTmanager','WDmanager']:
    #             return True
    #         else:
    #             return False
    

    # def get_export_formats(self):
    #     return [base_formats.XLSX]
    

    # def get_export_queryset(self, request):
    #     queryset = super().get_export_queryset(request)
    #     if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
    #         queryset = queryset
    #     else: 
    #         queryset = queryset.filter(Q(salesman1=request.user) | Q(salesman2=request.user))
    #     return queryset




    # 新增或修改数据时，设置外键可选值，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company': 
            kwargs["queryset"] = Company.objects.filter(is_active=True,id=2) 
        if db_field.name == 'hospital': 
            kwargs["queryset"] = Hospital.objects.filter(is_active=True) 
        if db_field.name == 'project':  
            kwargs["queryset"] = Project.objects.filter(is_active=True,company_id=2) 
        if db_field.name == 'salesman1': 
            # kwargs['initial'] = #设置默认值
            kwargs["queryset"] = UserInfo.objects.filter(Q(is_active=True) & Q(username__in= ['ybb', 'fzj','zxl','wh','zjm','gjb','gsj','jll','yy','hfj']))
        if db_field.name == 'salesman2':  
            kwargs["queryset"] = UserInfo.objects.filter(Q(is_active=True) & Q(username__in= ['ybb', 'fzj','zxl','wh','zjm','gjb','gsj','jll','yy','hfj'])) 

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    

#下面三个还没有修改
    def has_delete_permission(self, request,obj=None):
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] == 'pmronlyview' or request.user.groups.values()[0]['name'] == 'allviewonly':
                return False
            
        if obj==None:
            return True
        
        if request.POST.get('salesman1'):
            if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                return True
            if request.POST.get('salesman1')!=str(request.user.id):
                print('我在PmrResearchListAdmin has delete permission request.POST.get(salesman1)  false!!!',request.POST.get('salesman1'))
                return False
            else: 
                print('我在PmrResearchListAdmin has delete permission request.POST.get(salesman1)  true!!',request.POST.get('salesman1'))
                return True
        if obj.salesman1==request.user or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            print('我在PmrResearchListAdmin has delete permission True obj.salesman1 ',obj.salesman1,request.user)
            return True

        else:
            print('我在PmrResearchListAdmin has delete permission else else else',False)
            return False
        

    def has_change_permission(self,request, obj=None):
        print('我在PmrResearchListAdmin has change permission:: obj',obj)
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] =='pmronlyview' or request.user.groups.values()[0]['name'] == 'allviewonly':
                return False
        if obj==None:
            print('我在PmrResearchListAdmin has change permission obj==None,True ',request.POST.get('salesman1'))
            return True
        if request.POST.get('salesman1'):
            if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman1)  True superuser!!!')
                return True
            if request.POST.get('salesman1')!=str(request.user.id):
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman1)  false!!!',request.POST.get('salesman1'))
                return False
            else: 
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman1)  true!!',request.POST.get('salesman1'))
                return True
        if obj.salesman1==request.user or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            print('我在PmrResearchListAdmin has change permission True obj.salesman1 ',obj.salesman1)
            return True
        else:
            print('我在PmrResearchListAdmin has change permission else else else',False)
            return False

    # def has_add_permission(self,request):#,obj=None):
        
    #     if request.user.groups.values():
    #         if request.user.groups.values()[0]['name'] =='pmronlyview' or request.user.groups.values()[0]['name'] == 'allviewonly':
    #             return False
    #     if request.POST.get('salesman1'):
    #         if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
    #             print('我在PmrResearchListAdmin has add permission  request.POST.get(salesman1 True SUPERUSER!!)',request.POST.get('salesman1'))
    #             return True
    #         if request.POST.get('salesman1')!=str(request.user.id):
    #             print('我在PmrResearchListAdmin has add permission  request.POST.get(salesman1 false!!)',request.POST.get('salesman1'),request.user.id)
    #             raise PermissionDenied('Forbidden ++++++++++++++++++++++')
    #             #return False
    #         else:
    #             print('我在PmrResearchListAdmin has add permission  request.POST.get(salesman1 true!!)',request.POST.get('salesman1'))
    #             return True
    #     else:
    #         print('我在PmrResearchListAdmin has add permission else else',True)
    #         return True

    def has_add_permission(self,request):
        if  request.user.is_superuser:
            return True
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] =='boss':
                return True        
            else:
              return False
        else:
            return False


    def get_queryset(self, request):
        if request.user.groups.values():
            print('request.user.groups:::::',request.user, request.user.groups.values(),request.user.groups.values()[0]['id'], request.user.groups.values()[0]['name'])
        else:
            print('没有分组admin')
        #先拿到objects列表
        qs = super(PMRResearchListAdmin, self).get_queryset(request)
        print('我在PMRResearchListAdmin-get_queryset')

        #要不要在此加入Q1-Q4变动的？？
        self.list_display = result_of_Quatar_display(settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS,settings.MARKETING_RESEARCH_TARGET_AUTO_DELAYED_DAYS)[0]#+('detail_qtysum','detail_own_qtysum','detail_ownbusiness','detail_brands','detail_machinemodel','detail_machineseries','detail_installdate','detail_competitor',)
        # self.list_display = self.list_display + ('detail_qtysum','detail_own_qtysum',)

        if request.user.is_superuser :
            print('我在PMRResearchListAdmin-get_queryset-筛选active的')            
            return qs.filter(is_active=True,company_id=2)

                
        # <QuerySet [{'name': 'pmrdirectsales'}, {'name': 'QTmanager'}]>
        user_in_group_list = request.user.groups.values('name')
        print(user_in_group_list)
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.QT_view_group_list:
                 # print('我在模型里')
                return qs.filter(is_active=True,company_id=2)
            
       #普通销售的话:
        return qs.filter((Q(is_active=True)&Q(salesman1=request.user)&Q(company_id=2))|(Q(is_active=True)&Q(salesman2=request.user)&Q(company_id=2)))
                      

# ------delete_model内层的红色删除键------------------------------
    def delete_model(self, request, obj):
        print('我在LISTADMIN delete_model')
        if request.user.is_superuser or obj.salesman1==request.user or request.user.groups.values()[0]['name'] =='boss':             
            obj.is_active = False 
            obj.pmrresearchdetail3_set.all().update(is_active=False)
            obj.salestarget3_set.all().update(is_active=False)
            obj.detailcalculate3.is_active=False
            obj.detailcalculate3.save()
            obj.operator=request.user   

            # msg = '成功删除了{}的{}项目'.format(obj.hospitalname,obj.project)
            # self.message_user(request, msg,messages.SUCCESS) 

            obj.save()

    def delete_queryset(self,request, queryset):        
            print('我在delete_queryset')
            for delete_obj in queryset:     
                print('delete_queryset delete_obj',delete_obj)                    
                if request.user.is_superuser or delete_obj.salesman1==request.user or request.user.groups.values()[0]['name'] =='boss':     
                    delete_obj.is_active=False
                    print('list 已假删')
                    delete_obj.pmrresearchdetail3_set.all().update(is_active=False)
                    delete_obj.salestarget3_set.all().update(is_active=False)
                    delete_obj.detailcalculate3.is_active=False
                    print('delete_obj.detailcalculate3.is_active',delete_obj.detailcalculate3.is_active)
                    delete_obj.detailcalculate3.save()
                    delete_obj.operator=request.user
                    delete_obj.save()



    def save_model(self, request, obj, form, change):
        obj.operator = request.user
        obj.uniquestring = '公司:{}, 医院:{}, 项目:{}, 第一责任人:{}'.format(obj.company,obj.hospital,obj.project,obj.salesman1)
        # machine_details=obj.pmrresearchdetail3_set.all()
        # print('machine_details',machine_details)
        # for eachmachine in machine_details:
        #     print('save_model eachmachine::::::',eachmachine,eachmachine.installdate,form.cleaned_data.get('installdate'))
        #     if not form.cleaned_data.get('installdate'):
        #         ret = '--'
        #     else:
        #         if (datetime.now().date() - form.cleaned_data.get('installdate')).days >= 1825:
        #             ret = '已超5年'
        #         else:
        #             ret = '5年内'            
        #     eachmachine.expiration=ret
        #     print(eachmachine.expiration)
        #     eachmachine.save()
        # obj.save()    

        # if form.cleaned_data.get('salesman1') == request.user.username or obj.salesman1==request.user.username or request.user.is_superuser or request.user.groups.values()[0]['name']=='boss':#request.user.username == 'ssl' or request.user.username == 'chm' :
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change): 
        ###注意要判断是否共用仪器！！！！！！！如果我司仪器必填序列号，怎么validate？？？！？
        print('我在save_related')
        super().save_related(request, form, formsets, change)
        if form.cleaned_data.get('salesman1')==request.user or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss': 
            machine_total_number=0
            new_or_old_list=[]
            machine_own_number=0
            machineserieslist_all=[]
            machineserieslist_own=[]
            # total_sales_2022=0
            # for each_formset in formsets: #全部的inline 各个表的inline      
            #     print('each_formset cleaned_data',each_formset.cleaned_data)
            # print('formsets[0]',formsets[0])
            # print('formsets[1]',formsets[1])
            # if len(formsets[0].cleaned_data) > 0:
            #     for each_inline in formsets[0].cleaned_data:
            #         if  each_inline.get('DELETE')==True:

            if len(formsets[1].cleaned_data) > 0:
                #formsets[1]是仪器详情表，显示inline的行数，删除的行也计算在内
                # print(len(formsets[1].cleaned_data))
                for each_inline in formsets[1].cleaned_data:
                    #循环列表中每一个字典，一个字典就是一行具体的数据
                        #是否我司业务不为空 且  没有被删除  且 仪器数量不为0         
                    print('each_inline',each_inline)  
                    print(type(each_inline.get('id')))     
                    if  each_inline.get('DELETE')==False and each_inline.get('machinenumber')!=0:
                        machine_total_number += each_inline['machinenumber']  
                        new_or_old_list.append(str(each_inline['ownbusiness']))
                        if each_inline['machineseries']:
                            machineserieslist_all.append(each_inline['machineseries'])
                        # print('machine_total_number',machine_total_number)
                        # print('machineserieslist_all',machineserieslist_all,len(machineserieslist_all),list(set(machineserieslist_all)),len(list(set(machineserieslist_all))))
                        if each_inline['ownbusiness']==True:
                            machine_own_number += each_inline['machinenumber']
                            if each_inline['machineseries']:
                                machineserieslist_own.append(each_inline['machineseries'])

            machine_total_number=machine_total_number-len(machineserieslist_all)+len(list(set(machineserieslist_all)))
            machine_own_number=machine_own_number-len(machineserieslist_own)+len(list(set(machineserieslist_own)))

            print('我在save_related machine_own_number\machine_total_number',machine_own_number,machine_total_number) 
            # print('form.instance',form.instance,form.instance.id)
            if machine_total_number == 0 or machine_own_number ==0:
                ownmachinepercent = 0
            else:
                ownmachinepercent= machine_own_number/machine_total_number

            if 'True' in new_or_old_list:
                newold='已有业务(含我司仪器)'
            else:
                newold='新商机(不含我司仪器)'
            #如果有计算项（老数据修改），则以更新的方式
            if DetailCalculate3.objects.filter(researchlist_id=form.instance.id):
                print('能获取对应的detailcalculate::::',DetailCalculate3.objects.filter(researchlist_id=form.instance.id))
                a=DetailCalculate3.objects.get(researchlist=form.instance)
                # print(a)
                a.totalmachinenumber=machine_total_number
                a.ownmachinenumber=machine_own_number
                a.ownmachinepercent=ownmachinepercent
                a.newold=newold
                a.is_active=True
                a.save()
            else:
                print('不能获取对应的detailcalculate')
                DetailCalculate3.objects.create(researchlist=form.instance,totalmachinenumber=machine_total_number,ownmachinenumber=machine_own_number,ownmachinepercent=ownmachinepercent,newold=newold,is_active=True).save()
        
            for eachdetail in PMRResearchDetail3.objects.filter(researchlist_id=form.instance.id):
                print('eachdetail',eachdetail)
                if not eachdetail.installdate:
                    ret = '--'
                else:
                    if (datetime.now().date() - eachdetail.installdate).days >= 1825:
                        ret = '已超5年'
                    else:
                        ret = '5年内'      
                eachdetail.expiration=ret
                eachdetail.save()

            if not SalesTarget3.objects.filter(researchlist_id=form.instance.id):
                SalesTarget3.objects.create(researchlist=form.instance,year='2023',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()
                SalesTarget3.objects.create(researchlist=form.instance,year='2024',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()
            else:
                if len(formsets[0].cleaned_data) > 0:
                    # for each_inline in formsets[0].cleaned_data:
                    #     if  each_inline.get('DELETE')==True and each_inline.get('year')=='2023':
                    #         SalesTarget3.objects.create(researchlist=form.instance,year='2023',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()
                    #     if  each_inline.get('DELETE')==True and each_inline.get('year')=='2024':
                    #         SalesTarget3.objects.create(researchlist=form.instance,year='2024',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()
                    if not SalesTarget3.objects.filter(researchlist_id=form.instance.id,year='2023',is_active=True):
                        SalesTarget3.objects.create(researchlist=form.instance,year='2023',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()
                    if not SalesTarget3.objects.filter(researchlist_id=form.instance.id,year='2024',is_active=True):
                        SalesTarget3.objects.create(researchlist=form.instance,year='2024',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()

            samehospital=PMRResearchList3.objects.filter(Q(hospital_id=form.instance.hospital.id))
            for x in samehospital:
                if not x.contactname:
                    x.contactname=form.cleaned_data.get('contactname')
                    if not x.contactmobile:
                        x.contactmobile=form.cleaned_data.get('contactmobile')

                if x.contactname == form.cleaned_data.get('contactname') and not x.contactmobile:
                    x.contactmobile=form.cleaned_data.get('contactmobile')
                x.save()
            #更新同一个销售的不同公司的同一家医院，一更新就全部更新
            samehospitalandsalesman=PMRResearchList3.objects.filter(Q(hospital_id=form.instance.hospital.id) & Q(salesman1_id=form.instance.salesman1.id))
            for y in samehospitalandsalesman:
                if form.cleaned_data.get('contactname'):#如果本次填数据了就更新，没填就不动
                    y.contactname=form.cleaned_data.get('contactname')
                    if form.cleaned_data.get('contactmobile'):
                        y.contactmobile=form.cleaned_data.get('contactmobile')
                y.save()
            # print('打印某医院相关项目的主任姓名',[obj.contactname for obj in PMRResearchList.objects.filter(Q(hospital_id=form.instance.hospital.id) & Q(project__project=form.instance.project.project))])
            

            #补充不同公司的同一家医院，CRP/SAA项目总测试数，在空的时候，才覆盖
            if form.instance.project.project=='CRP/SAA' and form.cleaned_data.get('testspermonth'):
                sameCRPSAA=PMRResearchList3.objects.filter(Q(hospital_id=form.instance.hospital.id) & Q(project__project='CRP/SAA') & Q(company_id=1) )
                for z in sameCRPSAA:
                    if not z.testspermonth:
                        z.testspermonth=form.cleaned_data.get('testspermonth')
                        z.save()

            #更新同一个销售的不同公司的同一家医院，CRP/SAA项目，一更新总测试数，就联动更新
            # print('form.instance.project.project',form.instance.project.project)
            # print('form.cleaned_data.get(testspermont)',form.cleaned_data.get('testspermonth'))
            if form.instance.project.project=='CRP/SAA' and form.cleaned_data.get('testspermonth'):
                sameCRPSAA=PMRResearchList3.objects.filter(Q(hospital_id=form.instance.hospital.id) & Q(salesman1_id=form.instance.salesman1.id)& Q(project__project='CRP/SAA') & Q(company_id=1))
                for z in sameCRPSAA:
                    z.testspermonth=form.cleaned_data.get('testspermonth')
                    z.save()


            #CRP/SAA 普美瑞和其田的数据联动（仅针对同一个医院的同一个销售）
            if form.instance.project.project=='CRP/SAA':
                #找出目前obj下面的仪器信息，active的、所有仪器，需要和其田的CRP/SAA比较，需要更新至QT,除去国赛，因为国赛在其田里不准，在普美瑞中才准
                ownmachinedetail= PMRResearchDetail3.objects.filter(Q(researchlist_id=form.instance.id) & ~Q(brand_id=9) & Q(researchlist__salesman1_id=form.instance.salesman1.id) & Q(is_active=True) & ~Q(machinenumber=0))
               
                #找出其田下面的，同一家医院同一个项目的同一个人的，所有仪器obj
                PMRmachinedetailnotGUOSAI= PMRResearchDetail3.objects.filter(Q(researchlist__hospital__id=form.instance.hospital.id) & ~Q(brand_id=9) & Q(researchlist__project__project='CRP/SAA') &  Q(researchlist__salesman1_id=form.instance.salesman1.id) & Q(researchlist__company__id=1) )
                print('PMRmachinedetailnotGUOSAI',PMRmachinedetailnotGUOSAI)
                PMRresearchlist=PMRResearchList3.objects.filter(hospital__id=form.instance.hospital.id,project__project='CRP/SAA',salesman1_id=form.instance.salesman1.id,company__id=1)
                print('PMRresearchlist',PMRresearchlist)

                owneachactivedetailllist=[]
                #如果PMR这边的CRPSAA有仪器数据
                if ownmachinedetail:
                    for owneachactivedetail in ownmachinedetail:
                        owneachactivedetailldict={}
                        owneachactivedetailldict['detailedproject_id']=owneachactivedetail.detailedproject.id if owneachactivedetail.detailedproject else None
                        owneachactivedetailldict['ownbusiness']=owneachactivedetail.ownbusiness if owneachactivedetail.ownbusiness else False
                        owneachactivedetailldict['brand_id']=owneachactivedetail.brand.id if owneachactivedetail.brand else None
                        owneachactivedetailldict['machinemodel']=owneachactivedetail.machinemodel if owneachactivedetail.machinemodel else None
                        owneachactivedetailldict['machinenumber']=owneachactivedetail.machinenumber if owneachactivedetail.machinenumber else None
                        owneachactivedetailldict['installdate']=owneachactivedetail.installdate if owneachactivedetail.installdate else None
                        owneachactivedetailldict['expiration']=owneachactivedetail.expiration if owneachactivedetail.expiration else None
                        owneachactivedetailldict['endsupplier']=owneachactivedetail.endsupplier if owneachactivedetail.endsupplier else None
                        owneachactivedetailldict['competitionrelation_id']=owneachactivedetail.competitionrelation.id if owneachactivedetail.competitionrelation else None
                        owneachactivedetailldict['machineseries']=owneachactivedetail.machineseries if owneachactivedetail.machineseries else None
                        owneachactivedetailldict['testprice']=owneachactivedetail.testprice if owneachactivedetail.testprice else None
                        owneachactivedetailllist.append(owneachactivedetailldict)

                     #查看下品牌，要把迈瑞的变成'是'，国赛的变成'否'，然后再复制给QT
                    ownbrandlist= list(set(item['brand_id'] for item in owneachactivedetailllist))
                    print('ownbrandlist',ownbrandlist)  

                    if PMRresearchlist:
                        PMR_researchlist_id=PMRresearchlist[0].id
                        if PMRmachinedetailnotGUOSAI:
                            #批量删除QTmachinedetail
                            PMRmachinedetailnotGUOSAI.update(is_active=False)                              

                        #在对应的QT那边新增PMR中的仪器
                        for data in owneachactivedetailllist:#遍历PMR自己所有的仪器
                            # if data['brand_id']== 9: #'国赛'
                            #     data['ownbusiness']=True
                            if data['brand_id']==14: #'迈瑞Mindray'
                                data['ownbusiness']=False 
                            if data['detailedproject_id']==12:
                                data['detailedproject_id']=1 
                            if data['detailedproject_id']==13:
                                data['detailedproject_id']=2
                            print('data',data)
                            PMRResearchDetail3.objects.create(researchlist_id=PMR_researchlist_id,is_active=True, ownbusiness=data['ownbusiness'], machinenumber=data['machinenumber'], detailedproject_id=data['detailedproject_id'],brand_id=data['brand_id'],machinemodel=data['machinemodel'],installdate=data['installdate'],endsupplier=data['endsupplier'],competitionrelation_id=data['competitionrelation_id'],machineseries=data['machineseries'],testprice=data['testprice'],expiration=data['expiration']).save()                    
                
                if not ownmachinedetail:
                    #批量删除PMRmachinedetail
                    if PMRmachinedetailnotGUOSAI:
                        PMRmachinedetailnotGUOSAI.update(is_active=False)
                        print('普美瑞公司中的该医院CRPSAA仪器全部删除，QT跟着全部删除')



            print('saverelated 保存成功')
            # form.save()      

            # # #如果完全新增，无法实现装机时间
            # for formset in formsets:  
            #     self.save_formset(request, form, formset, change=change)    





   #这是通过saverelated点击保存时已经存入detailcalculate的数据
    @admin.display(description='仪器总数')
    def detailcalculate_totalmachinenumber(self, obj):
        if obj.detailcalculate3.totalmachinenumber ==0:
            return  '--'
        else:
            return obj.detailcalculate3.totalmachinenumber
    detailcalculate_totalmachinenumber.admin_order_field = '-detailcalculate3__totalmachinenumber'
    
    @admin.display(description='我司仪器占比')
    def detailcalculate_ownmachinenumberpercent(self, obj):
        if obj.detailcalculate3.ownmachinepercent ==0:
            return '--'
        else:
            return '{:.1f}%'.format(obj.detailcalculate3.ownmachinepercent*100)
    detailcalculate_ownmachinenumberpercent.admin_order_field = '-detailcalculate3__ownmachinepercent'
    
    @admin.display(description='业务类型')
    def detailcalculate_newold(self, obj):
        return obj.detailcalculate3.newold

    @admin.display(ordering="-hospital__district", description='地区') 
    def hospital_district(self, obj):
        return obj.hospital.district
    
    @admin.display(ordering="hospital__hospitalclass",description='级别')
    def hospital_hospitalclass(self, obj):
        return obj.hospital.hospitalclass

    @admin.display(ordering="salesman1__chinesename",description='第一责任人')
    def salesman1_chinesename(self, obj):
        return obj.salesman1.chinesename

    @admin.display(ordering="salesman2__chinesename",description='第二责任人')
    def salesman2_chinesename(self, obj):
        return obj.salesman2.chinesename

    @admin.display(ordering="project__project",description='项目')
    def colored_project(self,obj):
        if obj.project.project=='CRP/SAA':
            color_code='red'  

        elif obj.project.project=='血球':
            color_code='orange'    

        elif obj.project.project=='流式':
            color_code='green'   

        elif obj.project.project=='生化免疫':
            color_code='blue'
 
        else:
            color_code='black' 
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,
                obj.project.project, )



#每季度目标额
    @admin.display(description='23/Q1目标')
    def salestarget_23_q1(self, obj):
        if obj.salestarget3_set.filter(year='2023',is_active=True)[0].q1target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.salestarget3_set.filter(year='2023',is_active=True)[0].q1target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_23_q1.admin_order_field = '-salestarget3__q1target'

    @admin.display(description='23/Q2目标')
    def salestarget_23_q2(self, obj):
        if obj.salestarget3_set.filter(year='2023',is_active=True)[0].q2target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.salestarget3_set.filter(year='2023',is_active=True)[0].q2target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_23_q2.admin_order_field = '-salestarget3__q2target'
  
    @admin.display(description='23/Q3目标')
    def salestarget_23_q3(self, obj):
        if obj.salestarget3_set.filter(year='2023',is_active=True)[0].q3target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.salestarget3_set.filter(year='2023',is_active=True)[0].q3target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_23_q3.admin_order_field = '-salestarget3__q3target'

    @admin.display(description='23/Q4目标')
    def salestarget_23_q4(self, obj):
        if obj.salestarget3_set.filter(year='2023',is_active=True)[0].q4target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.salestarget3_set.filter(year='2023',is_active=True)[0].q4target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)    
    salestarget_23_q4.admin_order_field = '-salestarget3__q4target'

    @admin.display(description='24/Q1目标')
    def salestarget_24_q1(self, obj):
        if obj.salestarget3_set.filter(year='2024',is_active=True)[0].q1target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.salestarget3_set.filter(year='2024',is_active=True)[0].q1target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_24_q1.admin_order_field = '-salestarget3__q1target'
    
    @admin.display(description='24/Q2目标')
    def salestarget_24_q2(self, obj):
        if obj.salestarget3_set.filter(year='2024',is_active=True)[0].q2target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.salestarget3_set.filter(year='2024',is_active=True)[0].q2target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_24_q2.admin_order_field = '-salestarget3__q2target'
    
    @admin.display(description='24/Q3目标')
    def salestarget_24_q3(self, obj):
        if obj.salestarget3_set.filter(year='2024',is_active=True)[0].q3target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.salestarget3_set.filter(year='2024',is_active=True)[0].q3target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_24_q3.admin_order_field = '-salestarget3__q3target'

    @admin.display(description='24/Q4目标')
    def salestarget_24_q4(self, obj):
        if obj.salestarget3_set.filter(year='2024',is_active=True)[0].q4target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.salestarget3_set.filter(year='2024',is_active=True)[0].q4target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_24_q4.admin_order_field = '-salestarget3__q4target'


#目标完成月
    @admin.display(description='23/Q1目标月')
    def completemonth_23_q1(self, obj):
        return obj.salestarget3_set.filter(year='2023',is_active=True)[0].q1completemonth
    completemonth_23_q1.admin_order_field = 'salestarget3__q1completemonth'

    @admin.display(description='23/Q2目标月')
    def completemonth_23_q2(self, obj):
        return obj.salestarget3_set.filter(year='2023',is_active=True)[0].q2completemonth
    completemonth_23_q2.admin_order_field = 'salestarget3__q2completemonth'
    
    @admin.display(description='23/Q3目标月')
    def completemonth_23_q3(self, obj):
        return obj.salestarget3_set.filter(year='2023',is_active=True)[0].q3completemonth
    completemonth_23_q3.admin_order_field = 'salestarget3__q3completemonth'

    @admin.display(description='23/Q4目标月')
    def completemonth_23_q4(self, obj):
        return obj.salestarget3_set.filter(year='2023',is_active=True)[0].q4completemonth
    completemonth_23_q4.admin_order_field = 'salestarget3__q4completemonth'    
    
    @admin.display(description='24/Q1目标月')
    def completemonth_24_q1(self, obj):
        return obj.salestarget3_set.filter(year='2024',is_active=True)[0].q1completemonth
    completemonth_24_q1.admin_order_field = 'salestarget3__q1completemonth'

    @admin.display(description='24/Q2目标月')
    def completemonth_24_q2(self, obj):
        return obj.salestarget3_set.filter(year='2024',is_active=True)[0].q2completemonth
    completemonth_24_q2.admin_order_field = 'salestarget3__q2completemonth'
    
    @admin.display(description='24/Q3目标月')
    def completemonth_24_q3(self, obj):
        return obj.salestarget3_set.filter(year='2024',is_active=True)[0].q3completemonth
    completemonth_24_q3.admin_order_field = 'salestarget3__q3completemonth'

    @admin.display(description='24/Q4目标月')
    def completemonth_24_q4(self, obj):
        return obj.salestarget3_set.filter(year='2024',is_active=True)[0].q4completemonth
    completemonth_24_q4.admin_order_field = 'salestarget3__q4completemonth'


#每季度实际完成额
    @admin.display(description='23/Q1实际')
    def actualsales_23_q1(self, obj):
        return obj.salestarget3_set.filter(year='2023',is_active=True)[0].q1actualsales
    actualsales_23_q1.admin_order_field = '-salestarget3__q1actualsales'

    @admin.display(description='23/Q2实际')
    def actualsales_23_q2(self, obj):
        return obj.salestarget3_set.filter(year='2023',is_active=True)[0].q2actualsales
    actualsales_23_q2.admin_order_field = '-salestarget3__q2actualsales'
    
    @admin.display(description='23/Q3实际')
    def actualsales_23_q3(self, obj):
        return obj.salestarget3_set.filter(year='2023',is_active=True)[0].q3actualsales
    actualsales_23_q3.admin_order_field = '-salestarget3__q3actualsales'

    @admin.display(description='23/Q4实际')
    def actualsales_23_q4(self, obj):
        return obj.salestarget3_set.filter(year='2023',is_active=True)[0].q4actualsales
    actualsales_23_q4.admin_order_field = '-salestarget3__q4actualsales'
    
    @admin.display(description='24/Q1实际')
    def actualsales_24_q1(self, obj):
        return obj.salestarget3_set.filter(year='2024',is_active=True)[0].q1actualsales
    actualsales_24_q1.admin_order_field = '-salestarget3__q1actualsales'

    @admin.display(description='24/Q2实际')
    def actualsales_24_q2(self, obj):
        return obj.salestarget3_set.filter(year='2024',is_active=True)[0].q2actualsales
    actualsales_24_q2.admin_order_field = '-salestarget3__q2actualsales'
    
    @admin.display(description='24/Q3实际')
    def actualsales_24_q3(self, obj):
        return obj.salestarget3_set.filter(year='2024',is_active=True)[0].q3actualsales
    actualsales_24_q3.admin_order_field = '-salestarget3__q3actualsales'

    @admin.display(description='24/Q4实际')
    def actualsales_24_q4(self, obj):
        return obj.salestarget3_set.filter(year='2024',is_active=True)[0].q4actualsales
    actualsales_24_q4.admin_order_field = '-salestarget3__q4actualsales'


#每季度实际完成率
    @admin.display(description='23/Q1完成率')
    def finishrate_23_q1(self, obj):
        sales_target = obj.salestarget3_set.filter(year='2023',is_active=True)[0]
        if sales_target.q1target and sales_target.q1target != 0:#如果target不是0
            finishrate = sales_target.q1actualsales / sales_target.q1target
            sales_target.q1finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0 #如果target是0 actual是0
            finishrate=0
            sales_target.q1finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)        
    finishrate_23_q1.admin_order_field = '-salestarget3__q1finishrate'

    @admin.display(description='23/Q2完成率')
    def finishrate_23_q2(self, obj):
        sales_target = obj.salestarget3_set.filter(year='2023',is_active=True)[0]
        if sales_target.q2target and sales_target.q2target != 0:#如果target不是0
            finishrate = sales_target.q2actualsales / sales_target.q2target
            sales_target.q2finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0 #如果target是0 actual是0
            finishrate=0
            sales_target.q2finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)        
    finishrate_23_q2.admin_order_field = '-salestarget3__q2finishrate'

    
    @admin.display(description='23/Q3完成率')
    def finishrate_23_q3(self, obj):
        sales_target = obj.salestarget3_set.filter(year='2023',is_active=True)[0]
        if sales_target.q3target and sales_target.q3target != 0:#如果target不是0
            finishrate = sales_target.q3actualsales / sales_target.q3target
            sales_target.q3finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0 #如果target是0 actual是0
            finishrate=0
            sales_target.q3finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)        
    finishrate_23_q3.admin_order_field = '-salestarget3__q3finishrate'

    @admin.display(description='23/Q4完成率')
    def finishrate_23_q4(self, obj):
        sales_target = obj.salestarget3_set.filter(year='2023',is_active=True)[0]
        if sales_target.q4target and sales_target.q4target != 0:#如果target不是0
            finishrate = sales_target.q4actualsales / sales_target.q4target
            sales_target.q4finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0 #如果target是0 actual是0
            finishrate=0
            sales_target.q4finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)        
    finishrate_23_q4.admin_order_field = '-salestarget3__q4finishrate'
    
    @admin.display(description='24/Q1完成率')
    def finishrate_24_q1(self, obj):
        sales_target = obj.salestarget3_set.filter(year='2024',is_active=True)[0]
        if sales_target.q1target and sales_target.q1target != 0:#如果target不是0
            finishrate = sales_target.q1actualsales / sales_target.q1target
            sales_target.q1finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0 #如果target是0 actual是0
            finishrate=0
            sales_target.q1finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)        
    finishrate_24_q1.admin_order_field = '-salestarget3__q1finishrate'

    @admin.display(description='24/Q2完成率')
    def finishrate_24_q2(self, obj):
        sales_target = obj.salestarget3_set.filter(year='2024',is_active=True)[0]
        if sales_target.q2target and sales_target.q2target != 0:#如果target不是0
            finishrate = sales_target.q2actualsales / sales_target.q2target
            sales_target.q2finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0 #如果target是0 actual是0
            finishrate=0
            sales_target.q2finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)        
    finishrate_24_q2.admin_order_field = '-salestarget3__q2finishrate'
    
    @admin.display(description='24/Q3完成率')
    def finishrate_24_q3(self, obj):
        sales_target = obj.salestarget3_set.filter(year='2024',is_active=True)[0]
        if sales_target.q3target and sales_target.q3target != 0:#如果target不是0
            finishrate = sales_target.q3actualsales / sales_target.q3target
            sales_target.q3finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0 #如果target是0 actual是0
            finishrate=0
            sales_target.q3finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)        
    finishrate_24_q3.admin_order_field = '-salestarget3__q3finishrate'
    
    @admin.display(description='24/Q4完成率')
    def finishrate_24_q4(self, obj):
        sales_target = obj.salestarget3_set.filter(year='2024',is_active=True)[0]
        if sales_target.q4target and sales_target.q4target != 0:#如果target不是0
            finishrate = sales_target.q4actualsales / sales_target.q4target
            sales_target.q4finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0 #如果target是0 actual是0
            finishrate=0
            sales_target.q4finishrate = finishrate
            sales_target.save()
            return '{:.1f}%'.format(finishrate*100)        
    finishrate_24_q4.admin_order_field = '-salestarget3__q4finishrate'

    #通过display计算的仪器值，不做任何保存！！！
    @admin.display(description='test仪器总数')
    def detail_qtysum(self, obj):        
        qty= obj.pmrresearchdetail3_set.filter(is_active=True).aggregate(sumsum=Sum("machinenumber"))   
        # print('qty',qty)
        totalseries_qty= obj.pmrresearchdetail3_set.filter(is_active=True,machineseries__isnull=False).aggregate(countseries=Count("machineseries"))  
        # print('totalseries_qty[countseries]',totalseries_qty['countseries'])
        distinctseries_qty=obj.pmrresearchdetail3_set.filter(is_active=True,machineseries__isnull=False).values('machineseries').distinct().count()
        # print('distinctseries_qty',distinctseries_qty)        
        totalqty=qty['sumsum']-totalseries_qty['countseries']+distinctseries_qty
        # print('totalqty',totalqty)
        if not totalqty:
            ret = '--'
        else:
            ret = totalqty
        return ret
    #通过display计算的仪器值，不做任何保存！！！
    @admin.display(description='test我司仪器数')
    def detail_own_qtysum(self, obj):        
        qtyown= obj.pmrresearchdetail3_set.filter(Q(is_active=True) & Q(ownbusiness=True)).aggregate(sumsum=Sum("machinenumber"))
        # print('qtyown',qtyown)
        totalseries_own_qty= obj.pmrresearchdetail3_set.filter(is_active=True,machineseries__isnull=False,ownbusiness=True).aggregate(countseries=Count("machineseries"))  
        # print('totalseries_own_qty',totalseries_own_qty)
        distinctseries_own_qty=obj.pmrresearchdetail3_set.filter(is_active=True,machineseries__isnull=False,ownbusiness=True).values('machineseries').distinct().count()
        # print('distinctseries_own_qty',distinctseries_own_qty)
        if not qtyown['sumsum']:
            qtyown['sumsum']=0
        totalownqty=qtyown['sumsum']-totalseries_own_qty['countseries']+distinctseries_own_qty
        if not totalownqty:
            ret = '--'
        else:
            ret = totalownqty
        return ret

    @admin.display(description='项目细分') 
    def detail_detailedproject(self, obj):        
        detailedprojects= obj.pmrresearchdetail3_set.filter(is_active=True)
        if not detailedprojects:
            ret = '--'
        elif len(detailedprojects)>1:
             ret = '/'.join(str(i.detailedproject.detailedproject) for i in detailedprojects if i.machinenumber != 0 )             
        else:
            if detailedprojects[0].machinenumber != 0 :
                ret=str(detailedprojects[0].detailedproject.detailedproject)
            else:
                ret='--'
        return ret

    @admin.display(description='是否我司业务') 
    def detail_ownbusiness(self, obj):        
        ownbusinesses= obj.pmrresearchdetail3_set.filter(is_active=True)
        if not ownbusinesses:
            ret = '--'
        elif len(ownbusinesses)>1:
             ret = '/'.join(str(i.ownbusiness) for i in ownbusinesses if i.machinenumber != 0 )
             ret=ret.replace('True','是')  
             ret=ret.replace('False','否')  
        else:
            if ownbusinesses[0].machinenumber != 0:
                ret=str(ownbusinesses[0].ownbusiness)
                ret=ret.replace('True','是')  
                ret=ret.replace('False','否')  
            else:
                ret='--'
        return ret


    @admin.display(description='仪器型号') 
    def detail_machinemodel(self, obj):        
        machinemodels= obj.pmrresearchdetail3_set.filter(is_active=True)
        # print('ownbusinesses',ownbusinesses)
        if not machinemodels:
            ret = '--'
        elif len(machinemodels)>1:
             ret = '/'.join(str(i.machinemodel) for i in machinemodels if i.machinenumber != 0)               
        else:
            if machinemodels[0].machinenumber != 0:
                ret=str(machinemodels[0].machinemodel)
            else:
                ret='--'
        return ret

    @admin.display(description='仪器序列号') 
    def detail_machineseries(self, obj):        
        machineserieses= obj.pmrresearchdetail3_set.filter(is_active=True)
        if not machineserieses:
            ret = '--'
        elif len(machineserieses)>1:
             ret = '/'.join(str(i.machineseries) for i in machineserieses if i.machinenumber != 0)               
        else:
            if machineserieses[0].machineseries != 0:
                ret=str(machineserieses[0].machineseries)
            else:
                ret='--'
        return ret


    @admin.display(description='竞品关系点') 
    def detail_competitor(self, obj):        
        competitors= obj.pmrresearchdetail3_set.filter(is_active=True)
        # print('ownbusinesses',ownbusinesses)
        if not competitors:
            ret = '--'
        elif len(competitors)>1:
             ret = '/'.join(str(i.competitionrelation.competitionrelation) for i in competitors if i.machinenumber != 0 )             
        else:
            if competitors[0].machinenumber != 0 :
                ret=str(competitors[0].competitionrelation.competitionrelation)
            else:
                ret='--'
        return ret

    @admin.display(description='仪器品牌') 
    def detail_brands(self, obj):        
        brands= obj.pmrresearchdetail3_set.filter(is_active=True)
        # print('ownbusinesses',ownbusinesses)
        if not brands:
            ret = '--'
        elif len(brands)>1:
             ret = '/'.join(str(i.brand.brand) for i in brands if i.machinenumber != 0)
               
        else:
            if brands[0].machinenumber != 0:
                ret=str(brands[0].brand.brand)
            else:
                ret='--'
        return ret


    @admin.display(description='仪器装机日期') 
    def detail_installdate(self, obj):        
        installdates= obj.pmrresearchdetail3_set.filter(is_active=True)
        # print('ownbusinesses',ownbusinesses)
        if not installdates:
            ret = '--'
        elif len(installdates)>1:
             ret = '/'.join(str(i.installdate) for i in installdates if i.machinenumber != 0)
               
        else:
            if installdates[0].machinenumber != 0 :
                ret=str(installdates[0].installdate)
            else:
                ret='--'
        return ret


 #新增动作————统计按钮
    
    actions = ['calculate']
    def calculate(self, request, queryset):
        for i in queryset:
            #更新是新客户还是老客户
            if i.pmrresearchdetail3_set.filter(Q(is_active=True)&Q(ownbusiness=True) & ~Q(machinenumber='0')) :
                i.detailcalculate3.newold='已有业务(含我司仪器)'
            else:
                i.detailcalculate3.newold='新商机(不含我司仪器)'
            
            #更新仪器总数量
            qty= i.pmrresearchdetail3_set.filter(is_active=True).aggregate(sumsum=Sum("machinenumber"))   
            # print('我在action中的仪器总数',qty)
            totalseries_qty= i.pmrresearchdetail3_set.filter(Q(is_active=True) & Q(machineseries__isnull=False) & ~Q(machinenumber=0)).aggregate(countseries=Count("machineseries"))  
            distinctseries_qty=i.pmrresearchdetail3_set.filter(Q(is_active=True) & Q(machineseries__isnull=False) & ~Q(machinenumber=0)).values('machineseries').distinct().count()
            machinetotalnumber=qty['sumsum']
            machinetotalseries_qty=totalseries_qty['countseries']    
            # print('machinetotalnumber,machinetotalseries_qty,distinctseries_qty',machinetotalnumber,machinetotalseries_qty,distinctseries_qty)        
            if not qty:
                machinenumberret=0
            if not machinetotalnumber:
                machinenumberret=0
            else:    
                if machinetotalseries_qty:
                    totalqty=machinetotalnumber-machinetotalseries_qty+distinctseries_qty 
                    machinenumberret= totalqty        
                else:
                    machinenumberret = machinetotalnumber
            i.detailcalculate3.totalmachinenumber=machinenumberret

            #更新我司仪器数    
            qtyown= i.pmrresearchdetail3_set.filter(Q(is_active=True) & Q(ownbusiness=True)).aggregate(sumsum=Sum("machinenumber"))
            totalseries_own_qty= i.pmrresearchdetail3_set.filter(Q(is_active=True) & Q(machineseries__isnull=False) & Q(ownbusiness=True) & ~Q(machinenumber=0)).aggregate(countseries=Count("machineseries"))  
            distinctseries_own_qty=i.pmrresearchdetail3_set.filter(Q(is_active=True) & Q(machineseries__isnull=False) & Q(ownbusiness=True) & ~Q(machinenumber=0)).values('machineseries').distinct().count()
            machinetotalnumberown=qtyown['sumsum']
            machinetotalseries_qtyown=totalseries_own_qty['countseries']
            if not qtyown:
                ownmachinenumberret=0
            if not machinetotalnumberown:
                ownmachinenumberret=0
            else:
                if machinetotalseries_qtyown:
                    totalownqty=machinetotalnumberown-machinetotalseries_qtyown+distinctseries_own_qty
                    ownmachinenumberret=totalownqty            
                else:
                    ownmachinenumberret = machinetotalnumberown
            i.detailcalculate3.ownmachinenumber=ownmachinenumberret

            #更新我司仪器占比     
            if not qtyown or ownmachinenumberret==0 or ownmachinenumberret=='--' :
                ret=0
            elif not qty or machinenumberret==0 or  machinenumberret =='--':
                ret=0
            else:
                ret=ownmachinenumberret/machinenumberret
            i.detailcalculate3.ownmachinepercent=ret

#考虑直接在calculatedetail中匹配？？！！！
            # #更新22年的月均销售额
            # sumpermonth_total= i.pmrresearchdetail3_set.filter(is_active=True).aggregate(sumsum=Sum("sumpermonth"))
            # if not sumpermonth_total['sumsum']:
            #     ret = 0
            # else:
            #     ret = sumpermonth_total['sumsum']
            # i.detailcalculate.totalsumpermonth=ret


             #更新是否我司业务集合在detailcalculate表中
            ownbusinesses= i.pmrresearchdetail3_set.filter(is_active=True)
            if not ownbusinesses:
                ret = '--'
            elif len(ownbusinesses)>1:
                ret = '/'.join(str(i.ownbusiness) for i in ownbusinesses if i.machinenumber != 0 )
                ret=ret.replace('True','是')  
                ret=ret.replace('False','否')  
            else:
                if ownbusinesses[0].machinenumber != 0:
                    ret=str(ownbusinesses[0].ownbusiness)
                    ret=ret.replace('True','是')  
                    ret=ret.replace('False','否')  
                else:
                    ret='--'
            i.detailcalculate3.ownbusinesscombine=ret

            #更新项目细分集合在detailcalculate表中
            detailedprojects= i.pmrresearchdetail3_set.filter(is_active=True)
            if not detailedprojects:
                ret = '--'
                
            elif len(detailedprojects)>1:
                detailedprojectslist=[]
                for eachdetail in detailedprojects:
                    if eachdetail.machinenumber != 0:
                        if eachdetail.detailedproject:
                            detailedprojectslist.append(str(eachdetail.detailedproject.detailedproject))
                        else:
                            detailedprojectslist.append('None')
                ret = '/'.join(detailedprojectslist)
                
            else:
                if detailedprojects[0].machinenumber != 0:
                    if detailedprojects[0].detailedproject:
                        ret=str(detailedprojects[0].detailedproject.detailedproject)
                    else:
                        ret='None'
                else:
                    ret='--'
            i.detailcalculate3.detailedprojectcombine=ret


            #更新品牌集合在detailcalculate表中
            brands= i.pmrresearchdetail3_set.filter(is_active=True)
            if not brands:
                ret = '--'
            elif len(brands)>1:
                brandslist=[]
                for eachdetail in brands:
                    if eachdetail.machinenumber != 0:
                        if eachdetail.brand:
                            brandslist.append(str(eachdetail.brand.brand))
                        else:
                            brandslist.append('None')
                ret = '/'.join(brandslist)
                
            else:
                if brands[0].machinenumber != 0:
                    if brands[0].brand:
                        ret=str(brands[0].brand.brand)
                    else:
                        ret='None'
                else:
                    ret='--'
            i.detailcalculate3.brandscombine=ret

            #更新仪器型号集合在detailcalculate表中
            machinemodels= i.pmrresearchdetail3_set.filter(is_active=True)
            if not machinemodels:
                ret = '--'
            elif len(machinemodels)>1:
                ret = '/'.join(str(i.machinemodel) for i in machinemodels if i.machinenumber != 0)               
            else:
                if machinemodels[0].machinenumber != 0:
                    ret=str(machinemodels[0].machinemodel)
                else:
                    ret='--'
            i.detailcalculate3.machinemodelcombine=ret

            #更新仪器数量集合在detailcalculate表中
            machinenumbers= i.pmrresearchdetail3_set.filter(is_active=True)
            if not machinenumbers:
                ret = '--'
            elif len(machinenumbers)>1:
                ret = '/'.join(str(i.machinenumber) for i in machinenumbers if i.machinenumber != 0)               
            else:
                if machinenumbers[0].machinenumber != 0:
                    ret=str(machinenumbers[0].machinenumber)
                else:
                    ret='--'
            i.detailcalculate3.machinenumbercombine=ret

            #更新仪器序列号集合在detailcalculate表中
            machineserieses= i.pmrresearchdetail3_set.filter(is_active=True)
            if not machineserieses:
                ret = '--'
            elif len(machineserieses)>1:
                ret = '/'.join(str(i.machineseries) for i in machineserieses if i.machinenumber != 0)               
            else:
                if machineserieses[0].machineseries != 0:
                    ret=str(machineserieses[0].machineseries)
                else:
                    ret='--'
            i.detailcalculate3.machineseriescombine=ret


            #更新装机时间集合在detailcalculate表中
            installdates= i.pmrresearchdetail3_set.filter(is_active=True)
            if not installdates:
                ret = '--'
            elif len(installdates)>1:
                ret = '/'.join(str(i.installdate) for i in installdates if i.machinenumber != 0)
                
            else:
                if installdates[0].machinenumber != 0 :
                    ret=str(installdates[0].installdate)
                else:
                    ret='--'
            i.detailcalculate3.installdatescombine=ret

            #更新竞品关系点集合在detailcalculate表中
            competitors= i.pmrresearchdetail3_set.filter(is_active=True)
            if not competitors:
                ret = '--'
            elif len(competitors)>1:
                competitorslist=[]
                for eachdetail in competitors:
                    if eachdetail.machinenumber != 0:
                        if eachdetail.competitionrelation:
                            competitorslist.append(str(eachdetail.competitionrelation.competitionrelation))
                        else:
                            competitorslist.append('None')
                ret = '/'.join(competitorslist)
                
            else:
                if competitors[0].machinenumber != 0:
                    if competitors[0].competitionrelation:
                        ret=str(competitors[0].competitionrelation.competitionrelation)
                    else:
                        ret='None'
                else:
                    ret='--'
            i.detailcalculate3.competitionrelationcombine=ret

            i.detailcalculate3.save()

            #更新装机时间在detail表中
            qs_fk=i.pmrresearchdetail3_set.all()
            for j in qs_fk:
                if not j.installdate:
                    ret = '--'
                else:
                    if (datetime.now().date() - j.installdate).days >= 1825:
                        ret = '已超5年'
                    else:
                        ret = '5年内'            
                j.expiration=ret
                j.save()
            i.save()           

            #补充不同公司的同一家医院的主任姓名和电话，在空的时候或者姓名相同的时候，才覆盖
            samehospital=PMRResearchList3.objects.filter(Q(hospital_id=i.hospital.id))
            for x in samehospital:
                if not x.contactname:
                    x.contactname=i.contactname
                    if not x.contactmobile:
                        x.contactmobile=i.contactmobile

                if x.contactname == i.contactname and not x.contactmobile:
                    x.contactmobile=i.contactmobile
                x.save()


            #不同公司的同一家医院，CRP/SAA项目，补充总测试数
            if i.project.project=='CRP/SAA' and i.testspermonth:
                sameCRPSAA=PMRResearchList3.objects.filter(Q(hospital_id=i.hospital.id) & Q(project__project='CRP/SAA') & Q(company_id=1) )
                for z in sameCRPSAA:
                    if not z.testspermonth:
                        z.testspermonth=i.testspermonth
                        z.save()
            i.save()
            '''
            #如果项目大类是CRPSAA，则普美瑞和其田有重复的地方，在普美瑞中，国赛是自有业务、迈瑞是竞品，在其田中迈瑞是自有业务、国赛是竞品。
            # 需要将普美瑞中填的完整的国赛导入其田当作竞品，把其田中填的完整的迈瑞导入普美瑞中当作竞品
            if i.project.project=='CRP/SAA':
                #找出目前obj下面的仪器信息，active的、所有仪器，需要和其田的CRP/SAA比较，需要把其田的迈瑞的和其他竞品的都拿过来
                ownmachinedetail= PMRResearchDetail3.objects.filter(Q(researchlist_id=i.id) & Q(is_active=True) & ~Q(machinenumber=0) & ~Q(brand__brand='未知') & (Q(detailedproject_id=12) | Q(detailedproject_id=13)))
                #找出其田下面的，同一家医院同一个项目的同一个人的，所有仪器obj
                PMRmachinedetail= PMRResearchDetail3.objects.filter(Q(researchlist__hospital__id=i.hospital.id) & Q(researchlist__project__project='CRP/SAA') & Q(is_active=True) & ~Q(brand__brand='未知') &  ~Q(machinenumber=0) & Q(researchlist__company__id=1) & (Q(detailedproject_id=1) | Q(detailedproject_id=2)))
                print('PMRmachinedetail',PMRmachinedetail)

                PMRresearchlist=PMRResearchList3.objects.filter(hospital__id=i.hospital.id,project__project='CRP/SAA', company__id=1)
                print('PMRresearchlist',PMRresearchlist)

                owneachactivedetailllist=[]
                #如果PMR这边的CRPSAA有仪器数据
                if ownmachinedetail:
                    for owneachactivedetail in ownmachinedetail:
                        owneachactivedetailldict={}
                        owneachactivedetailldict['detailedproject_id']=owneachactivedetail.detailedproject.id if owneachactivedetail.detailedproject else None
                        owneachactivedetailldict['ownbusiness']=owneachactivedetail.ownbusiness if owneachactivedetail.ownbusiness else False
                        owneachactivedetailldict['brand_id']=owneachactivedetail.brand.id if owneachactivedetail.brand else None
                        owneachactivedetailldict['machinemodel']=owneachactivedetail.machinemodel if owneachactivedetail.machinemodel else None
                        owneachactivedetailldict['machinenumber']=owneachactivedetail.machinenumber if owneachactivedetail.machinenumber else None
                        owneachactivedetailldict['installdate']=owneachactivedetail.installdate if owneachactivedetail.installdate else None
                        owneachactivedetailldict['expiration']=owneachactivedetail.expiration if owneachactivedetail.expiration else None
                        owneachactivedetailldict['endsupplier']=owneachactivedetail.endsupplier if owneachactivedetail.endsupplier else None
                        owneachactivedetailldict['competitionrelation_id']=owneachactivedetail.competitionrelation.id if owneachactivedetail.competitionrelation else None
                        owneachactivedetailldict['machineseries']=owneachactivedetail.machineseries if owneachactivedetail.machineseries else None
                        owneachactivedetailldict['testprice']=owneachactivedetail.testprice if owneachactivedetail.testprice else None
                        owneachactivedetailllist.append(owneachactivedetailldict)

                    ownbrandlist= list(set(item['brand_id'] for item in owneachactivedetailllist))
                    print('ownbrandlist',ownbrandlist)

                    if PMRresearchlist:#先判断对方是否有这个医院项目
                        PMR_researchlist_id=PMRresearchlist[0].id
                        print('对应的其田的CRP/SAA的id',PMR_researchlist_id)  
                        PMRbrandlist=[] 
                        PMReachactivedetailllist=[]
                        if PMRmachinedetail:#然后判断对方有没有仪器数据
                            for PMReachactivedetail in PMRmachinedetail:
                                PMReachactivedetailldict={}
                                PMReachactivedetailldict['detailedproject_id']=PMReachactivedetail.detailedproject.id if PMReachactivedetail.detailedproject else None
                                PMReachactivedetailldict['ownbusiness']=PMReachactivedetail.ownbusiness if PMReachactivedetail.ownbusiness else False
                                PMReachactivedetailldict['brand_id']=PMReachactivedetail.brand.id if PMReachactivedetail.brand else None
                                PMReachactivedetailldict['machinemodel']=PMReachactivedetail.machinemodel if PMReachactivedetail.machinemodel else None
                                PMReachactivedetailldict['machinenumber']=PMReachactivedetail.machinenumber if PMReachactivedetail.machinenumber else None
                                PMReachactivedetailldict['installdate']=PMReachactivedetail.installdate if PMReachactivedetail.installdate else None
                                PMReachactivedetailldict['expiration']=PMReachactivedetail.expiration if PMReachactivedetail.expiration else None
                                PMReachactivedetailldict['endsupplier']=PMReachactivedetail.endsupplier if PMReachactivedetail.endsupplier else None
                                PMReachactivedetailldict['competitionrelation_id']=PMReachactivedetail.competitionrelation.id if PMReachactivedetail.competitionrelation else None
                                PMReachactivedetailldict['machineseries']=PMReachactivedetail.machineseries if PMReachactivedetail.machineseries else None
                                PMReachactivedetailldict['testprice']=PMReachactivedetail.testprice if PMReachactivedetail.testprice else None
                                PMReachactivedetailllist.append(PMReachactivedetailldict)

                            PMRbrandlist= list(set(item['brand_id'] for item in PMReachactivedetailllist))
                            print('PMRbrandlist',PMRbrandlist)

                            PMRmorebrandlist = [item for item in PMRbrandlist if item not in ownbrandlist]
                            print('PMRmorebrandlist',PMRmorebrandlist)
                            OWNmorebrandlist = [item for item in ownbrandlist if item not in PMRbrandlist]
                            print('OWNmorebrandlist',OWNmorebrandlist)
                            # SAMEbrandlist = [item for item in ownbrandlist if item in PMRbrandlist]
                            # print('SAMEbrandlist',SAMEbrandlist)

                            #如果PMR有额外品牌，则在此obj中新增仪器
                            if PMRmorebrandlist:
                                for data in PMReachactivedetailllist:#遍历PMR那边对应的所有仪器                              
                                    if data['brand_id'] in PMRmorebrandlist and data['brand_id']!=14 : #PMR中的14是迈瑞，但是迈瑞在QT中才是准的，所以去除
                                        #如果该仪器在PMR有而QT没有，需要在QT这里添加进去
                                        if data['brand_id']== 9: #国赛于QT来说是竞品，要变成False
                                            data['ownbusiness']=False    
                                        if data['detailedproject_id']==1:
                                            data['detailedproject_id']=12  
                                        if data['detailedproject_id']==2:
                                            data['detailedproject_id']=13  
                                        print('添加到PMR里面的data',data)
                                        PMRResearchDetail3.objects.create(researchlist_id=i.id,is_active=True, ownbusiness=data['ownbusiness'], machinenumber=data['machinenumber'], detailedproject_id=data['detailedproject_id'],brand_id=data['brand_id'],machinemodel=data['machinemodel'],installdate=data['installdate'],endsupplier=data['endsupplier'],competitionrelation_id=data['competitionrelation_id'],machineseries=data['machineseries'],testprice=data['testprice'],expiration=data['expiration']).save()                    
                            
                            #如果QT有额外品牌，则在对应的PMR那边新增仪器
                            if OWNmorebrandlist:
                                for data in owneachactivedetailllist:#遍历QT自己所有的仪器
                                    if data['brand_id'] in OWNmorebrandlist and  data['brand_id']!=9 : #QT中的9是国赛，但是国赛在PMR中才是准的，所以去除
                                        #若该仪器在QT有而PMR没有的品牌列表中，需要到PMR那边去添加该仪器
                                        if data['brand_id']== 14:
                                            data['ownbusiness']=False
                                        if data['detailedproject_id']==12:
                                            data['detailedproject_id']=1 
                                        if data['detailedproject_id']==13:
                                            data['detailedproject_id']=2
                                        print('添加到PMR里面的data',data)
                                        PMRResearchDetail3.objects.create(researchlist_id=PMR_researchlist_id,is_active=True, ownbusiness=data['ownbusiness'], machinenumber=data['machinenumber'], detailedproject_id=data['detailedproject_id'],brand_id=data['brand_id'],machinemodel=data['machinemodel'],installdate=data['installdate'],endsupplier=data['endsupplier'],competitionrelation_id=data['competitionrelation_id'],machineseries=data['machineseries'],testprice=data['testprice'],expiration=data['expiration']).save()                    
                        
                        #如果对方没有数据，则直接添加到对方
                        if not PMRmachinedetail:
                            for data in owneachactivedetailllist:#遍历QT自己所有的仪器
                                if data['brand_id']==14 : 
                                    data['ownbusiness']=False
                                if data['brand_id']== 9:
                                    data['ownbusiness']=True
                                if data['detailedproject_id']==12:
                                    data['detailedproject_id']=1
                                if data['detailedproject_id']==13:
                                    data['detailedproject_id']=2
                                print('添加到PMR里面的data',data)
                                PMRResearchDetail3.objects.create(researchlist_id=PMR_researchlist_id,is_active=True, ownbusiness=data['ownbusiness'], machinenumber=data['machinenumber'], detailedproject_id=data['detailedproject_id'],brand_id=data['brand_id'],machinemodel=data['machinemodel'],installdate=data['installdate'],endsupplier=data['endsupplier'],competitionrelation_id=data['competitionrelation_id'],machineseries=data['machineseries'],testprice=data['testprice'],expiration=data['expiration']).save()                    
                 


                if not ownmachinedetail:
                    if PMRresearchlist:#先判断对方是否有这个医院项目
                        PMR_researchlist_id=PMRresearchlist[0].id
                        print('对应的其田的CRP/SAA的id',PMR_researchlist_id)   
                        PMReachactivedetailllist=[]
                        if PMRmachinedetail:#然后判断对方有没有仪器数据
                            for PMReachactivedetail in PMRmachinedetail:
                                PMReachactivedetailldict={}
                                PMReachactivedetailldict['detailedproject_id']=PMReachactivedetail.detailedproject.id if PMReachactivedetail.detailedproject else None
                                PMReachactivedetailldict['ownbusiness']=PMReachactivedetail.ownbusiness if PMReachactivedetail.ownbusiness else False
                                PMReachactivedetailldict['brand_id']=PMReachactivedetail.brand.id if PMReachactivedetail.brand else None
                                PMReachactivedetailldict['machinemodel']=PMReachactivedetail.machinemodel if PMReachactivedetail.machinemodel else None
                                PMReachactivedetailldict['machinenumber']=PMReachactivedetail.machinenumber if PMReachactivedetail.machinenumber else None
                                PMReachactivedetailldict['installdate']=PMReachactivedetail.installdate if PMReachactivedetail.installdate else None
                                PMReachactivedetailldict['expiration']=PMReachactivedetail.expiration if PMReachactivedetail.expiration else None
                                PMReachactivedetailldict['endsupplier']=PMReachactivedetail.endsupplier if PMReachactivedetail.endsupplier else None
                                PMReachactivedetailldict['competitionrelation_id']=PMReachactivedetail.competitionrelation.id if PMReachactivedetail.competitionrelation else None
                                PMReachactivedetailldict['machineseries']=PMReachactivedetail.machineseries if PMReachactivedetail.machineseries else None
                                PMReachactivedetailldict['testprice']=PMReachactivedetail.testprice if PMReachactivedetail.testprice else None
                                PMReachactivedetailllist.append(PMReachactivedetailldict)


                            for data in PMReachactivedetailllist:#遍历QT那边对应的所有仪器                              
                                if data['brand_id']==9 : 
                                    data['ownbusiness']=False 
                                if data['brand_id']== 14: 
                                    data['ownbusiness']=True    
                                if data['detailedproject_id']==1:
                                    data['detailedproject_id']=12  
                                if data['detailedproject_id']==2:
                                    data['detailedproject_id']=13  
                                print('添加到PMR里面的data',data)
                                PMRResearchDetail3.objects.create(researchlist_id=i.id,is_active=True, ownbusiness=data['ownbusiness'], machinenumber=data['machinenumber'], detailedproject_id=data['detailedproject_id'],brand_id=data['brand_id'],machinemodel=data['machinemodel'],installdate=data['installdate'],endsupplier=data['endsupplier'],competitionrelation_id=data['competitionrelation_id'],machineseries=data['machineseries'],testprice=data['testprice'],expiration=data['expiration']).save()                    
                i.save()       

                '''



    calculate.short_description = "统计" 
    calculate.type = 'info'
    calculate.style = 'color:white;'







@admin.register(PMRResearchDetail3)
class PMRResearchDetailAdmin(GlobalAdmin): #ExportMixin
    # resource_class = PMRResearchDetailResource

    exclude = ('id','createtime','updatetime')
    search_fields=['researchlist__hospital__hospitalname','brand__brand','machinemodel','competitionrelation__competitionrelation']
    list_filter = ['researchlist__hospital__district','researchlist__hospital__hospitalclass',ProjectFilterforDetail,SalesmanFilterforDetail,'competitionrelation','ownbusiness','expiration']


    list_display_links =('list_hospitalname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('list_district','list_hospitalclass','list_hospitalname','list_salesman1','list_project', 
                    'renamed_detailedproject','ownbusiness','brand','machinemodel','renamed_machineseries','machinenumber','installdate','colored_expiration','testprice','endsupplier','colored_competitionrelation')
    autocomplete_fields=['researchlist','brand']
    # fields=('researchlist__project__project','detailedproject','ownbusiness','band','machinemodel')
    ordering = ('-researchlist__hospital__district',
                Case(
                        When(researchlist__hospital__hospitalclass='三级', then=Value(1)),
                        When(researchlist__hospital__hospitalclass='二级', then=Value(2)),
                        When(researchlist__hospital__hospitalclass='一级', then=Value(3)),
                        When(researchlist__hospital__hospitalclass='未定级', then=Value(4)),
                        output_field=IntegerField(),
                    ),
                'researchlist__hospital__hospitalname','researchlist__salesman1','researchlist__project',)
    # ordering = ('-id',)
    QT_view_group_list = ['boss','pmrmanager','QTmanager','allviewonly']

    # def has_export_permission(self, request):
    #     if request.user.is_superuser:
    #         return True
    #     user_in_group_list = request.user.groups.values('name')
    #     for user_in_group_dict in user_in_group_list:
    #         if user_in_group_dict['name'] in ['pmrdirectsales','pmrmanager','QTmanager','WDmanager']:
    #             return True
    #         else:
    #             return False
    

    # def get_export_formats(self):
    #     return [base_formats.XLSX]
    
    
    # def get_export_queryset(self, request):
    #     queryset = super().get_export_queryset(request)
    #     if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
    #         queryset = queryset
    #     else: 
    #         queryset = queryset.filter((Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__salesman1=request.user)&Q(researchlist__company_id=2))|(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__salesman2=request.user)&Q(researchlist__company_id=2)))
    #     return queryset


    def get_actions(self, request):
        actions = super(PMRResearchDetailAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions



    #只显示未被假删除的项目
    #------get_queryset-----------查询-------------------
    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的服务器"""
        qs = super(PMRResearchDetailAdmin, self).get_queryset(request)
        print('我在PMRResearchDetailAdmin-get_queryset')
        #通过外键连list中的负责人名称
        if request.user.is_superuser :
            return qs.filter(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__company_id=2))
        
                
        # <QuerySet [{'name': 'pmrdirectsales'}, {'name': 'QTmanager'}]>
        user_in_group_list = request.user.groups.values('name')
        print(user_in_group_list)
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.QT_view_group_list:
                 # print('我在模型里')
                return qs.filter(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__company_id=2))            
        
        #detail active ,list active 同时人员是自己
        return qs.filter((Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__salesman1=request.user)&Q(researchlist__company_id=2))|(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__salesman2=request.user)&Q(researchlist__company_id=2)))

        

    #用来控制list表中的inline的删除权限??????????????
    def has_delete_permission(self, request,obj=None):
        if obj==None:
            return True
        if request.user.is_superuser: 
            print('我在PmrResearchDETAILAdmin has delete permission: SUPERUSER ',super().has_delete_permission(request, obj))
            return super().has_delete_permission(request, obj)      
        elif obj.researchlist.salesman1==request.user or request.user.groups.values()[0]['name'] =='boss':          
            print('我在PmrResearchDETAILAdmin has delete permission:ELIF obj.salesman1',obj.researchlist.salesman1)
            return super().has_delete_permission(request, obj)  
       
        else:
            print('我在PmrResearchDETAILAdmin has delete permission:else')
            return False   
    
    #控制detail详情表中点进去后的红色删除
    def delete_model(self, request, obj):
        print('我在DETAILADMIN delete_model,, obj.researchlist.salesman1',obj.researchlist.salesman1)
        if request.user.is_superuser or obj.researchlist.salesman1==request.user or request.user.groups.values()[0]['name'] =='boss':   
            # print('delete_model detail 已假删')          
            obj.is_active = False 
            obj.researchlist.operator=request.user
            obj.save()

    # #需要核对
    # def delete_queryset(self,request, queryset):        
    #     print('我在delete_queryset')
    #     for delete_obj in queryset:     
    #         print('delete_queryset delete_obj',delete_obj,delete_obj.researchlist.salesman1)                    
    #         if request.user.is_superuser or delete_obj.researchlist.salesman1==request.user or request.user.groups.values()[0]['name'] =='boss':     
    #             delete_obj.is_active=False
    #             print('delete_queryset detail 已假删')
    #             delete_obj.operator=request.user
    #             delete_obj.save()



    # # 外键只显示active的(但是会被autocomplete覆盖，所以要在外键对应的“一”表的admin中重写getsearchresult)   
    # def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
    #     context['adminform'].form.fields['researchlist'].queryset = PMRResearchList.objects.filter(is_active=True)
    #     context['adminform'].form.fields['detailedproject'].queryset = ProjectDetail.objects.filter(is_active=True)
    #     context['adminform'].form.fields['brand'].queryset = Brand.objects.filter(is_active=True)
    #     context['adminform'].form.fields['competitionrelation'].queryset = CompetitionRelation.objects.filter(is_active=True)
    #     return super(PMRResearchDetailAdmin, self).render_change_form(request, context, add, change, form_url, obj)

#一下变化，在list的inline中有体现，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'researchlist': 
            kwargs["queryset"] = PMRResearchList3.objects.filter(is_active=True) 
        if db_field.name == 'detailedproject': 
            kwargs["queryset"] = ProjectDetail3.objects.filter(is_active=True) 
        if db_field.name == 'brand':  
            kwargs["queryset"] = Brand.objects.filter(is_active=True) 
        if db_field.name == 'competitionrelation': 
            kwargs["queryset"] = CompetitionRelation.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    #限制长度    
    @admin.display(ordering="-researchlist__hospital__district",description='区域')
    def list_district(self, obj):
        if len(str(obj.researchlist.hospital.district))>2:
            return '{}'.format(str(obj.researchlist.hospital.district)[0:2])
        else:
            return obj.researchlist.hospital.district

    @admin.display(ordering="researchlist__hospital__hospitalclass",description='级别')
    def list_hospitalclass(self, obj):
        return obj.researchlist.hospital.hospitalclass
    
    @admin.display(ordering="researchlist__hospital__hospitalname",description='医院名称')
    def list_hospitalname(self, obj):
        return obj.researchlist.hospital.hospitalname
    
    @admin.display(ordering="detailedproject",description='项目细分')
    def renamed_detailedproject(self, obj):
        return obj.detailedproject
    
    @admin.display(ordering="machineseries",description='序列号')
    def renamed_machineseries(self, obj):
        return obj.machineseries


    @admin.display(ordering="researchlist__salesman1__chinesename",description='第一负责人')
    def list_salesman1(self, obj): #用relatedname
        return obj.researchlist.salesman1.chinesename

    @admin.display(ordering="researchlist__project__project",description='项目')
    def list_project(self,obj):
        if not obj.researchlist.project.project:
            obj.researchlist.project.project = '--'
            color_code = 'black'

        elif obj.researchlist.project.project=='CRP/SAA':
            color_code='red'  

        elif obj.researchlist.project.project=='血球':
            color_code='orange'    

        elif obj.researchlist.project.project=='流式':
            color_code='green'   

        elif obj.researchlist.project.project=='生化免疫':
            color_code='blue'

        else:
            color_code='black' 


        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,
                obj.researchlist.project.project, )

    @admin.display(ordering="-expiration",description='装机时间')
    def colored_expiration(self,obj):
    # """自定义列表字段, 根据数据单截止日期和当前日期判断是否过期,并对数据库进行更新"""

        if not obj.expiration:
            ret='--'
            color_code = 'black'
        if obj.expiration=='--':
            ret='--'
            color_code = 'black'
        if obj.expiration=='已超5年':
            color_code = 'red'
            ret='已超5年'
        if obj.expiration=='5年内':
            ret='5年内'
            color_code = 'green'
        return format_html(
                    '<span style="color: {};">{}</span>',
                    color_code,
                    ret, 
                )


    @admin.display(ordering="competitionrelation",description='竞品关系点')
    def colored_competitionrelation(self,obj):
        if not obj.competitionrelation:
            ret = '--'
            color_code = 'black'
        else:
            if obj.competitionrelation.competitionrelation=='组长' or obj.competitionrelation.competitionrelation=='无':
                color_code='red'          
                ret=  obj.competitionrelation.competitionrelation
            else:
                color_code='black'   
                ret=  obj.competitionrelation.competitionrelation    
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,
                ret, )




@admin.register(Project)
class ProjectAdmin(GlobalAdmin):
    exclude = ('id','createtime','updatetime','is_active')
    search_fields=['project']
    list_display = ('project','company')
    #只显示未被假删除的项目
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request).filter(is_active=True)
    #     if request.user.is_superuser:
    #         return qs   
        
    # 外键company只显示active的   定死普美瑞
    # def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
    #     context['adminform'].form.fields['company'].queryset = Company.objects.filter(is_active=True, id=1)
    #     return super(ProjectAdmin, self).render_change_form(request, context, add, change, form_url, obj)
    
    #使得pmrresearchlist中的的autocompletefield被下面的代码过滤，过滤PMR的project
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            print('我在ProjectAdmin-get_search_results-autocomplete')
            queryset=queryset.filter(is_active=True,company_id=2)
        return queryset,use_distinct 


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
    
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request).filter(is_active=True)
    #     if request.user.is_superuser:
    #         return qs           

    # def delete_queryset(self,request, queryset):
    #     # print('CompanyAdmin-delete_queryset',queryset)
    #     for i in queryset:
    #         i.project_set.all().update(is_active=False)
    #     queryset.update(is_active=False)

@admin.register(Brand)  
class BrandAdmin(GlobalAdmin):   
    search_fields=['brand']
    exclude = ('id','createtime','updatetime','is_active')
    
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            queryset=queryset.filter(is_active=True).order_by('id')
        return queryset,use_distinct 
    

@admin.register(ProjectDetail3)  
class ProjectDetailAdmin(GlobalAdmin):   
    search_fields=['detailedproject']
    exclude = ('id','createtime','updatetime','is_active')

    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            queryset=queryset.filter(is_active=True,company_id=2).order_by('id')
        return queryset,use_distinct 
    
   

@admin.register(CompetitionRelation)  
class CompetitionRelationAdmin(GlobalAdmin):   
    search_fields=['competitionrelation']
    exclude = ('id','createtime','updatetime','is_active')


@admin.register(SalesTarget3)  
class SalesTargetAdmin(GlobalAdmin):   
    # resource_class = SalesTargetResource

    exclude = ('id','createtime','updatetime','is_active')






@admin.register(PMRResearchList3Delete)
class PMRResearchList3DeleteAdmin(admin.ModelAdmin):
    # form=PMRResearchListForm
    # inlines=[SalesTargetInline,PMRResearchDetailInline,DetailCalculateInline]
    empty_value_display = '--'
    # list_display_links =('hospital',)
    exclude = ('operator','is_active','olddata')
    readonly_fields=('company','hospital','project','salesman1','salesman2','testspermonth','contactname','contactmobile','salesmode','saleschannel','support','adminmemo')
    search_fields=['uniquestring']
    QT_view_group_list = ['boss','pmrmanager','QTmanager','allviewonly']

    def get_queryset(self, request):
        qs = super(PMRResearchList3DeleteAdmin,self).get_queryset(request)
  
        if request.user.is_superuser :
            print('我在PMRResearchListAdmin-get_queryset-筛选active的')        
            return qs.filter(is_active=False,company_id=2)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.QT_view_group_list:
                return qs.filter(is_active=False,company_id=2)      

       #普通销售的话:
        return qs.filter((Q(is_active=False)&Q(salesman1=request.user)&Q(company_id=2)))#|(Q(is_active=False)&Q(salesman2=request.user)&Q(company_id=2)))
    

    def has_delete_permission(self, request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request):
        return False

    def get_actions(self, request):
        actions = super(PMRResearchList3DeleteAdmin, self).get_actions(request)

        #配置恢复权限
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] == 'pmronlyview' or request.user.groups.values()[0]['name'] =='JC' or request.user.groups.values()[0]['name'] == 'allviewonly':
                del actions['restore']      
            else:  
                return actions
        return actions
    

    #新增动作————恢复按钮
    
    actions = ['restore']
    def restore(self, request, queryset):
        print(queryset)
        print('我在restore')      
        for i in queryset:
            print(i.pmrresearchdetail3delete_set.all())
            i.pmrresearchdetail3delete_set.all().update(is_active=True)
            i.salestarget3delete_set.all().update(is_active=True)
            i.detailcalculate3delete.is_active=True

            i.detailcalculate3delete.save()  
            i.operator=request.user
            print('恢复') 
            i.save()           
        queryset.update(is_active=True)
        print('queryset已update')

    restore.short_description = "恢复数据至调研列表" 
    restore.type = 'info'
    restore.style = 'color:white;'
