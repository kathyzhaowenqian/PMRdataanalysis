from django.contrib import admin

# Register your models here.
from django.contrib import admin
from Marketing_Research_ZS.models import *
from Marketing_Research_ZS.models_delete import *

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
from Marketing_Research_ZS.tools.calculate_Quater_target import result_of_Quatar_display,calculate_quarter_start_end_day
from django.db.models import Avg,Sum,Count,Max,Min

from django.contrib.admin import SimpleListFilter
from django.db.models import Case, When, Value, IntegerField


class ProjectFilter(SimpleListFilter):
    title = '项目' 
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        projects = Project.objects.filter(company_id=5)
        return [(project.id, project.project) for project in projects]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(project__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset


        

class IfTargetCustomerFilter(SimpleListFilter):
    title = '是否填写目标'
    parameter_name = 'iftarget'

    def lookups(self, request, model_admin):
        return [(1, '已填目标额/任何季度'), (2, '未填目标额')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':

            return queryset.filter((Q(gsmrsalestarget__q1target__gt= 0)|Q(gsmrsalestarget__q2target__gt =0)|Q(gsmrsalestarget__q3target__gt =0)|Q(gsmrsalestarget__q4target__gt=0)) & Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') )
 
        elif self.value() == '2':
            return queryset.filter(Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') & Q(gsmrsalestarget__q1target = 0)& Q(gsmrsalestarget__q2target =0) & Q(gsmrsalestarget__q3target =0)& Q(gsmrsalestarget__q4target=0))

'''class CustomerProjectTypeFilter(SimpleListFilter):
    title = '医院项目分类'
    parameter_name = 'customerprojecttype'

    def lookups(self, request, model_admin):
        return [(1, '老项目(22年已开票)'),(2, '丢失的项目(22年已开票、23年至今未开票)'), (3, 'Q1新项目(22年未开票、23Q1已开票)'), (4, 'Q2新项目(22-23Q1未开票、23Q2已开票)'),(5, 'Q3新项目(22-23Q2未开票、23Q3已开票)'),(6, 'Q4新项目(22-23Q3未开票、23Q4已开票)'),(7, '潜在项目(至今未曾开票)'),(8, '潜在项目和今年新项目(22年未开票)')]


    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':#老客户(去年已开票)
            return queryset.filter(Q(gsmrdetailcalculate__totalsumpermonth__gt = 0))
 
        elif self.value() == '2':#丢失的老客户(22年已开票、23年至今未开票)
            return queryset.filter(Q(gsmrdetailcalculate__totalsumpermonth__gt = 0) &  Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') & Q(gsmrsalestarget__q1actualsales= 0) & Q(gsmrsalestarget__q2actualsales= 0) & Q(gsmrsalestarget__q3actualsales= 0) & Q(gsmrsalestarget__q4actualsales= 0)) 

        elif self.value() == '3': #Q1新客户(22年未开票、23Q1已开票)
            return queryset.filter(Q(gsmrdetailcalculate__totalsumpermonth = 0) & ( Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') &  Q(gsmrsalestarget__q1actualsales__gt= 0)) )
        
        elif self.value() == '4': #Q2新客户(22-23Q1未开票、23Q2已开票
            return queryset.filter(Q(gsmrdetailcalculate__totalsumpermonth = 0) & ( Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') &  Q(gsmrsalestarget__q1actualsales= 0) &  Q(gsmrsalestarget__q2actualsales__gt= 0)) )
        
        elif self.value() == '5': #Q3新客户(22-23Q2未开票、23Q3已开票)'
            return queryset.filter(Q(gsmrdetailcalculate__totalsumpermonth = 0) & ( Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') &  Q(gsmrsalestarget__q1actualsales= 0) &  Q(gsmrsalestarget__q2actualsales= 0) & Q(gsmrsalestarget__q3actualsales__gt= 0)) )
        
        elif self.value() == '6': #Q4新客户(22-23Q3未开票、23Q4已开票)
            return queryset.filter(Q(gsmrdetailcalculate__totalsumpermonth = 0) & ( Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') &  Q(gsmrsalestarget__q1actualsales= 0) &  Q(gsmrsalestarget__q2actualsales= 0) &  Q(gsmrsalestarget__q3actualsales= 0) & Q(gsmrsalestarget__q4actualsales__gt= 0)) )
        
        elif self.value() == '7': #潜在客户  
            return queryset.filter(Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') & Q(gsmrsalestarget__q1actualsales = 0)& Q(gsmrsalestarget__q2actualsales =0) & Q(gsmrsalestarget__q3actualsales =0)& Q(gsmrsalestarget__q4actualsales=0) & Q(gsmrdetailcalculate__totalsumpermonth = 0) )
        elif self.value() == '8': #潜在客户 + 今年新客户， 22年未开票客户 
            return queryset.filter(Q(gsmrdetailcalculate__totalsumpermonth = 0))
'''



'''class IfActualSalesFilter(SimpleListFilter):
    title = '23年是否开票'
    parameter_name = 'ifactualsales'

    def lookups(self, request, model_admin):
        return [(1, '23年已开票'), (2, '23年未开票')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter((Q(gsmrsalestarget__q1actualsales__gt= 0)|Q(gsmrsalestarget__q2actualsales__gt =0)|Q(gsmrsalestarget__q3actualsales__gt =0)|Q(gsmrsalestarget__q4actualsales__gt=0)) & Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') )
 
        elif self.value() == '2':
            return queryset.filter(Q(gsmrsalestarget__is_active=True) & Q(gsmrsalestarget__year='2023') & Q(gsmrsalestarget__q1actualsales = 0)& Q(gsmrsalestarget__q2actualsales =0) & Q(gsmrsalestarget__q3actualsales =0)& Q(gsmrsalestarget__q4actualsales=0))
'''


# class IfSalesChannelFilter(SimpleListFilter):
#     title = '销售路径'
#     parameter_name = 'ifsaleschannel'

#     def lookups(self, request, model_admin):
#         return [(1, '已填写销售路径'), (2, '未填写销售路径')]

#     def queryset(self, request, queryset):
#         # pdb.set_trace()
#         if self.value() == '1':
#             return queryset.filter(Q(saleschannel__isnull=False) & ~Q(saleschannel=''))
 
#         elif self.value() == '2':
#             return queryset.filter(Q(saleschannel__isnull=True) | Q(saleschannel=''))


class IfSalesSupportChannelProgressFilter(SimpleListFilter):
    title = '销售路径/所需支持/进展'
    parameter_name = 'ifsalessupportchannelprogress'

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

        salesmans = GSMRUserInfo.objects.filter(Q(username__in= ['lxg','ddl','zw','cjl','szw','lzr']))
        print([(salesman.id, salesman.chinesename) for salesman in salesmans])
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

        salesmans = GSMRUserInfo.objects.filter(Q(username__in= ['lxg','ddl','zw','cjl','szw','lzr']))
        print([(salesman.id, salesman.chinesename) for salesman in salesmans])
        return [(salesman.id, salesman.chinesename) for salesman in salesmans]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(salesman2__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset
        
'''class SalesmanFilterforDetail(SimpleListFilter):
    title = '负责人' 
    parameter_name = 'userinfo'

    def lookups(self, request, model_admin):

        salesmans = GSMRUserInfo.objects.filter(Q(username__in= ['lxg']))
        return [(salesman.id, salesman.chinesename) for salesman in salesmans]
    
    def queryset(self, request, queryset):
        if self.value():
        # 筛选条件有值时, 查询对应的 node 的文章
            return queryset.filter(researchlist__salesman1__id=self.value())
        else:
        # 筛选条件没有值时，全部的时候是没有值的
            return queryset'''


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

###------------------FORM---------------------------------------------------------------------------------------------------------------
# 验证数据手机号
'''def validate(value): # 验证数据
    try:
        v = int(value)
    except:
        raise forms.ValidationError(u'请输入正确手机号')
    if len(value) != 11:
        raise forms.ValidationError(u'请输入正确手机号')
    '''

class GSMRResearchDetailInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print('self.fields',self.fields['ownbusiness'])
        # print(self.fields['brand'].queryset)
        # self.fields['brand'].queryset =  Brand.objects.filter(is_active=True)
        # print(self)
        #在没有autocomplete的前提下，只有在这个form里面修改才能保证过滤isactive

    class Meta: 
            model = GSMRResearchDetail
            exclude = ['id']
            widgets = {
                'endsupplier': forms.TextInput(attrs={'size':'25'}),
                'machinemodel': forms.TextInput(attrs={'size':'10'}),
                # 'testprice': forms.TextInput(attrs={'size':'10'}),
                # 'endsupplier': forms.TextInput(attrs={'size':'36'}),
                # 'detailedprojecttestspermonth': forms.TextInput(attrs={'size':'10'}),

                'machinenumber' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),
                'testprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),
                # 'detailedproject': AutocompleteSelect(
                #     model._meta.get_field('detailedproject'),
                #     admin.site,
                #     attrs={'style': 'width: 10ch'}),
                'brand': AutocompleteSelect(
                    model._meta.get_field('brand'),
                    admin.site,
                    attrs={'style': 'width: 15ch'}),
            }


'''class GSMRResearchListForm(forms.ModelForm):
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
        model = GSMRResearchList
        exclude = ['id']
   '''

###------------------INLINE------------------------------------------------------------------------------------------------------------

class SalesmanPositionInline(admin.TabularInline):
    model = GSMRSalesmanPosition
    fk_name = "user"
    extra = 0
    fields=['user','company','position'] 
    verbose_name = verbose_name_plural = ('员工职位列表')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Company.objects.filter(is_active=True)    
        return super(SalesmanPositionInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    

class GSMRSalesmanPositionInline(admin.TabularInline):
    model = GSMRSalesmanPosition
    fk_name = "company"
    extra = 0
    fields=['user','company','position'] 
    verbose_name = verbose_name_plural = ('员工职位列表')
  
    

class ProjectInline(admin.TabularInline):
    model = Project
    fk_name = "company"
    extra = 0
    fields=['project','company'] 
    verbose_name = verbose_name_plural = ('项目列表')

    def get_queryset(self, request):
        queryset = super().get_queryset(request).filter(is_active=True)        
        return queryset


class GSMRResearchDetailInline(admin.TabularInline):
    form=GSMRResearchDetailInlineForm
    model = GSMRResearchDetail
    fk_name = "researchlist"
    readonly_fields= ('sumpermonth','expiration')
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 
    fields=('brand','endsupplier','type','testspermonth','testprice','sumpermonth','machinemodel','machinenumber','installdate','expiration') 
    # readonly_fields = ('sumpermonth',)
    autocomplete_fields=['brand']
    verbose_name = verbose_name_plural = ('招商调研详情表')
    GSMR_view_group_list = ['boss','GSMRmanager','gsmronlyview','allviewonly']
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.GSMR_view_group_list:
                return qs.filter(is_active=True)
            
       #普通销售的话:
        return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)))




    def has_add_permission(self,request,obj):
        print('我在PMRResearchDetailInline has add permission:::obj',obj,request.user) 
        if obj==None:
            if request.POST.get('salesman1'):                
                if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                    return True
                elif request.POST.get('salesman1')!= str(request.user.id) and  request.POST.get('salesman2')!= str(request.user.id):
                    print('我在PMRResearchDetailInline has add permission:: :obj==None FALSE request.POST.get(salesman1)',request.POST.get('salesman1'),request.user)
                    return False
                else:
                    return True
            else:    
                print('我在PMRResearchDetailInline has add permission:: obj==None True 没有request.POST.get(salesman1)')
                return True

        else:    
            if request.user.is_superuser or obj.salesman1==request.user or obj.salesman2==request.user  or request.POST.get('salesman1')==str(request.user.id) or request.POST.get('salesman2')==str(request.user.id) or request.user.groups.values()[0]['name'] =='boss':
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
        elif obj.salesman1==request.user or obj.salesman2==request.user  or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            print('我在PMRResearchDetailInline has change permission:::obj',True,obj.salesman1)
            return True
        else:
            print('我在PMRResearchDetailInline has change permission:::obj',False)
            return False

    def has_delete_permission(self,request, obj=None):
        print('我在inline has_delete_permission:::obj',obj)        
        return True
    



class SalesTargetInline(admin.StackedInline):
    model = GSMRSalesTarget
    fk_name = "researchlist"
    extra = 0
    readonly_fields = result_of_Quatar_display(settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS,settings.MARKETING_RESEARCH_TARGET_AUTO_DELAYED_DAYS)[1]

    # readonly_fields = ('q1actualsales','q2actualsales','q3actualsales','q4actualsales','q1finishrate','q2finishrate','q3finishrate','q4finishrate')
    # fieldsets =  ('year','q1target','q1completemonth','q2target','q2completemonth','q3target','q3completemonth','q4target','q4completemonth'),       
    fields =  ('year',('q1target','q1completemonth','q1actualsales','field_q1finishrate'),
                      ('q2target','q2completemonth','q2actualsales','field_q2finishrate'),
                      ('q3target','q3completemonth','q3actualsales','field_q3finishrate'),
                      ('q4target','q4completemonth','q4actualsales','field_q4finishrate'),
                                            )                              
    
    verbose_name = verbose_name_plural = ('作战计划和成果 （仅针对新项目）')
    GSMR_view_group_list = ['boss','GSMRmanager','GSMR','gsmronlyview','allviewonly']

    def field_q1finishrate(self, obj):
        value = float(obj.q1finishrate) if obj.q1finishrate else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style,'{:.1%}'.format(value))
    field_q1finishrate.short_description = 'Q1完成率'

    def field_q2finishrate(self, obj):
        value = float(obj.q2finishrate) if obj.q2finishrate else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style,'{:.1%}'.format(value))
    field_q2finishrate.short_description = 'Q2完成率'

    def field_q3finishrate(self, obj):
        value = float(obj.q3finishrate) if obj.q3finishrate else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style,'{:.1%}'.format(value))
    field_q3finishrate.short_description = 'Q3完成率'

    def field_q4finishrate(self, obj):
        value = float(obj.q4finishrate) if obj.q4finishrate else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style,'{:.1%}'.format(value))
    field_q4finishrate.short_description = 'Q4完成率'

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
                if user_in_group_dict['name'] in self.GSMR_view_group_list:
                    return qs.filter(is_active=True,year='2023')
                
            #普通销售的话:
            return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user)&Q(year='2023'))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)&Q(year='2023')))
        
        #如果大于2024.1.1减掉30天
        # if today > calculate_quarter_start_end_day(1,thisyear+1)[0]-timedelta(days=settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS):
        if request.user.is_superuser :
            return qs.filter(is_active=True,year='2024')  
            
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.GSMR_view_group_list:
                return qs.filter(is_active=True,year='2024')

        #普通销售的话:
        return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user)&Q(year='2024'))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)&Q(year='2024')))

    #普通销售不允许删除目标inline
    def has_delete_permission(self,request, obj=None):
        print('我在SalesTargetInline has_delete_permission:::obj',obj)        
        if request.user.is_superuser :
            return True
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.GSMR_view_group_list:
                return True
        else:
            return False



class DetailCalculateInline(admin.StackedInline):
    model = GSMRDetailCalculate
    fk_name = "researchlist"
    extra = 0
    readonly_fields =  ('totalmachinenumber','ownmachinenumber','field_ownmachinepercent','newold','totaltestspermonth','owntestspermonth','field_owntestspercent','ownsalespermonth')                    
    verbose_name = verbose_name_plural = ('数据汇总')
    fields =  ('totalmachinenumber','ownmachinenumber','field_ownmachinepercent','newold','totaltestspermonth','owntestspermonth','field_owntestspercent','ownsalespermonth')
                             
    def field_ownmachinepercent(self, obj):
        value = float(obj.ownmachinepercent) if obj.ownmachinepercent else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style,'{:.1%}'.format(value))
    field_ownmachinepercent.short_description = '国赛仪器数占比'

    def field_owntestspercent(self, obj):
        value = float(obj.owntestspercent) if obj.owntestspercent else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style,'{:.1%}'.format(value))
    field_owntestspercent.short_description = '国赛测试数占比'




###------------------ADMIN-----------------------------------------------------------------------------------------------------------------------------------

@admin.register(GSMRUserInfo)  
class UserGSMRAdmin(UserAdmin):  
        
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
 




@admin.register(GSMRSalesmanPosition)  
class SalesmanPositionAdmin(GlobalAdmin):   
    exclude = ('id','createtime','updatetime')

    # 外键company只显示active的  定死普美瑞
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['adminform'].form.fields['company'].queryset = Company.objects.filter(is_active=True)
        return super(SalesmanPositionAdmin, self).render_change_form(request, context, add, change, form_url, obj)


@admin.register(Company)  
class CompanyAdmin(GlobalAdmin):   
    inlines=[GSMRSalesmanPositionInline,ProjectInline]
    exclude = ('id','createtime','updatetime','is_active')

 


@admin.register(GSMRResearchList)
class GSMRResearchListAdmin(GlobalAdmin):
    # form=GSMRResearchListForm
    inlines=[SalesTargetInline,GSMRResearchDetailInline,DetailCalculateInline]
    empty_value_display = '--'
    list_display_links =('hospital',)
    exclude = ('operator','is_active')
    list_per_page = 10
    list_display = result_of_Quatar_display(settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS,settings.MARKETING_RESEARCH_TARGET_AUTO_DELAYED_DAYS)[0]
 
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
    
  
    
    list_filter = [ProjectFilter,'hospital__district','hospital__hospitalclass',SalesmanFilter,SalesmanFilter2,IfTargetCustomerFilter,'gsmrdetailcalculate__newold',IfSalesSupportChannelProgressFilter]
    search_fields = ['hospital__hospitalname','gsmrresearchdetail__brand__brand','hospital__hospitalclass','hospital__district','project__project','gsmrresearchdetail__machinemodel']
    fieldsets = (('作战背景', {'fields': ('company','hospital','project','salesman1','salesman2',
                                       'director','relation','memo'),
                              'classes': ('wide','extrapretty',),
                              'description': format_html(
                '<span style="color:{};font-size:10.0pt;">{}</span>','red','注意："第一负责人" 只允许填登录用户自己的姓名,不可代填')}),

                 ('作战路径及需求', {'fields': ('saleschannel','support','progress'),
                              'classes': ('wide',)}),                
                )
    GSMR_view_group_list = ['boss','GSMRmanager','gsmronlyview','allviewonly']


    # 新增或修改数据时，设置外键可选值，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company': 
            kwargs["queryset"] = Company.objects.filter(is_active=True,id=5) 
        if db_field.name == 'hospital': 
            kwargs["queryset"] = Hospital.objects.filter(is_active=True) 
        if db_field.name == 'project':  
            kwargs["queryset"] = Project.objects.filter(is_active=True,company_id=5) 
        if db_field.name == 'salesman1': 
            # kwargs['initial'] = #设置默认值
            kwargs["queryset"] = UserInfo.objects.filter(Q(is_active=True) & Q(username__in= ['lxg','ddl','zw','cjl','szw','lzr']))
        if db_field.name == 'salesman2':  
            kwargs["queryset"] = UserInfo.objects.filter(Q(is_active=True) & Q(username__in= ['lxg','ddl','zw','cjl','szw','lzr'])) 

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    
    def has_delete_permission(self, request,obj=None):
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] == 'gsmronlyview' or request.user.groups.values()[0]['name'] == 'allviewonly':
                return False
            
        if obj==None:
            return True
        
        if request.POST.get('salesman1'):
            if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                return True
            if request.POST.get('salesman1')!=str(request.user.id) and request.POST.get('salesman2')!=str(request.user.id):
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
            if request.user.groups.values()[0]['name'] =='gsmronlyview' or request.user.groups.values()[0]['name'] == 'allviewonly':
                return False
        if obj==None:
            print('我在PmrResearchListAdmin has change permission obj==None,True ',request.POST.get('salesman1'))
            return True
        if request.POST.get('salesman1'):
            if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman1)  True superuser!!!')
                return True
            if request.POST.get('salesman1')!=str(request.user.id) and request.POST.get('salesman2')!=str(request.user.id):
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman1)  false!!!',request.POST.get('salesman1'))
                return False
            else: 
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman1)  true!!',request.POST.get('salesman1'))
                return True
        if obj.salesman1==request.user or obj.salesman2==request.user  or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            print('我在PmrResearchListAdmin has change permission True obj.salesman1 ',obj.salesman1)
            return True
        else:
            print('我在PmrResearchListAdmin has change permission else else else',False)
            return False

    # def has_add_permission(self,request):#,obj=None):
        
    #     if request.user.groups.values():
    #         if request.user.groups.values()[0]['name'] =='gsmronlyview' or request.user.groups.values()[0]['name'] == 'allviewonly':
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
        qs = super(GSMRResearchListAdmin, self).get_queryset(request)
        # print('我在PMRResearchListAdmin-get_queryset')

        #要不要在此加入Q1-Q4变动的？？
        self.list_display = result_of_Quatar_display(settings.MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS,settings.MARKETING_RESEARCH_TARGET_AUTO_DELAYED_DAYS)[0]
        # self.list_display = self.list_display + ('detail_qtysum','detail_own_qtysum',)

        if request.user.is_superuser :
            # print('我在PMRResearchListAdmin-get_queryset-筛选active的')            
            return qs.filter(is_active=True,company_id=5)

                
        # <QuerySet [{'name': 'pmrdirectsales'}, {'name': 'QTmanager'}]>
        user_in_group_list = request.user.groups.values('name')
        # print(user_in_group_list)
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.GSMR_view_group_list:
                 # print('我在模型里')
                return qs.filter(is_active=True,company_id=5)
            
       #普通销售的话:
        return qs.filter((Q(is_active=True)&Q(salesman1=request.user)&Q(company_id=5))|(Q(is_active=True)&Q(salesman2=request.user)&Q(company_id=5)))
                      

# ------delete_model内层的红色删除键------------------------------
    def delete_model(self, request, obj):
        print('我在LISTADMIN delete_model')
        if request.user.is_superuser or obj.salesman1==request.user or request.user.groups.values()[0]['name'] =='boss':             
            obj.is_active = False 
            obj.gsmrresearchdetail_set.all().update(is_active=False)
            obj.gsmrsalestarget_set.all().update(is_active=False)
            obj.gsmrdetailcalculate.is_active=False
            obj.gsmrdetailcalculate.save()
            obj.operator=request.user   
            obj.save()

    def delete_queryset(self,request, queryset):        
            print('我在delete_queryset')
            for delete_obj in queryset:     
                print('delete_queryset delete_obj',delete_obj)                    
                if request.user.is_superuser or delete_obj.salesman1==request.user or request.user.groups.values()[0]['name'] =='boss':     
                    delete_obj.is_active=False
                    print('list 已假删')
                    delete_obj.gsmrresearchdetail_set.all().update(is_active=False)
                    delete_obj.gsmrsalestarget_set.all().update(is_active=False)
                    delete_obj.gsmrdetailcalculate.is_active=False
                    print('delete_obj.gsmrdetailcalculate.is_active',delete_obj.gsmrdetailcalculate.is_active)
                    delete_obj.gsmrdetailcalculate.save()
                    delete_obj.operator=request.user
                    delete_obj.save()


    def save_model(self, request, obj, form, change):
        obj.operator = request.user
        obj.uniquestring = '公司:{}, 医院:{}, 项目:{}, 第一负责人:{}'.format(obj.company,obj.hospital,obj.project,obj.salesman1)
        super().save_model(request, obj, form, change)



    def save_related(self, request, form, formsets, change): 
        ###注意要判断是否共用仪器！！！！！！！如果我司仪器必填序列号，怎么validate？？？！？
        print('我在save_related')
        super().save_related(request, form, formsets, change)
        if form.cleaned_data.get('salesman1')==request.user or form.cleaned_data.get('salesman2')==request.user or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss': 
            machine_total_number=0
            machine_own_number=0
            new_or_old_list=[]
            brandscombine=[]
            testspermonthcombine=[]
            totaltests=0
            owntests=0
            salespermonth=0
            ownsalespermonth=0
            if len(formsets[1].cleaned_data) > 0:
                #formsets[1]是仪器详情表，显示inline的行数，删除的行也计算在内
                # print(len(formsets[1].cleaned_data))
                for each_inline in formsets[1].cleaned_data:
                    #循环列表中每一个字典，一个字典就是一行具体的数据
                        #是否我司业务不为空 且  没有被删除  且 仪器数量不为0         
                    print('each_inline',each_inline)  
                    # print(type(each_inline.get('id')))     
                    if  each_inline.get('DELETE')==False and each_inline.get('machinenumber')!=0:
                        machine_total_number += each_inline['machinenumber']  
                        # print('each_inline[brand]',each_inline['brand'])
                        brandscombine.append(each_inline['brand'].brand)
                        testspermonthcombine.append(each_inline['testspermonth'])
                        totaltests += each_inline['testspermonth'] 
                        salespermonth+=each_inline['testspermonth'] * each_inline['testprice']
                        new_or_old_list.append({'brand':each_inline['brand'].brand,'supplier':each_inline['endsupplier']})

                        if each_inline['brand'].brand=="国赛" :#and ("普美瑞" not in each_inline['endsupplier']  or  "普美瑞-"  in each_inline['endsupplier']):
                            machine_own_number += each_inline['machinenumber'] #针对国赛品牌
                            owntests += each_inline['testspermonth']  #针对国赛品牌
                            if each_inline['type']=="国赛美瑞-招商" :
                                ownsalespermonth +=each_inline['testspermonth'] * each_inline['testprice'] #针对国赛美瑞招商业务

            print('我在save_related machine_own_number\machine_total_number',machine_own_number,machine_total_number) 
            if machine_total_number == 0 or machine_own_number ==0:
                ownmachinepercent = 0
            else:
                ownmachinepercent= machine_own_number/machine_total_number

            if totaltests == 0 or owntests ==0:
                owntestspercent = 0
            else:
                owntestspercent= owntests/totaltests

            if salespermonth == 0 or ownsalespermonth ==0:
                ownsalespercent = 0
            else:
                ownsalespercent= ownsalespermonth/salespermonth
            # print('我在new_or_old_listnew_or_old_listnew_or_old_list',new_or_old_list)
            # newolds=''
            # for i in new_or_old_list:
            #     if i['brand']=="国赛":# and ("普美瑞" not in i['supplier']  or  "普美瑞-"  in i['supplier']):
            #         newolds+='已有国赛业务'
            #     else:
            #         newolds+='新商机'
            # print('newold',newolds)
            if any(item.get("brand") == "国赛" for item in new_or_old_list):
                newolds='已有国赛业务'
            else:
                newolds='新商机'
            print('brandscombine',brandscombine)
            print('testspermonthcombine',testspermonthcombine)


            #如果有计算项（老数据修改），则以更新的方式
            if GSMRDetailCalculate.objects.filter(researchlist_id=form.instance.id):
                a=GSMRDetailCalculate.objects.get(researchlist=form.instance)
                # print(a)
                a.totalmachinenumber=machine_total_number
                a.ownmachinenumber=machine_own_number
                a.ownmachinepercent=ownmachinepercent
                a.newold=newolds
                a.brandscombine='|'.join(str(i) for i in brandscombine)
                # print('a.brandscombine',a.brandscombine)
                a.testspermonthcombine='|'.join(str(i) for i in testspermonthcombine)
                # print('a.testspermonthcombine',a.testspermonthcombine)
                a.totaltestspermonth=totaltests
                a.owntestspermonth=owntests
                a.owntestspercent=owntestspercent
                a.salespermonth=salespermonth
                a.ownsalespermonth=ownsalespermonth
                a.ownsalespercent=ownsalespercent
                a.is_active=True
                a.save()
            else:
                print('不能获取对应的detailcalculate')
                GSMRDetailCalculate.objects.create(researchlist=form.instance,totalmachinenumber=machine_total_number,\
                                                   ownmachinenumber=machine_own_number,ownmachinepercent=ownmachinepercent,newold=newolds,\
                                                   brandscombine=brandscombine,testspermonthcombine=testspermonthcombine,\
                                                   totaltestspermonth=totaltests,owntestspermonth=owntests,owntestspercent=owntestspercent,\
                                                   salespermonth=salespermonth,ownsalespermonth=ownsalespermonth,ownsalespercent=ownsalespercent,\
                                                   is_active=True).save()
        
            #把进展整合 然后装进detailcalculate中
            if GSMRResearchList.objects.filter(id=form.instance.id):
                GSMRResearchListobj=GSMRResearchList.objects.get(id=form.instance.id)
                print('GSMRResearchListobj',GSMRResearchListobj)
                if GSMRResearchListobj.progress:
                    progress_history= [{'district':GSMRResearchListobj.hospital.district,
                                        'hospitalname':GSMRResearchListobj.hospital.hospitalname,
                                        'hospitalclass':GSMRResearchListobj.hospital.hospitalclass,
                                        'salesman1':GSMRResearchListobj.salesman1.chinesename,
                                        'salesman2':GSMRResearchListobj.salesman2.chinesename,
                                        'salesman2':GSMRResearchListobj.salesman2.chinesename,
                                        'project':GSMRResearchListobj.project.project,
                                        'progress':GSMRResearchListobj.progress,                                
                                        'time':str(datetime.now())                               
                                    }]
                    GSMRDetailCalculateobj=  GSMRDetailCalculate.objects.get(researchlist=form.instance)
                    print('GSMRDetailCalculateobj',GSMRDetailCalculateobj)
                    if not GSMRDetailCalculateobj.progresshistory:
                        GSMRDetailCalculateobj.progresshistory=progress_history
                    else:
                        GSMRDetailCalculateobj.progresshistory.extend(progress_history)
                    GSMRDetailCalculateobj.save()



            for eachdetail in GSMRResearchDetail.objects.filter(researchlist_id=form.instance.id):
                # print('eachdetail',eachdetail)
                if not eachdetail.installdate:
                    ret = '--'
                else:
                    if (datetime.now().date() - eachdetail.installdate).days >= 1825:
                        ret = '已超5年'
                    else:
                        ret = '5年内'      
                eachdetail.expiration=ret
                eachdetail.sumpermonth=eachdetail.testspermonth * eachdetail.testprice
                eachdetail.save()

            if not GSMRSalesTarget.objects.filter(researchlist_id=form.instance.id):
                GSMRSalesTarget.objects.create(researchlist=form.instance,year='2023',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()
                GSMRSalesTarget.objects.create(researchlist=form.instance,year='2024',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()
            else:
                if len(formsets[0].cleaned_data) > 0:
                    targets2023=GSMRSalesTarget.objects.filter(researchlist_id=form.instance.id,year='2023',is_active=True)
                    if len(targets2023)>1:
                        for i in range(1,len(targets2023)):
                            targets2023[i].delete()                
                    for i in targets2023:
                        i.q1finishrate=i.q1actualsales/i.q1target if i.q1target !=0 else 0.00 
                        i.q2finishrate=i.q2actualsales/i.q2target if i.q2target !=0 else 0.00
                        i.q3finishrate=i.q3actualsales/i.q3target if i.q3target !=0 else 0.00
                        i.q4finishrate=i.q4actualsales/i.q4target if i.q4target !=0 else 0.00                         
                        i.save()

                    targets2024=GSMRSalesTarget.objects.filter(researchlist_id=form.instance.id,year='2024',is_active=True)
                    if len(targets2024)>1:
                        for i in range(1,len(targets2024)):
                            targets2024[i].delete()
                    for i in targets2024:
                        i.q1finishrate=i.q1actualsales/i.q1target if i.q1target !=0 else 0.00 
                        i.q2finishrate=i.q2actualsales/i.q2target if i.q2target !=0 else 0.00
                        i.q3finishrate=i.q3actualsales/i.q3target if i.q3target !=0 else 0.00
                        i.q4finishrate=i.q4actualsales/i.q4target if i.q4target !=0 else 0.00        
                        i.save()


                    if not GSMRSalesTarget.objects.filter(researchlist_id=form.instance.id,year='2023',is_active=True):
                        GSMRSalesTarget.objects.create(researchlist=form.instance,year='2023',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()
             
                    if not GSMRSalesTarget.objects.filter(researchlist_id=form.instance.id,year='2024',is_active=True):
                        GSMRSalesTarget.objects.create(researchlist=form.instance,year='2024',q1target=0,q2target=0,q3target=0,q4target=0,is_active=True).save()

            print('saverelated 保存成功')
   
              







   #这是通过saverelated点击保存时已经存入detailcalculate的数据
    @admin.display(ordering="gsmrdetailcalculate__totaltestspermonth",description='测试总数')
    def detailcalculate_totaltestspermonth(self, obj):
        if obj.gsmrdetailcalculate.totaltestspermonth ==0:
            return  '--'
        else:
            return obj.gsmrdetailcalculate.totaltestspermonth
        
    @admin.display(ordering="gsmrdetailcalculate__brandscombine",description='品牌')    
    def detailcalculate_brandscombine(self, obj):
        return obj.gsmrdetailcalculate.brandscombine
    
    @admin.display(ordering="gsmrdetailcalculate__testspermonthcombine",description='测试数')    
    def detailcalculate_testspermonthcombine(self, obj):
        return obj.gsmrdetailcalculate.testspermonthcombine

    @admin.display(ordering="gsmrdetailcalculate__ownsalespermonth",description='国赛美瑞招商月产出额')    
    def detailcalculate_ownsalespermonth(self, obj):
        return obj.gsmrdetailcalculate.ownsalespermonth
    
    @admin.display(ordering="gsmrdetailcalculate__totalmachinenumber",description='仪器总数')
    def detailcalculate_totalmachinenumber(self, obj):
        if obj.gsmrdetailcalculate.totalmachinenumber ==0:
            return  '--'
        else:
            return obj.gsmrdetailcalculate.totalmachinenumber
    
    @admin.display(ordering="gsmrdetailcalculate__ownmachinepercent",description='我司仪器占比')
    def detailcalculate_ownmachinenumberpercent(self, obj):
        if obj.gsmrdetailcalculate.ownmachinepercent ==0:
            return '--'
        else:
            return '{:.1f}%'.format(obj.gsmrdetailcalculate.ownmachinepercent*100)
    
    @admin.display(description='业务类型')
    def detailcalculate_newold(self, obj):
        return obj.gsmrdetailcalculate.newold

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
        if obj.project.project=='全血蛋白':
            color_code='red'  

        elif obj.project.project=='小发光':
            color_code='orange'    

        elif obj.project.project=='尿蛋白':
            color_code='green'   

        elif obj.project.project=='糖化':
            color_code='purple'
        elif obj.project.project=='血清蛋白':
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
        if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_23_q1.admin_order_field = '-gsmrsalestarget__q1target'

    @admin.display(description='23/Q2目标')
    def salestarget_23_q2(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_23_q2.admin_order_field = '-gsmrsalestarget__q2target'
   
    @admin.display(description='23/Q3目标')
    def salestarget_23_q3(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_23_q3.admin_order_field = '-gsmrsalestarget__q3target'

    @admin.display(description='23/Q4目标')
    def salestarget_23_q4(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)    
    salestarget_23_q4.admin_order_field = '-gsmrsalestarget__q4target'
    

    @admin.display(description='24/Q1目标')
    def salestarget_24_q1(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_24_q1.admin_order_field = '-gsmrsalestarget__q1target'
    


    @admin.display(description='24/Q2目标')
    def salestarget_24_q2(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_24_q2.admin_order_field = '-gsmrsalestarget__q2target'
        
    @admin.display(description='24/Q3目标')
    def salestarget_24_q3(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_24_q3.admin_order_field = '-gsmrsalestarget__q3target'
    
    @admin.display(description='24/Q4目标')
    def salestarget_24_q4(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_24_q4.admin_order_field = '-gsmrsalestarget__q4target'


#目标完成月
    @admin.display(description='23/Q1目标月')
    def completemonth_23_q1(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1completemonth
    completemonth_23_q1.admin_order_field = 'gsmrsalestarget__q1completemonth'

    @admin.display(description='23/Q2目标月')
    def completemonth_23_q2(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2completemonth
    completemonth_23_q2.admin_order_field = 'gsmrsalestarget__q2completemonth'
    
    @admin.display(description='23/Q3目标月')
    def completemonth_23_q3(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3completemonth
    completemonth_23_q3.admin_order_field = 'gsmrsalestarget__q3completemonth'

    @admin.display(description='23/Q4目标月')
    def completemonth_23_q4(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4completemonth
    completemonth_23_q4.admin_order_field = 'gsmrsalestarget__q4completemonth'
    
    @admin.display(description='24/Q1目标月')
    def completemonth_24_q1(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1completemonth
    completemonth_24_q1.admin_order_field = 'gsmrsalestarget__q1completemonth'

    @admin.display(description='24/Q2目标月')
    def completemonth_24_q2(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2completemonth
    completemonth_24_q2.admin_order_field = 'gsmrsalestarget__q2completemonth'
    
    @admin.display(description='24/Q3目标月')
    def completemonth_24_q3(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3completemonth
    completemonth_24_q3.admin_order_field = 'gsmrsalestarget__q3completemonth'

    @admin.display(description='24/Q4目标月')
    def completemonth_24_q4(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4completemonth
    completemonth_24_q4.admin_order_field = 'gsmrsalestarget__q4completemonth'


#每季度实际完成额
    @admin.display(description='23/Q1实际')
    def actualsales_23_q1(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1actualsales
    actualsales_23_q1.admin_order_field = '-gsmrsalestarget__q1actualsales'

    @admin.display(description='23/Q2实际')
    def actualsales_23_q2(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2actualsales
    actualsales_23_q2.admin_order_field = '-gsmrsalestarget__q2actualsales'
    
    @admin.display(description='23/Q3实际')
    def actualsales_23_q3(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3actualsales
    actualsales_23_q3.admin_order_field = '-gsmrsalestarget__q3actualsales'

    @admin.display(description='23/Q4实际')
    def actualsales_23_q4(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4actualsales
    actualsales_23_q4.admin_order_field = '-gsmrsalestarget__q4actualsales'
    
    @admin.display(description='24/Q1实际')
    def actualsales_24_q1(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1actualsales
    actualsales_24_q1.admin_order_field = '-gsmrsalestarget__q1actualsales'

    @admin.display(description='24/Q2实际')
    def actualsales_24_q2(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2actualsales
    actualsales_24_q2.admin_order_field = '-gsmrsalestarget__q2actualsales'

    @admin.display(description='24/Q3实际')
    def actualsales_24_q3(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3actualsales
    actualsales_24_q3.admin_order_field = '-gsmrsalestarget__q3actualsales'

    @admin.display(description='24/Q4实际')
    def actualsales_24_q4(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4actualsales
    actualsales_24_q4.admin_order_field = '-gsmrsalestarget__q4actualsales'


#每季度实际完成率
    @admin.display(description='23/Q1完成率')
    def finishrate_23_q1(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1target and obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1target != 0: #如果target不是0
            finishrate=obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1actualsales/obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1target
            obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q1finishrate=finishrate
                return '--'
    finishrate_23_q1.admin_order_field = '-gsmrsalestarget__q1finishrate'

    @admin.display(description='23/Q2完成率')
    def finishrate_23_q2(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2target and obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2actualsales/obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2target
            obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2finishrate=finishrate
                return '--%'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q2finishrate=finishrate
                return '--'
    finishrate_23_q2.admin_order_field = '-gsmrsalestarget__q2finishrate'

    @admin.display(description='23/Q3完成率')
    def finishrate_23_q3(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3target and obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3actualsales/obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3target
            obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q3finishrate=finishrate
                return '--'
    finishrate_23_q3.admin_order_field = '-gsmrsalestarget__q3finishrate'

    @admin.display(description='23/Q4完成率')
    def finishrate_23_q4(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4target and obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4actualsales/obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4target
            obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2023',is_active=True)[0].q4finishrate=finishrate
                return '--'
    finishrate_23_q4.admin_order_field = '-gsmrsalestarget__q4finishrate'
 
    
    @admin.display(description='24/Q1完成率')
    def finishrate_24_q1(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1target and obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1actualsales/obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1target
            obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q1finishrate=finishrate
                return '--'
    finishrate_24_q1.admin_order_field = '-gsmrsalestarget__q1finishrate'

    @admin.display(description='24/Q2完成率')
    def finishrate_24_q2(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2target and obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2actualsales/obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2target
            obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)
        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q2finishrate=finishrate
                return '--'
    finishrate_24_q2.admin_order_field = '-gsmrsalestarget__q2finishrate'
    
    @admin.display(description='24/Q3完成率')
    def finishrate_24_q3(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3target and obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3actualsales/obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3target
            obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)
        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q3finishrate=finishrate
                return '--'
    finishrate_24_q3.admin_order_field = '-gsmrsalestarget__q3finishrate'
    
    @admin.display(description='24/Q4完成率')
    def finishrate_24_q4(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4target and obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4actualsales/obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4target
            obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)
        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2024',is_active=True)[0].q4finishrate=finishrate
                return '--'
    finishrate_24_q4.admin_order_field = '-gsmrsalestarget__q4finishrate'




#############



    @admin.display(description='25/Q1目标')
    def salestarget_25_q1(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_25_q1.admin_order_field = '-gsmrsalestarget__q1target'
    


    @admin.display(description='25/Q2目标')
    def salestarget_25_q2(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_25_q2.admin_order_field = '-gsmrsalestarget__q2target'
        
    @admin.display(description='25/Q3目标')
    def salestarget_25_q3(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_25_q3.admin_order_field = '-gsmrsalestarget__q3target'
    
    @admin.display(description='25/Q4目标')
    def salestarget_25_q4(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4target == 0:
            color_code='black'
            ret='--'
        else:
            color_code='green'
            ret=obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4target
        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,ret)
    salestarget_25_q4.admin_order_field = '-gsmrsalestarget__q4target'

    @admin.display(description='25/Q1目标月')
    def completemonth_25_q1(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1completemonth
    completemonth_25_q1.admin_order_field = 'gsmrsalestarget__q1completemonth'

    @admin.display(description='25/Q2目标月')
    def completemonth_25_q2(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2completemonth
    completemonth_25_q2.admin_order_field = 'gsmrsalestarget__q2completemonth'
    
    @admin.display(description='25/Q3目标月')
    def completemonth_25_q3(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3completemonth
    completemonth_25_q3.admin_order_field = 'gsmrsalestarget__q3completemonth'

    @admin.display(description='25/Q4目标月')
    def completemonth_25_q4(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4completemonth
    completemonth_25_q4.admin_order_field = 'gsmrsalestarget__q4completemonth'


    @admin.display(description='25/Q1实际')
    def actualsales_25_q1(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1actualsales
    actualsales_25_q1.admin_order_field = '-gsmrsalestarget__q1actualsales'

    @admin.display(description='25/Q2实际')
    def actualsales_25_q2(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2actualsales
    actualsales_25_q2.admin_order_field = '-gsmrsalestarget__q2actualsales'

    @admin.display(description='25/Q3实际')
    def actualsales_25_q3(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3actualsales
    actualsales_25_q3.admin_order_field = '-gsmrsalestarget__q3actualsales'

    @admin.display(description='25/Q4实际')
    def actualsales_25_q4(self, obj):
        return obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4actualsales
    actualsales_25_q4.admin_order_field = '-gsmrsalestarget__q4actualsales'


    @admin.display(description='25/Q1完成率')
    def finishrate_25_q1(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1target and obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1actualsales/obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1target
            obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)

        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q1finishrate=finishrate
                return '--'
    finishrate_25_q1.admin_order_field = '-gsmrsalestarget__q1finishrate'

    @admin.display(description='25/Q2完成率')
    def finishrate_25_q2(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2target and obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2actualsales/obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2target
            obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)
        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q2finishrate=finishrate
                return '--'
    finishrate_25_q2.admin_order_field = '-gsmrsalestarget__q2finishrate'
    
    @admin.display(description='25/Q3完成率')
    def finishrate_25_q3(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3target and obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3actualsales/obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3target
            obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)
        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q3finishrate=finishrate
                return '--'
    finishrate_25_q3.admin_order_field = '-gsmrsalestarget__q3finishrate'
    
    @admin.display(description='25/Q4完成率')
    def finishrate_25_q4(self, obj):
        if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4target and obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4target != 0:
            finishrate=obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4actualsales/obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4target
            obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4finishrate=finishrate
            return '{:.1f}%'.format(finishrate*100)
        else: #如果target是0 但actual不是0
            if obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4actualsales !=0:  
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4finishrate=finishrate
                return '--'
            else: #如果target是0 actual是0
                finishrate=0
                obj.gsmrsalestarget_set.filter(year='2025',is_active=True)[0].q4finishrate=finishrate
                return '--'
    finishrate_25_q4.admin_order_field = '-gsmrsalestarget__q4finishrate'


############


    #通过display计算的仪器值，不做任何保存！！！
    @admin.display(description='test仪器总数')
    def detail_qtysum(self, obj):        
        qty= obj.gsmrresearchdetail_set.filter(is_active=True).aggregate(sumsum=Sum("machinenumber"))   
        # print('qty',qty)
        totalseries_qty= obj.gsmrresearchdetail_set.filter(is_active=True,machineseries__isnull=False).aggregate(countseries=Count("machineseries"))  
        # print('totalseries_qty[countseries]',totalseries_qty['countseries'])
        distinctseries_qty=obj.gsmrresearchdetail_set.filter(is_active=True,machineseries__isnull=False).values('machineseries').distinct().count()
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
        qtyown= obj.gsmrresearchdetail_set.filter(Q(is_active=True) & Q(ownbusiness=True)).aggregate(sumsum=Sum("machinenumber"))
        # print('qtyown',qtyown)
        totalseries_own_qty= obj.gsmrresearchdetail_set.filter(is_active=True,machineseries__isnull=False,ownbusiness=True).aggregate(countseries=Count("machineseries"))  
        # print('totalseries_own_qty',totalseries_own_qty)
        distinctseries_own_qty=obj.gsmrresearchdetail_set.filter(is_active=True,machineseries__isnull=False,ownbusiness=True).values('machineseries').distinct().count()
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
        detailedprojects= obj.gsmrresearchdetail_set.filter(is_active=True)
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
        ownbusinesses= obj.gsmrresearchdetail_set.filter(is_active=True)
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
        machinemodels= obj.gsmrresearchdetail_set.filter(is_active=True)
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
        machineserieses= obj.gsmrresearchdetail_set.filter(is_active=True)
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
        competitors= obj.gsmrresearchdetail_set.filter(is_active=True)
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
        brands= obj.gsmrresearchdetail_set.filter(is_active=True)
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
        installdates= obj.gsmrresearchdetail_set.filter(is_active=True)
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
            if i.gsmrresearchdetail_set.filter(Q(is_active=True)& Q(brand=9) & ~Q(machinenumber='0')) :
                print('calculate已有国赛业务')
                i.gsmrdetailcalculate.newold='已有国赛业务'
            else:
                i.gsmrdetailcalculate.newold='新商机'
                print('calculate新商机')
            
            #更新仪器总数量
            machinetotalqty= i.gsmrresearchdetail_set.filter(is_active=True).aggregate(sumsum=Sum("machinenumber"))['sumsum']  
            if not machinetotalqty:
                machinetotalret=0
            else:
                machinetotalret=machinetotalqty
            i.gsmrdetailcalculate.totalmachinenumber=machinetotalret
            # print('machinetotalqty',machinetotalqty)


            #更新我司仪器数    
            machineqtyown= i.gsmrresearchdetail_set.filter(Q(is_active=True) & Q(brand=9)).aggregate(sumsum=Sum("machinenumber"))['sumsum']
            # print('machineqtyown',machineqtyown)
            if not machineqtyown:
                machineownret=0
            else:
                machineownret=machineqtyown
            i.gsmrdetailcalculate.ownmachinenumber=machineownret


            #更新我司仪器占比     
            if not machinetotalqty or machinetotalret==0 or machinetotalret=='--' or machineownret=='--':
                ownmachinepercent=0       
            else:
                ownmachinepercent=machineownret/machinetotalret
            i.gsmrdetailcalculate.ownmachinepercent=ownmachinepercent
            



            #---------------
            #更新测试总数量
            totaltestspermonth= i.gsmrresearchdetail_set.filter(is_active=True).aggregate(sumsum=Sum("testspermonth"))['sumsum']    
            if not totaltestspermonth:
                totaltestspermonthret=0
            else:
                totaltestspermonthret=totaltestspermonth
            i.gsmrdetailcalculate.totaltestspermonth=totaltestspermonthret

            #更新我司测试  
            owntestspermonth= i.gsmrresearchdetail_set.filter(Q(is_active=True) & Q(brand=9)).aggregate(sumsum=Sum("testspermonth"))['sumsum']  
            if not owntestspermonth:
                owntestspermonthret=0
            else:
                owntestspermonthret=owntestspermonth
            i.gsmrdetailcalculate.owntestspermonth=owntestspermonthret

            #更新我司测试占比     
            if not totaltestspermonth or  totaltestspermonthret==0 or owntestspermonthret=='--' or totaltestspermonthret=='--':
                owntestspercent=0       
            else:
                owntestspercent=owntestspermonthret/totaltestspermonthret
            i.gsmrdetailcalculate.owntestspercent=owntestspercent

            #---------------
            #更新sum量
            salespermonth= i.gsmrresearchdetail_set.filter(is_active=True).aggregate(sumsum=Sum("sumpermonth"))['sumsum']    
            if not salespermonth:
                salespermonthret=0
            else:
                salespermonthret=salespermonth
            i.gsmrdetailcalculate.salespermonth=salespermonthret

            #更新我司sum   
            ownsalespermonth= i.gsmrresearchdetail_set.filter(Q(is_active=True) & Q(brand=9) & Q(type='国赛美瑞-招商')).aggregate(sumsum=Sum("sumpermonth"))['sumsum']  
            if not ownsalespermonth:
                ownsalespermonthret=0
            else:
                ownsalespermonthret=ownsalespermonth
            i.gsmrdetailcalculate.ownsalespermonth=ownsalespermonthret

            #更新我司sum占比     
            if not salespermonth or salespermonthret==0:
                ownsalespercent=0       
            else:
                ownsalespercent=ownsalespermonthret/salespermonthret
            i.gsmrdetailcalculate.ownsalespercent=ownsalespercent

            #---------------
            #更新品牌集合在detailcalculate表中brandscombine
            brands= i.gsmrresearchdetail_set.filter(is_active=True)
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
                ret = '|'.join(brandslist)
                
            else:
                if brands[0].machinenumber != 0:
                    if brands[0].brand:
                        ret=str(brands[0].brand.brand)
                    else:
                        ret='None'
                else:
                    ret='--'
            i.gsmrdetailcalculate.brandscombine=ret


            #更新测试数量集合在detailcalculate表中     testspermonthcombine
            tests= i.gsmrresearchdetail_set.filter(is_active=True)
            if not tests:
                ret = '--'
            elif len(tests)>1:
                ret = '|'.join(str(i.testspermonth) for i in tests if i.machinenumber != 0)               
            else:
                if tests[0].machinenumber != 0:
                    ret=str(tests[0].testspermonth)
                else:
                    ret='--'
            i.gsmrdetailcalculate.testspermonthcombine=ret

            #更新装机时间在detail表中
            qs_fk=i.gsmrresearchdetail_set.all()
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
            i.gsmrdetailcalculate.save()    
            i.save()           


    calculate.short_description = "统计" 
    calculate.type = 'info'
    calculate.style = 'color:white;'







@admin.register(GSMRResearchDetail)
class GSMRResearchDetailAdmin(GlobalAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=['researchlist__hospital__hospitalname','brand__brand']
    list_filter = ['researchlist__hospital__district','researchlist__hospital__hospitalclass',SalesmanFilter,SalesmanFilter2,'researchlist__gsmrdetailcalculate__newold','expiration']

    list_display_links =('list_hospitalname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('list_district','list_hospitalname','list_hospitalclass','list_salesman1', 'list_salesman2','list_project',
                  'brand','type','endsupplier','testspermonth','testprice','sumpermonth','machinenumber','machinemodel','installdate','colored_expiration',
                    )
    autocomplete_fields=['researchlist','brand']
    readonly_fields=('is_active','expiration')
    
    ordering = ('-researchlist__hospital__district',
                Case(
                        When(researchlist__hospital__hospitalclass='三级', then=Value(1)),
                        When(researchlist__hospital__hospitalclass='二级', then=Value(2)),
                        When(researchlist__hospital__hospitalclass='一级', then=Value(3)),
                        When(researchlist__hospital__hospitalclass='未定级', then=Value(4)),
                        output_field=IntegerField(),
                    ),
                'researchlist__hospital__hospitalname','researchlist__salesman1','researchlist__project',)
    GSMR_view_group_list = ['boss','GSMRmanager','gsmronlyview','allviewonly']


    def get_actions(self, request):
        actions = super(GSMRResearchDetailAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions



    #只显示未被假删除的项目
    #------get_queryset-----------查询-------------------
    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的服务器"""
        qs = super(GSMRResearchDetailAdmin, self).get_queryset(request)
        print('我在PMRResearchDetailAdmin-get_queryset')
        #通过外键连list中的负责人名称
        if request.user.is_superuser :
            return qs.filter(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__company_id=5))
        
                
        # <QuerySet [{'name': 'pmrdirectsales'}, {'name': 'QTmanager'}]>
        user_in_group_list = request.user.groups.values('name')
        print(user_in_group_list)
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.GSMR_view_group_list:
                 # print('我在模型里')
                return qs.filter(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__company_id=5))            
        
        #detail active ,list active 同时人员是自己
        return qs.filter((Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__salesman1=request.user)&Q(researchlist__company_id=5))|(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__salesman2=request.user)&Q(researchlist__company_id=5)))

        

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


#一下变化，在list的inline中有体现，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'researchlist': 
            kwargs["queryset"] = GSMRResearchList.objects.filter(is_active=True) 
        # if db_field.name == 'detailedproject': 
        #     kwargs["queryset"] = GSMRProjectDetail.objects.filter(is_active=True) 
        # if db_field.name == 'brand':  
        #     kwargs["queryset"] = Brand.objects.filter(is_active=True) 
        # if db_field.name == 'competitionrelation': 
        #     kwargs["queryset"] = CompetitionRelation.objects.filter(is_active=True)
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
    


    @admin.display(ordering="researchlist__salesman1",description='第一负责人')
    def list_salesman1(self, obj): #用relatedname
        return obj.researchlist.salesman1.chinesename
    
    @admin.display(ordering="researchlist__salesman2",description='第二负责人')
    def list_salesman2(self, obj): #用relatedname
        return obj.researchlist.salesman2.chinesename

    @admin.display(ordering="researchlist__project",description='项目')
    def list_project(self,obj):
        if not obj.researchlist.project.project:
            obj.researchlist.project.project = '--'
            color_code = 'black'

        if obj.researchlist.project.project=='全血蛋白':
            color_code='red'  

        elif obj.researchlist.project.project=='小发光':
            color_code='orange'    

        elif obj.researchlist.project.project=='尿蛋白':
            color_code='green'   

        elif obj.researchlist.project.project=='糖化':
            color_code='purple'
        elif obj.researchlist.project.project=='血清蛋白':
            color_code='blue'

        else:
            color_code='black' 


        return format_html(
                '<span style="color:{};">{}</span>',
                color_code,
                obj.researchlist.project.project, )

    @admin.display(ordering="expiration",description='装机时间')
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






@admin.register(Project)
class ProjectAdmin(GlobalAdmin):
    exclude = ('id','createtime','updatetime','is_active')
    search_fields=['project']
    list_display = ('project','company')

    
    #使得pmrresearchlist中的的autocompletefield被下面的代码过滤，过滤PMR的project
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            print('我在ProjectAdmin-get_search_results-autocomplete')
            queryset=queryset.filter(is_active=True,company_id=5)
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
    

@admin.register(Brand)  
class BrandAdmin(GlobalAdmin):   
    search_fields=['brand']
    exclude = ('id','createtime','updatetime','is_active')
    
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            queryset=queryset.filter(is_active=True).order_by('id')
        return queryset,use_distinct 
    

@admin.register(GSMRSalesTarget)  
class SalesTargetAdmin(GlobalAdmin):   
    exclude = ('id','createtime','updatetime','is_active')






@admin.register(GSMRResearchListDelete)
class GSMRResearchListDeleteAdmin(admin.ModelAdmin):

    empty_value_display = '--'
    # list_display_links =('hospital',)
    exclude = ('operator','is_active')
    readonly_fields=('company','hospital','project','salesman1','salesman2','director','saleschannel','support')
    search_fields=['uniquestring']
    GSMR_view_group_list = ['boss','GSMRmanager','gsmronlyview','allviewonly']

    def get_queryset(self, request):
        qs = super(GSMRResearchListDeleteAdmin,self).get_queryset(request)
  
        if request.user.is_superuser :
            print('我在PMRResearchListAdmin-get_queryset-筛选active的')        
            return qs.filter(is_active=False,company_id=5)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.GSMR_view_group_list:
                return qs.filter(is_active=False,company_id=5)      

       #普通销售的话:
        return qs.filter((Q(is_active=False)&Q(salesman1=request.user)&Q(company_id=5))|(Q(is_active=False)&Q(salesman2=request.user)&Q(company_id=5)))
    

    def has_delete_permission(self, request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request):
        return False

    def get_actions(self, request):
        actions = super(GSMRResearchListDeleteAdmin, self).get_actions(request)

        #配置恢复权限
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] == 'gsmronlyview' or request.user.groups.values()[0]['name'] =='JC' or request.user.groups.values()[0]['name'] == 'allviewonly':
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
            # print(i.gsmrresearchdetaildelete_set.all())
            i.gsmrresearchdetaildelete_set.all().update(is_active=True)
            i.gsmrsalestargetdelete_set.all().update(is_active=True)
            i.gsmrdetailcalculatedelete.is_active=True

            i.gsmrdetailcalculatedelete.save()  
            i.operator=request.user
            print('恢复') 
            i.save()           
        queryset.update(is_active=True)
        print('queryset已update')

    restore.short_description = "恢复数据至调研列表" 
    restore.type = 'info'
    restore.style = 'color:white;'
