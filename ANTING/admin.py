from django.contrib import admin
from ANTING.models import *
from ANTING.models_delete import *

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from django.db.models import Q
import nested_admin
from django import forms
from django.utils.html import format_html
from django.forms import ModelForm, Select
from django.forms import widgets
from django.contrib.admin.widgets import AutocompleteSelect
import textwrap
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.widgets import RadioSelect
from django.contrib.admin import SimpleListFilter
from django.core.cache import cache
from datetime import date,timedelta,datetime

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
    
@admin.register(ATUserInfo)  
class ATUserAdmin(UserAdmin):  
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
 
@admin.register(Company)  
class CompanyAdmin(GlobalAdmin):   
    exclude = ('id','createtime','updatetime','is_active')

@admin.register(ATSPDList)
class ATSPDListAdmin(GlobalAdmin):
    exclude = ('id','createtime','updatetime','is_active','operator')
    search_fields=['supplier','brand']
    # list_filter = ['hospital__district','hospital__hospitalclass','jcornot']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 10
    list_display = ('salesman_chinesename','supplier','brand','department','product','machinemodel','listotal_formatted','salestotal_formatted','display_salestotalpercent','purchasetotal_formatted','display_gppercent','relation',
                    )
    ordering = ('id',)
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    # 新增或修改数据时，设置外键可选值，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company': 
            kwargs["queryset"] = Company.objects.filter(is_active=True,id=9) 
        if db_field.name == 'salesman': 
            kwargs["queryset"] = UserInfo.objects.filter(Q(is_active=True) & Q(username__in= ['zxl']))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ------delete_model内层的红色删除键------------------------------
    def delete_model(self, request, obj):
        print('AT delete_model')
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or obj.salesman==request.user:             
            obj.is_active = False 
            obj.operator=request.user   
            obj.save()

    def delete_queryset(self,request, queryset):        
            print('我在delete_queryset')
            for delete_obj in queryset:     
                print('delete_queryset delete_obj',delete_obj)                    
                if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or delete_obj.salesman==request.user:     
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
        if request.user.is_superuser :
            return qs.filter(is_active=True,company_id=9)

        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True,company_id=9)


    @admin.display(ordering="salesman__chinesename",description='责任人')
    def salesman_chinesename(self, obj):
        return obj.salesman.chinesename
    
    @admin.display(ordering="salestotalpercent",description='开票占比')
    def display_salestotalpercent(self, obj):
        if obj.salestotalpercent:
            return '{:.1f}%'.format(obj.salestotalpercent*100)
        else:
            return '--'
        
    @admin.display(ordering="gppercent",description='毛利率')
    def display_gppercent(self, obj):
        if obj.gppercent:
            return '{:.1f}%'.format(obj.gppercent*100)
        else:
            return '--'
        
    @admin.display(ordering="listotal",description='LIS收入')    
    def listotal_formatted(self, obj):
        if obj.listotal:
            return '{:,.0f}'.format(obj.listotal) 
        else:
            return '--'
        
    @admin.display(ordering="salestotal",description='年开票额')    
    def salestotal_formatted(self, obj):
        if obj.salestotal:
            return '{:,.0f}'.format(obj.salestotal) 
        else:
            return '--'    
        
    @admin.display(ordering="purchasetotal",description='年采购额')    
    def purchasetotal_formatted(self, obj):
        if obj.purchasetotal:
            return '{:,.0f}'.format(obj.purchasetotal) 
        else:
            return '--'
        


############################################################################################
#====================================================
#====================================================
#====================================================

#======作战计划！！！！！！！========================

class IfWhyGrowthFilter(SimpleListFilter):
    title = '是否填写增量来源'
    parameter_name = 'ifwhygrowth'

    def lookups(self, request, model_admin):
        return [(1, '已填写增量来源'), (2, '未填写')]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(Q(whygrowth__isnull=False) & ~Q(whygrowth=''))
 
        elif self.value() == '2':
            return queryset.filter(Q(saleschannel__isnull=True) | Q(saleschannel=''))



#----------FORM-------LIST--------
class ATOverallForm(forms.ModelForm):

    class Meta:
        model = ATOverall
        fields = '__all__'
        widgets = {
            'whygrowth': forms.SelectMultiple(attrs={'style': 'width: 20%'}),
        }   
 
#----------FORM---DETAIL ----FORM-----DETAIL
class ATNewProjectDetailInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATNewProjectDetail
            exclude = ['id']
            widgets = {
                'originalsupplier': forms.TextInput(attrs={'size':'10'}),
                'originalbrand': forms.TextInput(attrs={'size':'5'}),
                'code': forms.TextInput(attrs={'size':'10'}),
                'product': forms.TextInput(attrs={'size':'15'}),
                'spec': forms.TextInput(attrs={'size':'7'}),
                'unit': forms.TextInput(attrs={'size':'2'}),
                'whygrowth': forms.TextInput(attrs={'size':'3'}),
                'pplperunit' : forms.NumberInput(attrs={
                    'style': 'width:8ch'
                }),
                'recentsales' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentcost' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentgp' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),  
                'lisfee' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'lispercent' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),    
                'lissettleprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),                  
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'purchaseqty' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'costppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'marketprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'newcostppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'targetppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estimatemonthlyppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estmonthlygpgrowth' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
            }

class ATNegotiationDetailInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print('aaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.fields['productid'].queryset =  ATMenu.objects.filter(is_active=True)

    class Meta: 
            model = ATNegotiationDetail
            exclude = ['id']
            widgets = {
                'productid': AutocompleteSelect(
                    model._meta.get_field('productid'),
                    admin.site,
                    attrs={'style': 'width: 60ch'}),
                'originalsupplier': forms.TextInput(attrs={'size':'10'}),
                'originalbrand': forms.TextInput(attrs={'size':'5'}),
                'code': forms.TextInput(attrs={'size':'10'}),
                'product': forms.TextInput(attrs={'size':'15'}),
                'spec': forms.TextInput(attrs={'size':'7'}),
                'unit': forms.TextInput(attrs={'size':'2'}),
                'whygrowth': forms.TextInput(attrs={'size':'3'}),
                'pplperunit' : forms.NumberInput(attrs={
                    'style': 'width:8ch'
                }),
                # 'recentsales' : forms.NumberInput(attrs={
                #     'style': 'width:10ch'
                # }),
                # 'recentcost' : forms.NumberInput(attrs={
                #     'style': 'width:10ch'
                # }),
                # 'recentgp' : forms.NumberInput(attrs={
                #     'style': 'width:10ch'
                # }),  
                'lisfee' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'lispercent' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),   
                'lissettleprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),   
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),     
                # 'lissettleprice' : forms.NumberInput(attrs={
                #     'style': 'width:7ch'
                # }),                  
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'purchaseqty' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                # 'costppl' : forms.NumberInput(attrs={
                #     'style': 'width:7ch'
                # }),  
                'marketprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'newcostppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'targetppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                # 'estimatemonthlyppl' : forms.NumberInput(attrs={
                #     'style': 'width:7ch'
                # }),  
                'estmonthlygpgrowth' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
            }

   
class ATChangeChannelDetailInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['productid'].queryset =  ATMenu.objects.filter(is_active=True)

    class Meta: 
            model = ATChangeChannelDetail
            exclude = ['id']
            widgets = {
                'productid': AutocompleteSelect(
                    model._meta.get_field('productid'),
                    admin.site,
                    attrs={'style': 'width: 60ch'}),
                'originalsupplier': forms.TextInput(attrs={'size':'10'}),
                'originalbrand': forms.TextInput(attrs={'size':'5'}),
                'newsupplier': forms.TextInput(attrs={'size':'10'}),
                'code': forms.TextInput(attrs={'size':'10'}),
                'product': forms.TextInput(attrs={'size':'15'}),
                'spec': forms.TextInput(attrs={'size':'7'}),
                'unit': forms.TextInput(attrs={'size':'2'}),
                'whygrowth': forms.TextInput(attrs={'size':'3'}),
                'pplperunit' : forms.NumberInput(attrs={
                    'style': 'width:8ch'
                }),
                'recentsales' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentcost' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentgp' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),  
                'lisfee' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'lispercent' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),   
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),     
                'lissettleprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),                  
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'purchaseqty' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'costppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'marketprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'newcostppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'targetppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estimatemonthlyppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estmonthlygpgrowth' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
            }


class ATBeforeChangeBrandDetailInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['productid'].queryset =  ATMenu.objects.filter(is_active=True)

    class Meta: 
            model = ATBeforeChangeBrandDetail
            exclude = ['id']
            widgets = {
                'productid': AutocompleteSelect(
                    model._meta.get_field('productid'),
                    admin.site,
                    attrs={'style': 'width: 60ch'}),
                'originalsupplier': forms.TextInput(attrs={'size':'10'}),
                'originalbrand': forms.TextInput(attrs={'size':'5'}),
                'code': forms.TextInput(attrs={'size':'10'}),
                'product': forms.TextInput(attrs={'size':'15'}),
                'spec': forms.TextInput(attrs={'size':'7'}),
                'unit': forms.TextInput(attrs={'size':'2'}),
                'whygrowth': forms.TextInput(attrs={'size':'2'}),
                'pplperunit' : forms.NumberInput(attrs={
                    'style': 'width:8ch'
                }),
                'recentsales' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentcost' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentgp' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),  
                'lisfee' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'lispercent' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),   
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),     
                'lissettleprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),                  
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'purchaseqty' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'costppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'marketprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'newcostppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'targetppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estimatemonthlyppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estmonthlygpgrowth' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
            }

class ATAfterChangeBrandDetailInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATAfterChangeBrandDetail
            exclude = ['id']
            widgets = {
                'originalsupplier': forms.TextInput(attrs={'size':'10'}),
                'originalbrand': forms.TextInput(attrs={'size':'5'}),
                'code': forms.TextInput(attrs={'size':'10'}),
                'product': forms.TextInput(attrs={'size':'15'}),
                'spec': forms.TextInput(attrs={'size':'7'}),
                'unit': forms.TextInput(attrs={'size':'2'}),
                'whygrowth': forms.TextInput(attrs={'size':'2'}),
                'pplperunit' : forms.NumberInput(attrs={
                    'style': 'width:8ch'
                }),
                'recentsales' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentcost' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentgp' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),  
                'lisfee' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'lispercent' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),    
                'lissettleprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),                  
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'purchaseqty' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'costppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'marketprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'newcostppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'targetppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estimatemonthlyppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estmonthlygpgrowth' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
            }

class ATSetDetailInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATSetDetail
            exclude = ['id']
            widgets = {
                'originalsupplier': forms.TextInput(attrs={'size':'10'}),
                'originalbrand': forms.TextInput(attrs={'size':'5'}),
                'code': forms.TextInput(attrs={'size':'10'}),
                'product': forms.TextInput(attrs={'size':'15'}),
                'spec': forms.TextInput(attrs={'size':'7'}),
                'unit': forms.TextInput(attrs={'size':'2'}),
                'whygrowth': forms.TextInput(attrs={'size':'3'}),
                'pplperunit' : forms.NumberInput(attrs={
                    'style': 'width:8ch'
                }),
                'recentsales' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentcost' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                'recentgp' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),  
                'lisfee' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'lispercent' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),    
                'lissettleprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),                  
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'purchaseqty' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'costppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'marketprice' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'newcostppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'targetppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estimatemonthlyppl' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
                'estmonthlygpgrowth' : forms.NumberInput(attrs={
                    'style': 'width:7ch'
                }),  
            }

#----------FORM----STATUS----FORM----STATUS-

class ATNewProjectStatusInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATNewProjectStatus
            exclude = ['id']
            widgets = {
            
                'monthgpgrowth': forms.TextInput(attrs={'size':'37'}),
                'progress': Select(attrs={'style': 'width: 275px'}),
                'completemonth': Select(attrs={'style': 'width: 275px'}),
                # 'pplperunit' : forms.NumberInput(attrs={
                #     'style': 'width:7ch'
                # }),
            }    
            
class ATNegotiationStatusInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATNegotiationStatus
            exclude = ['id']
            widgets = {
            
                'monthgpgrowth': forms.TextInput(attrs={'size':'37'}),
                'progress': Select(attrs={'style': 'width: 275px'}),
                'completemonth': Select(attrs={'style': 'width: 275px'}),
                # 'pplperunit' : forms.NumberInput(attrs={
                #     'style': 'width:7ch'
                # }),
            }    

class ATChangeChannelStatusInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATChangeChannelStatus
            exclude = ['id']
            widgets = {
            
                'monthgpgrowth': forms.TextInput(attrs={'size':'37'}),
                'progress': Select(attrs={'style': 'width: 275px'}),
                'completemonth': Select(attrs={'style': 'width: 275px'}),
                # 'pplperunit' : forms.NumberInput(attrs={
                #     'style': 'width:7ch'
                # }),
            }    


class ATChangeBrandStatusInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATChangeBrandStatus
            exclude = ['id']
            widgets = {
            
                'monthgpgrowth': forms.TextInput(attrs={'size':'37'}),
                'progress': Select(attrs={'style': 'width: 275px'}),
                'completemonth': Select(attrs={'style': 'width: 275px'}),
                # 'pplperunit' : forms.NumberInput(attrs={
                #     'style': 'width:7ch'
                # }),
            }    
  

class ATSetStatusInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATSetStatus
            exclude = ['id']
            widgets = {
            
                'monthgpgrowth': forms.TextInput(attrs={'size':'37'}),
                'progress': Select(attrs={'style': 'width: 275px'}),
                'completemonth': Select(attrs={'style': 'width: 275px'}),
            }    
            

class ATMenuforinlineInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = ATNewProjectDetail
            exclude = ['id']
            widgets = {
                'supplier': forms.TextInput(attrs={'size':'10'}),
                'brand': forms.TextInput(attrs={'size':'5'}),
                'code': forms.TextInput(attrs={'size':'11'}),
                'product': forms.TextInput(attrs={'size':'17'}),
                'spec': forms.TextInput(attrs={'size':'8'}),
                'unit': forms.TextInput(attrs={'size':'2'}),
                'machinemodel': forms.TextInput(attrs={'size':'8'}),
                'machinebrand': forms.TextInput(attrs={'size':'8'}),
                'priceperunit' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),                  
                'costperunit' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),  
                'purchaseqty' : forms.NumberInput(attrs={
                    'style': 'width:8ch'
                }),  
                'purchasesum' : forms.NumberInput(attrs={
                    'style': 'width:12ch'
                }),  
                'theoreticalvalue' : forms.NumberInput(attrs={
                    'style': 'width:12ch'
                }),  
                'theoreticalgp' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),  
                # 'theoreticalgppercent' : forms.NumberInput(attrs={
                #     'style': 'width:7ch'
                # }),  
              
            }

    
#----INNLINE----INLINE----INLINE----INLINE
#---------------------------------------------------------------
#新开项目明细的内嵌inline
class ATNewProjectDetailInline(nested_admin.NestedTabularInline):
    form=ATNewProjectDetailInlineForm
    model = ATNewProjectDetail
    fk_name = "progressid"
    extra = 0
    readonly_fields= ('field_estmonthlygpgrowth',) #'costfeepercent','marketpricefeepercent', 'newcostfeepercent') #'field_lissettleprice', 'field_recentgp',

    fields=['originalsupplier','originalbrand','code','product','spec',
            'unit','pplperunit','costperunit',
            'lisfee','lissettleprice',#'purchaseqty',   #'field_lissettleprice',  'costppl',        
            'marketprice',#'costfeepercent','marketpricefeepercent', #'gppercent'
            'newcostppl',#'newcostfeepercent', #'newcostdroprate', ,'newgppercent'
            'targetppl','estimatemonthlyppl', #'targetdropdate','realmonthlyppl',
            'field_estmonthlygpgrowth'#'whygrowth'
            ] 
    verbose_name = verbose_name_plural = ('新开项目明细')
    view_group_list = ['boss','AT','allviewonly','JConlyview']

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
    #     return formset

    def field_estmonthlygpgrowth(self, obj):
        value = obj.estmonthlygpgrowth if obj.estmonthlygpgrowth else '--'
        style = 'width: 10ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, value)
    field_estmonthlygpgrowth.short_description = '预估月毛利额增量'

   
    def field_lissettleprice(self, obj):
        value = obj.lissettleprice if obj.lissettleprice else '--'
        style = 'width:10ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, value)
    field_lissettleprice.short_description = 'Lis结算价'


    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)

    def has_add_permission(self,request,obj):
        print('ATNewProjectDetailInline has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATNewProjectDetailInline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('ATNewProjectDetailInline has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATNewProjectDetailInline has change permission:::obj',False)
            return False
        
#新开项目状态的内嵌inline
class ATNewProjectStatusInline(nested_admin.NestedStackedInline):
    form=ATNewProjectStatusInlineForm
    inlines=[ATNewProjectDetailInline]
    model = ATNewProjectStatus
    # fk_name = "overallid"
    extra = 0
    readonly_fields= ('thisyeargpgrowth','field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail') 
    fields=(('progress','completemonth'),
            ('target','reason'),
            ('relation','support'),           
            ('actionplan','memo'),
            ('monthgpgrowth','thisyeargpgrowth'),   
            ('field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail'),
            ('advicedirector','adviceboss'),
            
            ) 

    verbose_name = verbose_name_plural = ('新开项目总表')
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 

    def field_monthgpgrowthbydetail(self, obj):
        value = obj.monthgpgrowthbydetail if obj.monthgpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_monthgpgrowthbydetail.short_description = '根据下方明细计算月毛利额增量(供参考)'

    def field_thisyeargpgrowthbydetail(self, obj):
        value = obj.thisyeargpgrowthbydetail if obj.thisyeargpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_thisyeargpgrowthbydetail.short_description = '根据下方明细计算23年毛利额增量(供参考)'

    #倪日磊只可以填写advicedirector， 老板填写adviceboss ，其他人只能看
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # print('formset.form.base_fields',formset.form.base_fields)
        if request.user.username == 'nrl':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = False
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
        elif request.user.username == 'chm':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = False
        else:
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
            # formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
        return formset
    
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
        # return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)))
    def has_add_permission(self,request,obj):
        print('ATNewProjectStatusInline has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATNewProjectStatusInline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('ATNewProjectStatusInline has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATNewProjectStatusInline has change permission:::obj',False)
            return False

#----------------------------------------------------------------
#供应商重新谈判明细的内嵌inline
class ATNegotiationDetailInline(nested_admin.NestedTabularInline):
    form=ATNegotiationDetailInlineForm
    model = ATNegotiationDetail
    extra = 0
    readonly_fields= ('field_recentsales','field_recentcost','field_recentgp','field_recentgpofsupplier','field_estmonthlygpgrowth')#'field_lissettleprice') 
    autocomplete_fields=['productid']
    fields=[#'originalsupplier','originalbrand','code','product','spec','unit',这些都是后来再存进去
            'productid','pplperunit','field_recentsales','field_recentcost','field_recentgp','field_recentgpofsupplier',#'costperunit',#,这个也是后来再存进去
            'lisfee','lissettleprice',#'lispercent','purchaseqty',         #'field_lissettleprice', 'costppl'    
            'marketprice',#'gppercent','costfeepercent','marketpricefeepercent',
            'newcostppl',#'newcostdroprate','newgppercent','newcostfeepercent',
            'targetppl',#'targetdropdate','realmonthlyppl',
            'field_estmonthlygpgrowth'#, 'whygrowth' #'gpgrowthppl',
            ] 
                      
    verbose_name = verbose_name_plural = ('供应商重新谈判明细')
    view_group_list = ['boss','AT','allviewonly','JConlyview']


    def field_recentsales(self, obj):
        value = int(obj.recentsales) if obj.recentsales else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style,'{:,}'.format(value))
    field_recentsales.short_description = '半年度开票额'

    def field_recentcost(self, obj):
        value = int(obj.recentcost) if obj.recentcost else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentcost.short_description = '半年度采购额'


    def field_estmonthlygpgrowth(self, obj):
        value = int(obj.estmonthlygpgrowth) if obj.estmonthlygpgrowth else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_estmonthlygpgrowth.short_description = '预估月毛利额增量'

    #可以设置field字段的显示方式
    def field_recentgp(self, obj):
        value = int(obj.recentgp) if obj.recentgp else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentgp.short_description = '盈亏'
    
    def field_lissettleprice(self, obj):
        value = obj.lissettleprice if obj.lissettleprice else '--'
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, value)
    field_lissettleprice.short_description = 'Lis结算价'

    def field_recentgpofsupplier(self, obj):
        value = int(obj.recentgpofsupplier) if obj.recentgpofsupplier else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentgpofsupplier.short_description = '供应商盈利'

    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
       
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
        # return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)))
    def has_add_permission(self,request,obj):
        print('ATNegotiationDetailInline has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATNegotiationDetailInline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('ATNegotiationDetailInline has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATNegotiationDetailInline has change permission:::obj',False)
            return False

#供应商重新谈判状态的内嵌inline
class ATNegotiationStatusInline(nested_admin.NestedStackedInline):
    form=ATNegotiationStatusInlineForm
    inlines=[ATNegotiationDetailInline]
    model = ATNegotiationStatus
    fk_name = "overallid"
    extra = 0
    readonly_fields= ('thisyeargpgrowth','field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail') 
    fields=(('progress','completemonth'),
            ('target','reason'),
            ('relation','support'),           
            ('actionplan','memo'),
            ('monthgpgrowth','thisyeargpgrowth'),   
            ('field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail'),
            ('advicedirector','adviceboss'),
            ) 
    verbose_name = verbose_name_plural = ('供应商重新谈判总表')
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 
   

    def field_monthgpgrowthbydetail(self, obj):
        value = obj.monthgpgrowthbydetail if obj.monthgpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_monthgpgrowthbydetail.short_description = '根据下方明细计算月毛利额增量(供参考)'

    def field_thisyeargpgrowthbydetail(self, obj):
        value = obj.thisyeargpgrowthbydetail if obj.thisyeargpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_thisyeargpgrowthbydetail.short_description = '根据下方明细计算23年毛利额增量(供参考)'

    #倪日磊只可以填写advicedirector， 老板填写adviceboss ，其他人只能看
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # print('formset.form.base_fields',formset.form.base_fields)
        if request.user.username == 'nrl':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = False
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
        elif request.user.username == 'chm':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = False
        else:
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
            # formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
        return formset
    
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
        # return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)))

    def has_add_permission(self,request,obj):
        print('ATNegotiationStatusInline has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATNegotiationStatusInline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('ATNegotiationStatusInline has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATNegotiationStatusInline has change permission:::obj',False)
            return False
#----------------------------------------------------------------
#渠道变更明细的内嵌inline
class ATChangeChannelDetailInline(nested_admin.NestedTabularInline):
    form=ATChangeChannelDetailInlineForm
    model = ATChangeChannelDetail
    # fk_name = "progressid"
    extra = 0
    readonly_fields= ('field_recentsales','field_recentcost','field_recentgp','field_recentgpofsupplier','field_estmonthlygpgrowth')#'field_lissettleprice') 
    autocomplete_fields=['productid']
    fields=[#'originalsupplier','originalbrand',,'code','product','spec','unit',
            'productid','newsupplier','pplperunit','field_recentsales','field_recentcost','field_recentgp','field_recentgpofsupplier',
            'lisfee','lissettleprice',#'lispercent',#'purchaseqty',         #'field_lissettleprice', 'costppl'    
            'marketprice',#'gppercent','costfeepercent','marketpricefeepercent',
            'newcostppl',#'newcostdroprate','newgppercent','newcostfeepercent',
            'targetppl',#'targetdropdate','realmonthlyppl',
            'field_estmonthlygpgrowth'#, 'whygrowth' #'gpgrowthppl',
            ] 
                      
    verbose_name = verbose_name_plural = ('渠道变更明细')
    view_group_list = ['boss','AT','allviewonly','JConlyview']

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
    #     return formset

    def field_recentsales(self, obj):
        value = int(obj.recentsales) if obj.recentsales else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentsales.short_description = '半年度开票额'

    def field_recentcost(self, obj):
        value = int(obj.recentcost) if obj.recentcost else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentcost.short_description = '半年度采购额'


    def field_estmonthlygpgrowth(self, obj):
        value = int(obj.estmonthlygpgrowth) if obj.estmonthlygpgrowth else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_estmonthlygpgrowth.short_description = '预估月毛利额增量'

    #可以设置field字段的显示方式
    def field_recentgp(self, obj):
        value = int(obj.recentgp) if obj.recentgp else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentgp.short_description = '盈亏'
    
    def field_lissettleprice(self, obj):
        value = obj.lissettleprice if obj.lissettleprice else '--'
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, value)
    field_lissettleprice.short_description = 'Lis结算价'

    def field_recentgpofsupplier(self, obj):
        value = int(obj.recentgpofsupplier) if obj.recentgpofsupplier else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentgpofsupplier.short_description = '原供应商盈利'

    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)

    def has_add_permission(self,request,obj):
        print('ATChangeChannelDetailInline has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATChangeChannelDetailInline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('ATChangeChannelDetailInline has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATChangeChannelDetailInline has change permission:::obj',False)
            return False

#渠道变更状态的内嵌inline
class ATChangeChannelStatusInline(nested_admin.NestedStackedInline):
    form=ATChangeChannelStatusInlineForm
    inlines=[ATChangeChannelDetailInline]
    model = ATChangeChannelStatus
    # fk_name = "overallid"
    extra = 0
    readonly_fields= ('thisyeargpgrowth','field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail') 
    fields=(('progress','completemonth'),
           ('target','reason'),
            ('relation','support'),           
            ('actionplan','memo'),
            ('monthgpgrowth','thisyeargpgrowth'),   
            ('field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail'),
            ('advicedirector','adviceboss'),
            ) 
    verbose_name = verbose_name_plural = ('渠道变更总表(品牌不变)')
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 

    def field_monthgpgrowthbydetail(self, obj):
        value = obj.monthgpgrowthbydetail if obj.monthgpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_monthgpgrowthbydetail.short_description = '根据下方明细计算月毛利额增量(供参考)'

    def field_thisyeargpgrowthbydetail(self, obj):
        value = obj.thisyeargpgrowthbydetail if obj.thisyeargpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_thisyeargpgrowthbydetail.short_description = '根据下方明细计算23年毛利额增量(供参考)'

    #倪日磊只可以填写advicedirector， 老板填写adviceboss ，其他人只能看
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # print('formset.form.base_fields',formset.form.base_fields)
        if request.user.username == 'nrl':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = False
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
        elif request.user.username == 'chm':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = False
        else:
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
            # formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
        return formset
    
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)

    def has_add_permission(self,request,obj):
        print('ATChangeChannelStatusInline has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATChangeChannelStatusInline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('ATChangeChannelStatusInline has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATChangeChannelStatusInline has change permission:::obj',False)
            return False
#-----------------------------------------------------------------
#品牌替换前明细的内嵌inline
class ATBeforeChangeBrandDetailInline(nested_admin.NestedTabularInline):
    form=ATBeforeChangeBrandDetailInlineForm
    model = ATBeforeChangeBrandDetail
    fk_name = "progressid"
    extra = 0
    readonly_fields= ('field_recentsales','field_recentcost','field_recentgp','field_recentgpofsupplier','field_monthgp','field_realmonthlyppl')

    fields=[#'originalsupplier','originalbrand','code','product','spec',#'beforeorafterbrandchange','unit',
             'productid','pplperunit','field_recentsales','field_recentcost','field_recentgp','field_recentgpofsupplier',
            'lisfee','lissettleprice',#'purchaseqty',   #'lispercent',  'costppl',        
            'marketprice',#'costfeepercent','marketpricefeepercent', #'gppercent'
            #'newcostppl',#'newcostfeepercent', #'newcostdroprate', ,'newgppercent'
            'field_realmonthlyppl',#'targetppl','estimatemonthlyppl', #'targetdropdate',
            'field_monthgp'#,'whygrowth'
            ] 
    

    verbose_name = verbose_name_plural = ('品牌替换之前——原品牌明细表')
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    autocomplete_fields=['productid']


    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
    #     return formset
    
    def field_realmonthlyppl(self, obj):
        value = int(obj.realmonthlyppl) if obj.realmonthlyppl else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_realmonthlyppl.short_description = '每月开票人份数'

    def field_recentsales(self, obj):
        value = int(obj.recentsales) if obj.recentsales else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentsales.short_description = '半年度开票额'

    def field_recentcost(self, obj):
        value = int(obj.recentcost) if obj.recentcost else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentcost.short_description = '半年度采购额'


    def field_monthgp(self, obj):
        value = int(obj.monthgp) if obj.monthgp else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_monthgp.short_description = '月毛利额'

    #可以设置field字段的显示方式
    def field_recentgp(self, obj):
        value = int(obj.recentgp) if obj.recentgp else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentgp.short_description = '盈亏'
    
    def field_lissettleprice(self, obj):
        value = obj.lissettleprice if obj.lissettleprice else '--'
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, value)
    field_lissettleprice.short_description = 'Lis结算价'

    def field_recentgpofsupplier(self, obj):
        value = int(obj.recentgpofsupplier) if obj.recentgpofsupplier else 0
        style = 'width: 6ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_recentgpofsupplier.short_description = '供应商盈利'


    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)

    def has_add_permission(self,request,obj):
        print('ATBeforeChangeBrandDetailInline has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATBeforeChangeBrandDetailInline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('ATBeforeChangeBrandDetailInline has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATBeforeChangeBrandDetailInline has change permission:::obj',False)
            return False



#品牌替换后明细的内嵌inline
class ATAfterChangeBrandDetailInline(nested_admin.NestedTabularInline):
    form=ATAfterChangeBrandDetailInlineForm
    model = ATAfterChangeBrandDetail
    fk_name = "progressid"
    extra = 0
    readonly_fields= ('field_monthgp',) #'costfeepercent','marketpricefeepercent', 'newcostfeepercent') #'field_lissettleprice', 'field_recentgp',

    fields=['originalsupplier','originalbrand','code','product','spec', #'beforeorafterbrandchange',
            'unit','pplperunit','costperunit',
            'lisfee','lissettleprice',#'purchaseqty',   #'field_lissettleprice',  'costppl',        
            'marketprice',#'costfeepercent','marketpricefeepercent', #'gppercent'
            'newcostppl',#'newcostfeepercent', #'newcostdroprate', ,'newgppercent'
            'targetppl','estimatemonthlyppl', #'targetdropdate','realmonthlyppl',
            'field_monthgp'#,'whygrowth'
            ] 
    verbose_name = verbose_name_plural = ('品牌替换之后——新品牌明细表')
    view_group_list = ['boss','AT','allviewonly','JConlyview']

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
    #     return formset

    def field_monthgp(self, obj):
        value = obj.monthgp if obj.monthgp else '--'
        style = 'width: 10ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_monthgp.short_description = '预估月毛利额'

   
    def field_lissettleprice(self, obj):
        value = obj.lissettleprice if obj.lissettleprice else '--'
        style = 'width:10ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, value)
    field_lissettleprice.short_description = 'Lis结算价'


    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    
    def has_add_permission(self,request,obj):
        print('ATAfterChangeBrandDetailInline has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATAfterChangeBrandDetailInline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('ATAfterChangeBrandDetailInline has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('ATAfterChangeBrandDetailInline has change permission:::obj',False)
            return False


#品牌替换状态的内嵌inline
class ATChangeBrandStatusInline(nested_admin.NestedStackedInline):
    form= ATChangeBrandStatusInlineForm
    inlines=[ATBeforeChangeBrandDetailInline,ATAfterChangeBrandDetailInline]
    model =  ATChangeBrandStatus
    extra = 0
    readonly_fields= ('thisyeargpgrowth','field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail') 
    fields=(('progress','completemonth'),
            ('target','reason'),
            ('relation','support'),           
            ('actionplan','memo'),
            ('monthgpgrowth','thisyeargpgrowth'),   
            ('field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail'),
            ('advicedirector','adviceboss'),
            ) 

    verbose_name = verbose_name_plural = ('品牌替换总表(品牌变更、或渠道和品牌均变更)')
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 

    def field_monthgpgrowthbydetail(self, obj):
        value = obj.monthgpgrowthbydetail if obj.monthgpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_monthgpgrowthbydetail.short_description = '根据下方明细计算月毛利额增量(供参考,品牌替换后毛利润和-替换前毛利润和)'

    def field_thisyeargpgrowthbydetail(self, obj):
        value = obj.thisyeargpgrowthbydetail if obj.thisyeargpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_thisyeargpgrowthbydetail.short_description = '根据下方明细计算23年毛利额增量(供参考)'

    #倪日磊只可以填写advicedirector， 老板填写adviceboss ，其他人只能看
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # print('formset.form.base_fields',formset.form.base_fields)
        if request.user.username == 'nrl':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = False
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
        elif request.user.username == 'chm':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = False
        else:
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
            # formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
        return formset
    
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    
#-----------------------------------------------------------------
#套餐绑定明细的内嵌inline
class ATSetDetailInline(nested_admin.NestedTabularInline):
    form=ATSetDetailInlineForm
    model = ATSetDetail
    fk_name = "progressid"
    extra = 0
    readonly_fields= ('field_estmonthlygpgrowth',) #'costfeepercent','marketpricefeepercent', 'newcostfeepercent') #'field_lissettleprice', 'field_recentgp',

    fields=['originalsupplier','originalbrand','code','product','spec',
            'unit','pplperunit','costperunit',
            'lisfee','lissettleprice',#'purchaseqty',   #'field_lissettleprice',  'costppl',        
            'marketprice',#'costfeepercent','marketpricefeepercent', #'gppercent'
            'newcostppl',#'newcostfeepercent', #'newcostdroprate', ,'newgppercent'
            'targetppl','estimatemonthlyppl', #'targetdropdate','realmonthlyppl',
            'field_estmonthlygpgrowth'#,'whygrowth'
            ] 
    verbose_name = verbose_name_plural = ('套餐绑定明细')
    view_group_list = ['boss','AT','allviewonly','JConlyview']

    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
    #     return formset

    def field_estmonthlygpgrowth(self, obj):
        value = obj.estmonthlygpgrowth if obj.estmonthlygpgrowth else '--'
        style = 'width: 10ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_estmonthlygpgrowth.short_description = '预估月毛利额增量'

   
    def field_lissettleprice(self, obj):
        value = obj.lissettleprice if obj.lissettleprice else '--'
        style = 'width:10ch'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, value)
    field_lissettleprice.short_description = 'Lis结算价'


    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)

    def has_add_permission(self,request,obj):
        print('我在setinelin has add permission:::obj',obj,request.user) 
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('我在setinline has add permission:::,obj.salesman1 else',False)
            return False

    def has_change_permission(self,request, obj=None):
        print('我在setinlinee has change permission:: obj',obj)
        if obj==None:
            return True            
        elif  request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss'  or request.user.groups.values()[0]['name'] =='AT':
            return True
        else:
            print('setinline has change permission:::obj',False)
            return False




#套餐绑定状态的内嵌inline
class ATSetStatusInline(nested_admin.NestedStackedInline):
    form=ATSetStatusInlineForm
    inlines=[ATSetDetailInline]
    model = ATSetStatus
    # fk_name = "overallid"
    extra = 0
    readonly_fields= ('thisyeargpgrowth','field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail') 
    fields=(('progress','completemonth'),
            ('target','reason'),
            ('relation','support'),           
            ('actionplan','memo'),
            ('monthgpgrowth','thisyeargpgrowth'),   
            ('field_monthgpgrowthbydetail','field_thisyeargpgrowthbydetail'),
            ('advicedirector','adviceboss'),
            ) 

    verbose_name = verbose_name_plural = ('套餐绑定总表')
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 

    def field_monthgpgrowthbydetail(self, obj):
        value = obj.monthgpgrowthbydetail if obj.monthgpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_monthgpgrowthbydetail.short_description = '根据下方明细计算月毛利额增量(供参考)'

    def field_thisyeargpgrowthbydetail(self, obj):
        value = obj.thisyeargpgrowthbydetail if obj.thisyeargpgrowthbydetail else '--'
        style = 'width:275px'#; background-color: #f2f2f2;'
        return format_html('<div style="{}">{}</div>', style, '{:,}'.format(value))
    field_thisyeargpgrowthbydetail.short_description = '根据下方明细计算23年毛利额增量(供参考)'

    #倪日磊只可以填写advicedirector， 老板填写adviceboss ，其他人只能看
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # print('formset.form.base_fields',formset.form.base_fields)
        if request.user.username == 'nrl':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = False
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
        elif request.user.username == 'chm':
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = False
        else:
            formset.form.base_fields['advicedirector'].widget.attrs['readonly'] = True
            formset.form.base_fields['adviceboss'].widget.attrs['readonly'] = True
            # formset.form.base_fields['whygrowth'].widget.attrs['readonly'] = True
        return formset
    
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
        # return qs.filter((Q(is_active=True)&Q(researchlist__salesman1=request.user))|(Q(is_active=True)&Q(researchlist__salesman2=request.user)))
    
    def has_add_permission(self,request,obj):
        print('我在setinelin has add permission:::obj',obj,request.user) 
        if obj==None:
            if request.POST.get('salesman'):                
                if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                    return True
                elif request.POST.get('salesman')!= str(request.user.id):
                    print('我在P我在setinelin has add permission:: :obj==None FALSE request.POST.get(salesman)',request.POST.get('salesman'),request.user)
                    return False
                else:
                    return True
            else:    
                print('我在setinelin has add permission:: obj==None True 没有request.POST.get(salesman)')
                return True

        else:    
            if request.user.is_superuser or obj.salesman==request.user  or request.POST.get('salesman')==str(request.user.id) or request.user.groups.values()[0]['name'] =='boss':
                print('我在setinline has add permission:::,obj.salesman1 if ',True)
                return True
            else:
                print('我在setinline has add permission:::,obj.salesman1 else',False)
                return False

    def has_change_permission(self,request, obj=None):
        print('我在setinlinee has change permission:: obj',obj)
        if obj==None:
                print('setinline has change permission:::obj,request.POST.get(salesman)',True,request.POST.get('salesman'))
                return True            
        elif obj.salesman==request.user or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            print('setinline has change permission:::obj',True,obj.salesman)
            return True
        else:
            print('setinline has change permission:::obj',False)
            return False
#----------------------------------------------------------------
#作战计划计算表
class ATCalculateInline(nested_admin.NestedStackedInline):
    model = ATCalculate
    # fk_name = "overallid"
    extra = 0
    readonly_fields = ('estnewgpgrowth','realnewgpgrowth','newgpgrowthpercent',
                        'estnegogpgrowth','realnegogpgrowth','negogpgrowthpercent',
                        'estchannelgpgrowth','realchannelgpgrowth','channelgpgrowthpercent',
                        'estbrandgpgrowth', 'realbrandgpgrowth','brandgpgrowthpercent',
                        'estsetgpgrowth','realsetgpgrowth','setgpgrowthpercent',
                        'estallgpgrowth','realallgpgrowth','allgpgrowthpercent',
                        )
                 
    verbose_name = verbose_name_plural = ('作战计划情况汇总(计算逻辑：根据销售填空的预估毛利润增量)')

    fields=  (('estnewgpgrowth','realnewgpgrowth','newgpgrowthpercent'),
               ('estnegogpgrowth','realnegogpgrowth','negogpgrowthpercent'),
               ('estchannelgpgrowth','realchannelgpgrowth','channelgpgrowthpercent'),
               ('estbrandgpgrowth', 'realbrandgpgrowth','brandgpgrowthpercent'),
               ('estsetgpgrowth','realsetgpgrowth','setgpgrowthpercent'),
               ('estallgpgrowth','realallgpgrowth','allgpgrowthpercent'),
               )

#----------------------------------------------------------------
#该科室该项目大类的相关产品明细'
class ATMenuforinlineInline(nested_admin.NestedTabularInline):
    model = ATMenuforinline
    form=ATMenuforinlineInlineForm
    extra = 0                  
    verbose_name = verbose_name_plural = ('该科室该项目大类的相关产品明细(供填报下方明细时参考)')
    readonly_fields= ('field_theoreticalgppercent',)
    fields=  ('supplier','brand','code','product','spec','unit','costperunit','priceperunit','purchaseqty',
              'purchasesum', 'theoreticalvalue','theoreticalgp',
              'field_theoreticalgppercent','machinemodel','machinebrand',
               )

    
    def field_theoreticalgppercent(self, obj):
        value = obj.theoreticalgppercent if obj.theoreticalgppercent else '--'
        style = 'width:50px'#; background-color: #f2f2f2;'
        return format_html('<div style={}>{}</div>', style,'{:.1%}'.format(value))
    field_theoreticalgppercent.short_description = '毛利率'

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['supplier'].widget.attrs['readonly'] = True
        formset.form.base_fields['brand'].widget.attrs['readonly'] = True
        formset.form.base_fields['code'].widget.attrs['readonly'] = True
        formset.form.base_fields['product'].widget.attrs['readonly'] = True
        formset.form.base_fields['spec'].widget.attrs['readonly'] = True
        formset.form.base_fields['unit'].widget.attrs['readonly'] = True
        formset.form.base_fields['costperunit'].widget.attrs['readonly'] = True
        formset.form.base_fields['priceperunit'].widget.attrs['readonly'] = True
        formset.form.base_fields['purchaseqty'].widget.attrs['readonly'] = True
        formset.form.base_fields['purchasesum'].widget.attrs['readonly'] = True
        formset.form.base_fields['theoreticalvalue'].widget.attrs['readonly'] = True
        formset.form.base_fields['theoreticalgp'].widget.attrs['readonly'] = True
        # formset.form.base_fields['theoreticalgppercent'].widget.attrs['readonly'] = True
        formset.form.base_fields['machinemodel'].widget.attrs['readonly'] = True
        formset.form.base_fields['machinebrand'].widget.attrs['readonly'] = True

        return formset


#!!!!!!!!!!ADMIN!!!!）））））））!!ADMIN!!!!!!!!ADMIN!!!!ADMIN!!!!!!ADMIN!!!!!ADMIN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!``````````````````````````````````````
#作战计划总表
@admin.register(ATOverall)
class ATOverallAdmin(nested_admin.NestedModelAdmin):
    form = ATOverallForm
    inlines=[ATMenuforinlineInline,ATNewProjectStatusInline,ATNegotiationStatusInline,ATChangeChannelStatusInline,ATChangeBrandStatusInline,ATSetStatusInline,ATCalculateInline]
    exclude = ('id','createtime','updatetime','is_active','operator')
    search_fields=['department','semidepartment','project','supplier','atmenuforinline__product']
    list_filter = ['department','semidepartment','project','supplier',IfWhyGrowthFilter]
    list_display_links =('project',)
    empty_value_display = '--'
    list_per_page = 10
    list_display = ('semidepartment','project','display_purchasesum','display_purchasesumpercent','display_theoreticalvalue','display_theoreticalgp', 'display_theoreticalgppercent',
                    'display_supplier','display_supplierpurchasesum','display_purchasesumpercentinproject','display_suppliertheoreticalvalue','display_suppliertheoreticalgp','display_suppliertheoreticalgppercent',                   
                    'relation','display_actionplan','whygrowth','display_progress','display_support',
                    'completemonth','monthgpgrowthdetail','thisyeargpgrowthdetail')#'display_monthgpgrowth',,'display_thisyeargpgrowth')
    ordering = ('-purchasesum','-supplierpurchasesum')
    readonly_fields =  ('thisyeargpgrowth','progress','support','monthgpgrowth', 'completemonth',
                        'monthgpgrowthdetail','thisyeargpgrowthdetail','actionplan','relation',
                        'field_purchasesum','field_purchasesumpercent','field_theoreticalvalue','field_theoreticalgp','field_theoreticalgppercent',
                        'field_supplierpurchasesum','field_purchasesumpercentinproject','field_suppliertheoreticalvalue',
                        'field_suppliertheoreticalgp','field_suppliertheoreticalgppercent',
                        )
    
    fieldsets = (('作战背景', {'fields': ('company','salesman','semidepartment','project',
                                      'field_purchasesum','field_purchasesumpercent','field_theoreticalvalue','field_theoreticalgp','field_theoreticalgppercent',
                                      'supplier','field_supplierpurchasesum','field_purchasesumpercentinproject','field_suppliertheoreticalvalue',
                                      'field_suppliertheoreticalgp','field_suppliertheoreticalgppercent',
                                    'relation','actionplan','whygrowth','progress','support','completemonth','monthgpgrowthdetail','monthgpgrowth',
                                    'thisyeargpgrowthdetail','thisyeargpgrowth'),
                            'classes': ('wide','extrapretty',),
                            'description': format_html(
            '<span style="color:{};font-size:13.0pt;">{}</span>','blue','注意：项目大类和增量来源是必填项。如增量来源选择多项，请在下方补充对应选项的进度和明细')}),
        )
    view_group_list = ['boss','AT','allviewonly','JConlyview']

    def add_view(self, request, form_url='', extra_context=None):
        print('add_viewadd_viewadd_viewadd_view')
        
        username = request.user.username
        print('username',username)
        # project_name = 'AT'
        existed_redis_data = cache.get(username)
                             
        if  existed_redis_data:            
            print(cache.delete(username),'新建项目，要把redis清空')

        return super().add_view(
            request, form_url, extra_context=extra_context,
        )





    #把项目的id放入redis，方便下面的ATMENU来获取对应id的details
    def change_view(self, request, object_id, form_url='', extra_context=None):
        
        print('change_viewchange_viewchange_view object_id',object_id)
        
        username = request.user.username
        print('username',username)
        project_name = 'AT'
        existed_redis_data = cache.get(username)
        #print('existed_redis_data',existed_redis_data)
        # expected redis_data : 
        # key:'name'
        # value: {'PXZ':{'object_id':1,...}
        #          '455':{'object_id:1,...}
        #         }

        user_selected_data = {'object_id':object_id}
                               
        if not existed_redis_data:
            # assemb the data
            data = {
                project_name:user_selected_data
            }
            print(data)
            print(cache.set(username,data,None))

        elif existed_redis_data: #{'PZX': {'object_id': '10'}, 'AT': {'object_id': '2'}}
            print(existed_redis_data,'elif existed_redis_data')
            existed_redis_data[project_name] = user_selected_data
            print(existed_redis_data,'elif')
            print(cache.set(username,existed_redis_data,None),'cache set ATOverallAdmin')

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


    # 新增或修改数据时，设置外键可选值，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company': 
            kwargs["queryset"] = Company.objects.filter(is_active=True,id=9) 
        if db_field.name == 'salesman': 
            kwargs["queryset"] = UserInfo.objects.filter(Q(is_active=True) & Q(username__in= ['zxl']))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

    # ------delete_model内层的红色删除键------------------------------
    def delete_model(self, request, obj):
        print('AT delete_model')
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or obj.salesman==request.user:             
            obj.is_active = False 
            obj.operator=request.user   
            if ATNewProjectStatus.objects.filter(overallid__id=obj.id,is_active=True):
                obj.atnewprojectstatus_set.all().update(is_active=False)
            if  ATNewProjectDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True):
                ATNewProjectDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True).update(is_active=False)

            if ATNegotiationStatus.objects.filter(overallid__id=obj.id,is_active=True):
                obj.atnegotiationstatus_set.all().update(is_active=False)
            if  ATNegotiationDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True):
                ATNegotiationDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True).update(is_active=False)

            if ATChangeChannelStatus.objects.filter(overallid__id=obj.id,is_active=True):
                obj.atchangechannelstatus_set.all().update(is_active=False)
            if  ATChangeChannelDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True):
                ATChangeChannelDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True).update(is_active=False)

            if ATChangeBrandStatus.objects.filter(overallid__id=obj.id,is_active=True):
                obj.atchangebrandstatus_set.all().update(is_active=False)
            if  ATBeforeChangeBrandDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True):
                ATBeforeChangeBrandDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True).update(is_active=False)
            if  ATAfterChangeBrandDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True):
                ATAfterChangeBrandDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True).update(is_active=False)

            if ATSetStatus.objects.filter(overallid__id=obj.id,is_active=True):
                obj.atsetstatus_set.all().update(is_active=False)
            if  ATSetDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True):
                ATSetDetail.objects.filter(progressid__overallid__id=obj.id,is_active=True).update(is_active=False)

            # if ATMenu.objects.filter(overallid__id=obj.id,is_active=True):
            #     obj.atmenu_set.all().update(is_active=False)
   
            if  ATCalculate.objects.filter(overallid__id=obj.id,is_active=True):   
                obj.atcalculate.is_active=False
                obj.atcalculate.save()

         

            obj.save()


    def delete_queryset(self,request, queryset):        
            print('我在delete_queryset')
            for delete_obj in queryset:     
                print('delete_queryset delete_obj',delete_obj)                    
                if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or delete_obj.salesman==request.user:     
                    delete_obj.is_active=False
                    delete_obj.operator=request.user
                    if ATNewProjectStatus.objects.filter(overallid__id=delete_obj.id,is_active=True):
                        delete_obj.atnewprojectstatus_set.all().update(is_active=False)
                    if  ATNewProjectDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True):
                        ATNewProjectDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True).update(is_active=False)

                    if ATNegotiationStatus.objects.filter(overallid__id=delete_obj.id,is_active=True):
                        delete_obj.atnegotiationstatus_set.all().update(is_active=False)
                    if  ATNegotiationDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True):
                        ATNegotiationDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True).update(is_active=False)

                    if  ATChangeChannelStatus.objects.filter(overallid__id=delete_obj.id,is_active=True):
                        delete_obj.atchangechannelstatus_set.all().update(is_active=False)
                    if  ATChangeChannelDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True):
                        ATChangeChannelDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True).update(is_active=False)

                    if ATChangeBrandStatus.objects.filter(overallid__id=delete_obj.id,is_active=True):
                        delete_obj.atchangebrandstatus_set.all().update(is_active=False)
                    if  ATBeforeChangeBrandDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True):
                        ATBeforeChangeBrandDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True).update(is_active=False)
                    if  ATAfterChangeBrandDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True):
                        ATAfterChangeBrandDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True).update(is_active=False)
                    
                    if ATSetStatus.objects.filter(overallid__id=delete_obj.id,is_active=True):
                        delete_obj.atsetstatus_set.all().update(is_active=False)
                    if  ATSetDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True):
                        ATSetDetail.objects.filter(progressid__overallid__id=delete_obj.id,is_active=True).update(is_active=False)

                    if  ATCalculate.objects.filter(overallid__id=delete_obj.id,is_active=True):   
                        delete_obj.atcalculate.is_active=False
                        delete_obj.atcalculate.save()
                    delete_obj.save()


         

    def save_model(self, request, obj, form, change):
        obj.operator = request.user

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change): 
        print('我在save_related') 
       

        super().save_related(request, form, formsets, change)
        whygrowth=''
        for eachformset in formsets: #循环每一个增量来源及明细,删除多填的信息
            # print('eachformset.model,eachformset.model',eachformset.model)
            if eachformset.model==ATNewProjectStatus:
                # print('eachformset-------ATNewProjectStatus------------=-=-=-=-=-=-',eachformset.cleaned_data)
                # print('eachformset.forms',eachformset.forms)
                statusobjs=ATNewProjectStatus.objects.filter(overallid__id=form.instance.id,is_active=True)
                if len(statusobjs)>1:
                    for i in range(1,len(statusobjs)):
                        detailobjs=ATNewProjectDetail.objects.filter(progressid__id=statusobjs[i].id,is_active=True)
                        detailobjs.update(is_active=False)
                        statusobjs[i].delete()
                if statusobjs:
                    print('statusobjs[0]',statusobjs[0])
                    whygrowth+='新开项目,'

            if eachformset.model==ATNegotiationStatus:
                # print('eachformset------ATNegotiationStatus------------=-=-=-=-=-=-',eachformset.cleaned_data)
                # print('eachformset.forms',eachformset.form)
                statusobjs=ATNegotiationStatus.objects.filter(overallid__id=form.instance.id,is_active=True)
                if len(statusobjs)>1:
                    for i in range(1,len(statusobjs)):
                        detailobjs=ATNegotiationDetail.objects.filter(progressid__id=statusobjs[i].id,is_active=True)
                        detailobjs.update(is_active=False)
                        statusobjs[i].delete()
                if statusobjs:
                    print('statusobjs[0]',statusobjs[0])
                    whygrowth+='供应商重新谈判,'

            if eachformset.model==ATChangeChannelStatus:
                # print('eachformset-------ATChangeChannelStatus------------=-=-=-=-=-=-',eachformset.cleaned_data)
                # print('eachformset.forms',eachformset.forms)
                statusobjs=ATChangeChannelStatus.objects.filter(overallid__id=form.instance.id,is_active=True)
                if len(statusobjs)>1:
                    for i in range(1,len(statusobjs)):
                        detailobjs=ATChangeChannelDetail.objects.filter(progressid__id=statusobjs[i].id,is_active=True)
                        detailobjs.update(is_active=False)
                        statusobjs[i].delete()  
                if statusobjs:   
                    whygrowth+='渠道变更,'

            if eachformset.model==ATChangeBrandStatus:
                # print('eachformset-------ATChangeBrandStatus------------=-=-=-=-=-=-',eachformset.cleaned_data)
                # print('eachformset.forms',eachformset.forms)
                statusobjs=ATChangeBrandStatus.objects.filter(overallid__id=form.instance.id,is_active=True)
                if len(statusobjs)>1:
                    for i in range(1,len(statusobjs)):
                        detailobjs=ATBeforeChangeBrandDetail.objects.filter(progressid__id=statusobjs[i].id,is_active=True)
                        detailobjs.update(is_active=False)
                        detailobjs2=ATAfterChangeBrandDetail.objects.filter(progressid__id=statusobjs[i].id,is_active=True)
                        detailobjs2.update(is_active=False)
                        statusobjs[i].delete() 
                if statusobjs: 
                    whygrowth+='品牌替换,'

            if eachformset.model==ATSetStatus:
                # print('eachformset-------ATSetStatus------------=-=-=-=-=-=-',eachformset.cleaned_data)
                # print('eachformset.forms',eachformset.forms)
                statusobjs=ATSetStatus.objects.filter(overallid__id=form.instance.id,is_active=True)
                if len(statusobjs)>1:
                    for i in range(1,len(statusobjs)):
                        detailobjs=ATSetDetail.objects.filter(progressid__id=statusobjs[i].id,is_active=True)
                        detailobjs.update(is_active=False)       
                        statusobjs[i].delete()  
                if statusobjs:
                    whygrowth+='套餐绑定,'

        progresses=[]
        completemonths=[]
        supports=[]
        actionplan=[]
        relation=[]
        monthgpgrowthdetail=[]
        thisyeargpgrowthdetail=[]
       
        newprojectmonthgpgrowthtotal=0
        for eachdetail in ATNewProjectDetail.objects.filter(progressid__overallid__id=form.instance.id,is_active=True):
            print('eachdetail',eachdetail)
          
            #costppl采购价/人份  = （采购价每单位 / 每单位人份数）
            eachdetail.costppl=eachdetail.costperunit/eachdetail.pplperunit
            #gppercent毛利率 （呈现%）  =  （LIS结算 -  采购价每单位 / 每单位人份数）/（LIS结算）
            eachdetail.gppercent=(eachdetail.lissettleprice-(eachdetail.costperunit/eachdetail.pplperunit))/eachdetail.lissettleprice
            #costfeepercent原采购价占收费比例 =（（采购价每单位 / 每单位人份数 ） /  LIS收费价 ）
            eachdetail.costfeepercent=(eachdetail.costperunit/eachdetail.pplperunit)/eachdetail.lisfee
            #marketpricefeepercent市场价占收费比例 =  （市场价/人份    /  LIS收费价 ）
            eachdetail.marketpricefeepercent=eachdetail.marketprice/eachdetail.lisfee
            #newcostdroprate 新采购价下降比例 =（（新采购价/人份   - （采购价每单位 / 每单位人份数）  ）/ （采购价每单位 / 每单位人份数））
            eachdetail.newcostdroprate=-(eachdetail.newcostppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
            #newgppercent新毛利率  =（LIS结算  -  新采购价/人份）/LIS结算
            eachdetail.newgppercent=(eachdetail.lissettleprice-eachdetail.newcostppl)/eachdetail.lissettleprice
            #newcostfeepercent新采购价占收费比例  =（新采购价/人份    /  LIS收费价 ）
            eachdetail.newcostfeepercent=eachdetail.newcostppl/eachdetail.lisfee
            #targetdropdate谈判下降比例 = （（谈判目标/元    -   （采购价每单位 / 每单位人份数） ）/ （采购价每单位 / 每单位人份数））
            eachdetail.targetdropdate=-(eachdetail.targetppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)

            if eachdetail.newcostppl  != 0:#如果有新采购价（谈判后的） 就按这个算
                eachdetail.estmonthlygpgrowth=(eachdetail.lissettleprice-eachdetail.newcostppl)*eachdetail.estimatemonthlyppl
            if  eachdetail.newcostppl  == 0 and eachdetail.targetppl  != 0: #如果有谈判价就按这个预估
                eachdetail.estmonthlygpgrowth=(eachdetail.lissettleprice-eachdetail.targetppl)*eachdetail.estimatemonthlyppl
            if eachdetail.newcostppl == 0 and eachdetail.targetppl  == 0 : #啥都没有就按初始报价算
                eachdetail.estmonthlygpgrowth=(eachdetail.lissettleprice-(eachdetail.costperunit/eachdetail.pplperunit))*eachdetail.estimatemonthlyppl                                  
            
            eachdetail.save()
            newprojectmonthgpgrowthtotal+=eachdetail.estmonthlygpgrowth

        if  ATNewProjectStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            newprojectobject= ATNewProjectStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            newprojectobject.monthgpgrowthbydetail  = newprojectmonthgpgrowthtotal
            newprojectobject.thisyeargpgrowthbydetail  = newprojectmonthgpgrowthtotal*(12-newprojectobject.completemonth)
            #根据销售填的月毛利增量预估来算今年度的：
            newprojectobject.thisyeargpgrowth  = newprojectobject.monthgpgrowth*(12-newprojectobject.completemonth)
            newprojectobject.save()
            progresses.append(newprojectobject.progress)
            completemonths.append(str(newprojectobject.completemonth) if newprojectobject.completemonth else '--' )
            supports.append(newprojectobject.support if newprojectobject.support else '--' )
            actionplan.append(newprojectobject.actionplan if newprojectobject.actionplan else '--' )
            relation.append(newprojectobject.relation if newprojectobject.relation else '--' )
            monthgpgrowthdetail.append(str('{:,.0f}'.format(newprojectobject.monthgpgrowth)) if newprojectobject.monthgpgrowth else '--' )
            thisyeargpgrowthdetail.append(str('{:,.0f}'.format(newprojectobject.thisyeargpgrowth))if newprojectobject.thisyeargpgrowth else '--' )
            
            status_history= [{  'department':newprojectobject.overallid.department,
                                'semidepartment':newprojectobject.overallid.semidepartment,
                                'project':newprojectobject.overallid.project,
                                'purchasesum':str(newprojectobject.overallid.purchasesum),
                                'purchasesumpercent':str(newprojectobject.overallid.purchasesumpercent),
                                'theoreticalvalue':str(newprojectobject.overallid.theoreticalvalue),
                                'theoreticalgp':str(newprojectobject.overallid.theoreticalgp),
                                'theoreticalgppercent':str(newprojectobject.overallid.theoreticalgppercent),

                                'supplier':str(newprojectobject.overallid.supplier),
                                'supplierpurchasesum':str(newprojectobject.overallid.supplierpurchasesum),
                                'purchasesumpercentinproject':str(newprojectobject.overallid.purchasesumpercentinproject),
                                'suppliertheoreticalvalue':str(newprojectobject.overallid.suppliertheoreticalvalue),
                                'suppliertheoreticalgp':str(newprojectobject.overallid.suppliertheoreticalgp),
                                'suppliertheoreticalgppercent':str(newprojectobject.overallid.suppliertheoreticalgppercent),

                                'whygrowth':newprojectobject.whygrowth,
                                'status':newprojectobject.progress,
                                'completemonth':str(newprojectobject.completemonth),
                                'monthgpgrowth':str(newprojectobject.monthgpgrowth),
                                'thisyeargpgrowth':str(newprojectobject.thisyeargpgrowth),
                                'monthgpgrowthbydetail':str(newprojectobject.monthgpgrowthbydetail),
                                'thisyeargpgrowthbydetail':str(newprojectobject.thisyeargpgrowthbydetail),
                                'target':str(newprojectobject.target),
                                'reason':str(newprojectobject.reason),
                                'relation':str(newprojectobject.relation),
                                'support':str(newprojectobject.support),
                                'actionplan':str(newprojectobject.actionplan),
                                'memo':str(newprojectobject.memo),
                                'time':str(datetime.now())                               
                               }]
            if not newprojectobject.statushistory:
                newprojectobject.statushistory=status_history
            else:
                newprojectobject.statushistory.extend(status_history)
            newprojectobject.save()


        #供应商重新谈判···········································································
        negotiationmonthgpgrowthtotal=0
        for eachdetail in ATNegotiationDetail.objects.filter(progressid__overallid__id=form.instance.id,is_active=True):
            
            eachdetail.product=str(eachdetail.productid.product)
            eachdetail.code=str(eachdetail.productid.code)
            eachdetail.originalsupplier=eachdetail.productid.supplier
            eachdetail.originalbrand=eachdetail.productid.brand
            eachdetail.spec=eachdetail.productid.spec
            eachdetail.unit=eachdetail.productid.unit
            eachdetail.purchaseqty=eachdetail.productid.purchaseqty
            eachdetail.recentcost=eachdetail.productid.purchasesum
            eachdetail.recentsales=eachdetail.productid.theoreticalvalue
            eachdetail.recentgp=eachdetail.productid.theoreticalgp
            
            eachdetail.save() 
            #如果这行数据是此次新填报的，而不是之前已经填的
            if not eachdetail.skuhistory or eachdetail.skuhistory=='':
                print('first time input')
                # print('eachdetail',eachdetail)
                # print('eachdetail.productid.product',eachdetail.productid.product,type(eachdetail.productid.product))
                eachdetail.costperunit=eachdetail.productid.costperunit
                eachdetail.gppercent=eachdetail.productid.theoreticalgppercent
                eachdetail.save()      

                #costppl采购价/人份  = （采购价每单位 / 每单位人份数）
                eachdetail.costppl=eachdetail.costperunit/eachdetail.pplperunit
                #recentgpofsupplier半年度供应商盈利额  =（半年度采购数量/单位 X 每单位人份数 X（采购价/人份 -  市场价/人份 ) )
                eachdetail.recentgpofsupplier=eachdetail.purchaseqty*eachdetail.pplperunit*(eachdetail.costperunit/eachdetail.pplperunit-eachdetail.marketprice)
                #costfeepercent原采购价占收费比例 =（（采购价每单位 / 每单位人份数 ） /  LIS收费价 ）
                eachdetail.costfeepercent=(eachdetail.costperunit/eachdetail.pplperunit)/eachdetail.lisfee
                #marketpricefeepercent市场价占收费比例 =  （市场价/人份    /  LIS收费价 ）
                eachdetail.marketpricefeepercent=eachdetail.marketprice/eachdetail.lisfee
                #newcostdroprate 新采购价下降比例 =（（新采购价/人份   - （采购价每单位 / 每单位人份数）  ）/ （采购价每单位 / 每单位人份数））
                eachdetail.newcostdroprate=0 if eachdetail.newcostppl==0 else -(eachdetail.newcostppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
                #不确定是用lis结算价作为销售价 还是用 （recentsales（thereticalvalue）/ 半年度采购数量每单位 ） /每单位人份数
                #newgppercent新毛利率  =（LIS结算价（开票价）  -  新采购价/人份）/（LIS结算价（开票价））
                eachdetail.newgppercent=0 if eachdetail.newcostppl==0 else (eachdetail.lissettleprice-eachdetail.newcostppl)/eachdetail.lissettleprice
                #newcostfeepercent新采购价占收费比例  =（新采购价/人份    /  LIS收费价 ）
                eachdetail.newcostfeepercent=eachdetail.newcostppl/eachdetail.lisfee
                #targetdropdate谈判下降比例 = （（谈判目标/元    -   （采购价每单位 / 每单位人份数） ）/ （采购价每单位 / 每单位人份数））
                eachdetail.targetdropdate=-(eachdetail.targetppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
                #realmonthlyppl月开票人份数=半年度进货数量/单位 * 每单位人份数/6，  #【注意！！！看看到底是几个月】
                eachdetail.realmonthlyppl=eachdetail.purchaseqty*eachdetail.pplperunit/6
                #gpgrowthppl毛利额增量/人份 = （（采购价每单位 / 每单位人份数）- 谈判目标/元  或者  新采购价/人份 ）
                #estmonthlygpgrowth预估月毛利额增量=半年度采购数量/单位 X 每单位人份数 / 6 X  （（采购价每单位 / 每单位人份数）- 谈判目标/元  或者 新采购价/人份 ）
                if eachdetail.newcostppl  != 0: #如果有新价格
                    eachdetail.gpgrowthppl=(eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.newcostppl
                    eachdetail.estmonthlygpgrowth=eachdetail.purchaseqty*eachdetail.pplperunit/6*((eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.newcostppl)
                else:#否则用谈判目标算
                    eachdetail.gpgrowthppl=(eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.targetppl
                    eachdetail.estmonthlygpgrowth=eachdetail.purchaseqty*eachdetail.pplperunit/6*((eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.targetppl)
                # print('eachdetail.productid.product', eachdetail.productid.product)      
                sku_history= [{'status':eachdetail.progressid.progress,
                               'completemonth':str(eachdetail.progressid.completemonth),
                               'monthgpgrowth':str(eachdetail.progressid.monthgpgrowth),
                               'time':str(datetime.now()),
                               'code':eachdetail.code,
                               'originalsupplier':eachdetail.originalsupplier,
                               'originalbrand':eachdetail.originalbrand,
                               'purchaseqty':str(eachdetail.purchaseqty),
                               'recentcost':str(eachdetail.recentcost),
                               'recentsales':str(eachdetail.recentsales),
                               'recentgp':str(eachdetail.recentgp),
                               'gppercent':str(eachdetail.gppercent),                        
                               'costperunit':str(eachdetail.costperunit),
                               'marketprice':str(eachdetail.marketprice),
                               'newcostppl':str(eachdetail.newcostppl),
                               'targetppl':str(eachdetail.targetppl),
                               'newgppercent':str(eachdetail.newgppercent),
                               'gpgrowthppl':str(eachdetail.gpgrowthppl),
                               'estmonthlygpgrowth':str(round(eachdetail.estmonthlygpgrowth,2)),
                               }]
                eachdetail.skuhistory=sku_history
                eachdetail.save()
                negotiationmonthgpgrowthtotal+=eachdetail.estmonthlygpgrowth
            
            else:
                print('not first time input')
                #如果之前填报的采购价比大菜单上的采购价多，说明后来降价了，那么将大菜单上的采购价赋值到新采购价中
                if eachdetail.costperunit > eachdetail.productid.costperunit:
                    eachdetail.newcostppl=eachdetail.productid.costperunit/eachdetail.pplperunit
                    eachdetail.newgppercent=eachdetail.productid.theoreticalgppercent#这是在大菜单里就算好的，如果成本更新了 毛利会直接更新
                    eachdetail.save()      

                #costppl采购价/人份  = （采购价每单位 / 每单位人份数）
                eachdetail.costppl=eachdetail.costperunit/eachdetail.pplperunit
                #recentgpofsupplier半年度供应商盈利额  =（半年度采购数量/单位 X 每单位人份数 X（采购价/人份 -  市场价/人份 ) )  !!!!!!!!!!用新的采购价来算供应商的盈利值,还是原来的供应商
                eachdetail.recentgpofsupplier=eachdetail.purchaseqty*eachdetail.pplperunit*(eachdetail.productid.costperunit/eachdetail.pplperunit-eachdetail.marketprice)
                #costfeepercent原采购价占收费比例 =（（采购价每单位 / 每单位人份数 ） /  LIS收费价 ）
                eachdetail.costfeepercent=(eachdetail.costperunit/eachdetail.pplperunit)/eachdetail.lisfee
                #marketpricefeepercent市场价占收费比例 =  （市场价/人份    /  LIS收费价 ）
                eachdetail.marketpricefeepercent=eachdetail.marketprice/eachdetail.lisfee
                #newcostdroprate 新采购价下降比例 =（（新采购价/人份   - （采购价每单位 / 每单位人份数）  ）/ （采购价每单位 / 每单位人份数））
                eachdetail.newcostdroprate=0 if eachdetail.newcostppl==0 else -(eachdetail.newcostppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
                # #newgppercent新毛利率  =（LIS结算价（开票价）  -  新采购价/人份）/（LIS结算价（开票价））
                # eachdetail.newgppercent=(eachdetail.lissettleprice-eachdetail.newcostppl)/eachdetail.lissettleprice
                #newcostfeepercent新采购价占收费比例  =（新采购价/人份    /  LIS收费价 ）
                eachdetail.newcostfeepercent=eachdetail.newcostppl/eachdetail.lisfee
                #targetdropdate谈判下降比例 = （（谈判目标/元    -   （采购价每单位 / 每单位人份数） ）/ （采购价每单位 / 每单位人份数））
                eachdetail.targetdropdate=-(eachdetail.targetppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
                #realmonthlyppl月开票人份数=半年度进货数量/单位 * 每单位人份数/6，  #【注意！！！看看到底是几个月】
                eachdetail.realmonthlyppl=eachdetail.purchaseqty*eachdetail.pplperunit/6
                #gpgrowthppl毛利额增量/人份 = （（采购价每单位 / 每单位人份数）- 谈判目标/元  或者  新采购价/人份 ）
                #estmonthlygpgrowth预估月毛利额增量=半年度采购数量/单位 X 每单位人份数 / 6 X  （（采购价每单位 / 每单位人份数）- 谈判目标/元  或者 新采购价/人份 ）
                if eachdetail.newcostppl  != 0: #如果有新价格
                    eachdetail.gpgrowthppl=(eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.newcostppl
                    eachdetail.estmonthlygpgrowth=eachdetail.purchaseqty*eachdetail.pplperunit/6*((eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.newcostppl)
                else:#否则用谈判目标算
                    eachdetail.gpgrowthppl=(eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.targetppl
                    eachdetail.estmonthlygpgrowth=eachdetail.purchaseqty*eachdetail.pplperunit/6*((eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.targetppl)
                # print('eachdetail.productid.product', eachdetail.productid.product)         
                sku_history= [{'status':eachdetail.progressid.progress,
                               'completemonth':str(eachdetail.progressid.completemonth),
                               'monthgpgrowth':str(eachdetail.progressid.monthgpgrowth),
                                'time':str(datetime.now()),
                               'code':eachdetail.code,
                               'originalsupplier':eachdetail.originalsupplier,
                               'originalbrand':eachdetail.originalbrand,
                               'purchaseqty':str(eachdetail.purchaseqty),
                               'recentcost':str(eachdetail.recentcost),
                               'recentsales':str(eachdetail.recentsales),
                               'recentgp':str(eachdetail.recentgp),
                               'gppercent':str(eachdetail.gppercent),                        
                               'costperunit':str(eachdetail.costperunit),
                               'marketprice':str(eachdetail.marketprice),
                               'newcostppl':str(eachdetail.newcostppl),
                               'targetppl':str(eachdetail.targetppl),
                               'newgppercent':str(eachdetail.newgppercent),
                               'gpgrowthppl':str(eachdetail.gpgrowthppl),
                               'estmonthlygpgrowth':str(round(eachdetail.estmonthlygpgrowth,2)),
                               }]
                eachdetail.skuhistory.extend(sku_history)
                eachdetail.save()
                negotiationmonthgpgrowthtotal+=eachdetail.estmonthlygpgrowth

        if ATNegotiationStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            print('negotiationobject',ATNegotiationStatus.objects.get(overallid__id=form.instance.id,is_active=True))
            negotiationobject= ATNegotiationStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            negotiationobject.monthgpgrowthbydetail  = negotiationmonthgpgrowthtotal
            negotiationobject.thisyeargpgrowthbydetail  = negotiationmonthgpgrowthtotal*(12-negotiationobject.completemonth)
            #根据销售填的月毛利增量预估来算今年度的：
            negotiationobject.thisyeargpgrowth  = negotiationobject.monthgpgrowth*(12-negotiationobject.completemonth)
            negotiationobject.save()
            progresses.append(negotiationobject.progress)
            completemonths.append(str(negotiationobject.completemonth) if negotiationobject.completemonth else '--' )
            supports.append(negotiationobject.support if negotiationobject.support else '--' )
            actionplan.append(negotiationobject.actionplan if negotiationobject.actionplan else '--' )
            relation.append(negotiationobject.relation if negotiationobject.relation else '--' )
            monthgpgrowthdetail.append(str('{:,.0f}'.format(negotiationobject.monthgpgrowth)) if negotiationobject.monthgpgrowth else '--' )
            thisyeargpgrowthdetail.append(str('{:,.0f}'.format(negotiationobject.thisyeargpgrowth)) if negotiationobject.thisyeargpgrowth else '--' )

            status_history= [{  'department':negotiationobject.overallid.department,
                                'semidepartment':negotiationobject.overallid.semidepartment,
                                'project':negotiationobject.overallid.project,
                                'purchasesum':str(negotiationobject.overallid.purchasesum),
                                'purchasesumpercent':str(negotiationobject.overallid.purchasesumpercent),
                                'theoreticalvalue':str(negotiationobject.overallid.theoreticalvalue),
                                'theoreticalgp':str(negotiationobject.overallid.theoreticalgp),
                                'theoreticalgppercent':str(negotiationobject.overallid.theoreticalgppercent),

                                'supplier':str(negotiationobject.overallid.supplier),
                                'supplierpurchasesum':str(negotiationobject.overallid.supplierpurchasesum),
                                'purchasesumpercentinproject':str(negotiationobject.overallid.purchasesumpercentinproject),
                                'suppliertheoreticalvalue':str(negotiationobject.overallid.suppliertheoreticalvalue),
                                'suppliertheoreticalgp':str(negotiationobject.overallid.suppliertheoreticalgp),
                                'suppliertheoreticalgppercent':str(negotiationobject.overallid.suppliertheoreticalgppercent),

                                'whygrowth':negotiationobject.whygrowth,
                                'status':negotiationobject.progress,
                                'completemonth':str(negotiationobject.completemonth),
                                'monthgpgrowth':str(negotiationobject.monthgpgrowth),
                                'thisyeargpgrowth':str(negotiationobject.thisyeargpgrowth),
                                'monthgpgrowthbydetail':str(negotiationobject.monthgpgrowthbydetail),
                                'thisyeargpgrowthbydetail':str(negotiationobject.thisyeargpgrowthbydetail),
                                'target':str(negotiationobject.target),
                                'reason':str(negotiationobject.reason),
                                'relation':str(negotiationobject.relation),
                                'support':str(negotiationobject.support),
                                'actionplan':str(negotiationobject.actionplan),
                                'memo':str(negotiationobject.memo),
                                'time':str(datetime.now())                               
                               }]
            if not negotiationobject.statushistory:
                negotiationobject.statushistory=status_history
            else:
                negotiationobject.statushistory.extend(status_history)
            negotiationobject.save()

        #渠道变更``````````````````````````````````````````````````````````````````````````````````
        changechannelobjectmonthgpgrowthtotal=0
        for eachdetail in ATChangeChannelDetail.objects.filter(progressid__overallid__id=form.instance.id,is_active=True):
            eachdetail.product=str(eachdetail.productid.product)
            eachdetail.code=str(eachdetail.productid.code)            
            eachdetail.originalbrand=eachdetail.productid.brand
            eachdetail.spec=eachdetail.productid.spec
            eachdetail.unit=eachdetail.productid.unit
            eachdetail.purchaseqty=eachdetail.productid.purchaseqty
            eachdetail.recentcost=eachdetail.productid.purchasesum
            eachdetail.recentsales=eachdetail.productid.theoreticalvalue
            eachdetail.recentgp=eachdetail.productid.theoreticalgp
            eachdetail.save()         
            if not eachdetail.skuhistory or eachdetail.skuhistory=='':
                print('ChangeChannel first time input')
                eachdetail.originalsupplier=eachdetail.productid.supplier
                eachdetail.costperunit=eachdetail.productid.costperunit
                eachdetail.gppercent=eachdetail.productid.theoreticalgppercent
                eachdetail.save()         
                #costppl采购价/人份  = （采购价每单位 / 每单位人份数）
                eachdetail.costppl=eachdetail.costperunit/eachdetail.pplperunit
                #recentgpofsupplier半年度供应商盈利额  =（半年度采购数量/单位 X 每单位人份数 X（采购价/人份 -  市场价/人份 ) )
                eachdetail.recentgpofsupplier=eachdetail.purchaseqty*eachdetail.pplperunit*(eachdetail.costperunit/eachdetail.pplperunit-eachdetail.marketprice)
                #costfeepercent原采购价占收费比例 =（（采购价每单位 / 每单位人份数 ） /  LIS收费价 ）
                eachdetail.costfeepercent=(eachdetail.costperunit/eachdetail.pplperunit)/eachdetail.lisfee
                #marketpricefeepercent市场价占收费比例 =  （市场价/人份    /  LIS收费价 ）
                eachdetail.marketpricefeepercent=eachdetail.marketprice/eachdetail.lisfee
                #newcostdroprate 新采购价下降比例 =（（新采购价/人份   - （采购价每单位 / 每单位人份数）  ）/ （采购价每单位 / 每单位人份数））
                eachdetail.newcostdroprate=0 if eachdetail.newcostppl==0 else -(eachdetail.newcostppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
                #不确定是用lis结算价作为销售价 还是用 （recentsales（thereticalvalue）/ 半年度采购数量每单位 ） /每单位人份数
                #newgppercent新毛利率  =（LIS结算价（开票价）  -  新采购价/人份）/（LIS结算价（开票价））
                eachdetail.newgppercent=0 if eachdetail.newcostppl==0 else (eachdetail.lissettleprice-eachdetail.newcostppl)/eachdetail.lissettleprice
                #newcostfeepercent新采购价占收费比例  =（新采购价/人份    /  LIS收费价 ）
                eachdetail.newcostfeepercent=eachdetail.newcostppl/eachdetail.lisfee
                #targetdropdate谈判下降比例 = （（谈判目标/元    -   （采购价每单位 / 每单位人份数） ）/ （采购价每单位 / 每单位人份数））
                eachdetail.targetdropdate=-(eachdetail.targetppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
                #realmonthlyppl月开票人份数=半年度进货数量/单位 * 每单位人份数/6，  #【注意！！！看看到底是几个月】
                eachdetail.realmonthlyppl=eachdetail.purchaseqty*eachdetail.pplperunit/6
                #gpgrowthppl毛利额增量/人份 = （（采购价每单位 / 每单位人份数）- 谈判目标/元  或者  新采购价/人份 ）
                #estmonthlygpgrowth预估月毛利额增量=半年度采购数量/单位 X 每单位人份数 / 6 X  （（采购价每单位 / 每单位人份数）- 谈判目标/元  或者 新采购价/人份 ）
                if eachdetail.newcostppl  != 0: #如果有新价格
                    eachdetail.gpgrowthppl=(eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.newcostppl
                    eachdetail.estmonthlygpgrowth=eachdetail.purchaseqty*eachdetail.pplperunit/6*((eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.newcostppl)
                if eachdetail.newcostppl  == 0 and eachdetail.targetppl  != 0:#否则用谈判目标算
                    eachdetail.gpgrowthppl=(eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.targetppl
                    eachdetail.estmonthlygpgrowth=eachdetail.purchaseqty*eachdetail.pplperunit/6*((eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.targetppl)
                if eachdetail.newcostppl == 0 and eachdetail.targetppl  == 0 :
                    eachdetail.gpgrowthppl=0
                    eachdetail.estmonthlygpgrowth=0
                eachdetail.save()
                sku_history= [{'originalsupplier':eachdetail.originalsupplier,
                               'originalbrand':eachdetail.originalbrand,
                               'newsupplier':eachdetail.newsupplier,
                               'code':eachdetail.code,
                               'purchaseqty':str(eachdetail.purchaseqty),
                               'recentcost':str(eachdetail.recentcost),
                               'recentsales':str(eachdetail.recentsales),
                               'recentgp':str(eachdetail.recentgp),
                               'gppercent':str(eachdetail.gppercent),                        
                               'costperunit':str(eachdetail.costperunit),
                               'marketprice':str(eachdetail.marketprice),
                               'newcostppl':str(eachdetail.newcostppl),
                               'targetppl':str(eachdetail.targetppl),
                               'newgppercent':str(eachdetail.newgppercent),
                               'gpgrowthppl':str(eachdetail.gpgrowthppl),
                               'estmonthlygpgrowth':str(round(eachdetail.estmonthlygpgrowth,2)),
                               }]
                eachdetail.skuhistory=sku_history
                eachdetail.save()
                changechannelobjectmonthgpgrowthtotal+=eachdetail.estmonthlygpgrowth
            
            #如果不是第一次填写，skuhistory已经有数据了的话
            else:
                #如果供应商名字变更了
                # print('eachdetail.originalsupplier',eachdetail.originalsupplier)
                # print('eachdetail.productid.supplier',eachdetail.productid.supplier)
                if eachdetail.productid.supplier!=eachdetail.originalsupplier:
                    print('渠道变更中，大菜单中的供应商已更换')
                    #新价格变成大菜单里的价格（就是新供应商的价格）
                    eachdetail.newsupplier=eachdetail.productid.supplier
                    eachdetail.newcostppl=eachdetail.productid.costperunit/eachdetail.pplperunit
                    eachdetail.newgppercent=eachdetail.productid.theoreticalgppercent#这是在大菜单里就算好的，如果成本更新了 毛利会直接更新
                    eachdetail.save()   

                #costppl采购价/人份  = （采购价每单位 / 每单位人份数）
                eachdetail.costppl=eachdetail.costperunit/eachdetail.pplperunit
                #recentgpofsupplier半年度供应商盈利额  =（半年度采购数量/单位 X 每单位人份数 X（采购价/人份 -  市场价/人份 ) )
                eachdetail.recentgpofsupplier=eachdetail.purchaseqty*eachdetail.pplperunit*(eachdetail.costperunit/eachdetail.pplperunit-eachdetail.marketprice)
                #costfeepercent原采购价占收费比例 =（（采购价每单位 / 每单位人份数 ） /  LIS收费价 ）
                eachdetail.costfeepercent=(eachdetail.costperunit/eachdetail.pplperunit)/eachdetail.lisfee
                #marketpricefeepercent市场价占收费比例 =  （市场价/人份    /  LIS收费价 ）
                eachdetail.marketpricefeepercent=eachdetail.marketprice/eachdetail.lisfee
                #newcostdroprate 新采购价下降比例 =（（新采购价/人份   - （采购价每单位 / 每单位人份数）  ）/ （采购价每单位 / 每单位人份数））
                eachdetail.newcostdroprate=0 if eachdetail.newcostppl==0 else -(eachdetail.newcostppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
                
                #newcostfeepercent新采购价占收费比例  =（新采购价/人份    /  LIS收费价 ）
                eachdetail.newcostfeepercent=eachdetail.newcostppl/eachdetail.lisfee
                #targetdropdate谈判下降比例 = （（谈判目标/元    -   （采购价每单位 / 每单位人份数） ）/ （采购价每单位 / 每单位人份数））
                eachdetail.targetdropdate=-(eachdetail.targetppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
                #realmonthlyppl月开票人份数=半年度进货数量/单位 * 每单位人份数/6，  #【注意！！！看看到底是几个月】
                eachdetail.realmonthlyppl=eachdetail.purchaseqty*eachdetail.pplperunit/6
                #gpgrowthppl毛利额增量/人份 = （（采购价每单位 / 每单位人份数）- 谈判目标/元  或者  新采购价/人份 ）
                #estmonthlygpgrowth预估月毛利额增量=半年度采购数量/单位 X 每单位人份数 / 6 X  （（采购价每单位 / 每单位人份数）- 谈判目标/元  或者 新采购价/人份 ）
                if eachdetail.newcostppl  != 0: #如果有新价格
                    print('#如果有新价格')
                    eachdetail.gpgrowthppl=(eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.newcostppl
                    eachdetail.estmonthlygpgrowth=eachdetail.purchaseqty*eachdetail.pplperunit/6*((eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.newcostppl)
                if eachdetail.newcostppl  == 0 and eachdetail.targetppl  != 0:
                    print('#否则用谈判目标算')
                    eachdetail.gpgrowthppl=(eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.targetppl
                    eachdetail.estmonthlygpgrowth=eachdetail.purchaseqty*eachdetail.pplperunit/6*((eachdetail.costperunit/eachdetail.pplperunit)-eachdetail.targetppl)
                if eachdetail.newcostppl == 0 and eachdetail.targetppl  == 0 :
                    eachdetail.gpgrowthppl=0
                    eachdetail.estmonthlygpgrowth=0
                eachdetail.save()
                sku_history= [{'originalsupplier':eachdetail.originalsupplier,
                            'originalbrand':eachdetail.originalbrand,
                            'newsupplier':eachdetail.productid.supplier,
                            'code':eachdetail.code,
                            'purchaseqty':str(eachdetail.purchaseqty),
                            'recentcost':str(eachdetail.recentcost),
                            'recentsales':str(eachdetail.recentsales),
                            'recentgp':str(eachdetail.recentgp),
                            'gppercent':str(eachdetail.gppercent),                        
                            'costperunit':str(eachdetail.costperunit),
                            'marketprice':str(eachdetail.marketprice),
                            'newcostppl':str(eachdetail.newcostppl),
                            'targetppl':str(eachdetail.targetppl),
                            'newgppercent':str(eachdetail.newgppercent),
                            'gpgrowthppl':str(eachdetail.gpgrowthppl),
                            'estmonthlygpgrowth':str(round(eachdetail.estmonthlygpgrowth,2)),
                            }]
                eachdetail.skuhistory.extend(sku_history)
                eachdetail.save()
                changechannelobjectmonthgpgrowthtotal+=eachdetail.estmonthlygpgrowth

        if ATChangeChannelStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            print('changechannelobject',ATChangeChannelStatus.objects.get(overallid__id=form.instance.id,is_active=True))
            changechannelobject= ATChangeChannelStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            changechannelobject.monthgpgrowthbydetail  = changechannelobjectmonthgpgrowthtotal
            changechannelobject.thisyeargpgrowthbydetail  = changechannelobjectmonthgpgrowthtotal*(12-changechannelobject.completemonth)
            #根据销售填的月毛利增量预估来算今年度的：
            changechannelobject.thisyeargpgrowth  = changechannelobject.monthgpgrowth*(12-changechannelobject.completemonth)
            changechannelobject.save()
            progresses.append(changechannelobject.progress)
            completemonths.append(str(changechannelobject.completemonth) if changechannelobject.completemonth else '--' )
            supports.append(changechannelobject.support if changechannelobject.support else '--' )
            actionplan.append(changechannelobject.actionplan if changechannelobject.actionplan else '--' )
            relation.append(changechannelobject.relation if changechannelobject.relation else '--' )
            monthgpgrowthdetail.append(str('{:,.0f}'.format(changechannelobject.monthgpgrowth)) if changechannelobject.monthgpgrowth else '--' )
            thisyeargpgrowthdetail.append(str('{:,.0f}'.format(changechannelobject.thisyeargpgrowth)) if changechannelobject.thisyeargpgrowth else '--' )

            status_history= [{  'department':changechannelobject.overallid.department,
                                'semidepartment':changechannelobject.overallid.semidepartment,
                                'project':changechannelobject.overallid.project,
                                'purchasesum':str(changechannelobject.overallid.purchasesum),
                                'purchasesumpercent':str(changechannelobject.overallid.purchasesumpercent),
                                'theoreticalvalue':str(changechannelobject.overallid.theoreticalvalue),
                                'theoreticalgp':str(changechannelobject.overallid.theoreticalgp),
                                'theoreticalgppercent':str(changechannelobject.overallid.theoreticalgppercent),

                                'supplier':str(changechannelobject.overallid.supplier),
                                'supplierpurchasesum':str(changechannelobject.overallid.supplierpurchasesum),
                                'purchasesumpercentinproject':str(changechannelobject.overallid.purchasesumpercentinproject),
                                'suppliertheoreticalvalue':str(changechannelobject.overallid.suppliertheoreticalvalue),
                                'suppliertheoreticalgp':str(changechannelobject.overallid.suppliertheoreticalgp),
                                'suppliertheoreticalgppercent':str(changechannelobject.overallid.suppliertheoreticalgppercent),

                                'whygrowth':changechannelobject.whygrowth,
                                'status':changechannelobject.progress,
                                'completemonth':str(changechannelobject.completemonth),
                                'monthgpgrowth':str(changechannelobject.monthgpgrowth),
                                'thisyeargpgrowth':str(changechannelobject.thisyeargpgrowth),
                                'monthgpgrowthbydetail':str(changechannelobject.monthgpgrowthbydetail),
                                'thisyeargpgrowthbydetail':str(changechannelobject.thisyeargpgrowthbydetail),
                                'target':str(changechannelobject.target),
                                'reason':str(changechannelobject.reason),
                                'relation':str(changechannelobject.relation),
                                'support':str(changechannelobject.support),
                                'actionplan':str(changechannelobject.actionplan),
                                'memo':str(changechannelobject.memo),
                                'time':str(datetime.now())                               
                               }]
            if not changechannelobject.statushistory:
                changechannelobject.statushistory=status_history
            else:
                changechannelobject.statushistory.extend(status_history)
            changechannelobject.save()



        #品牌替换前  ·············································································      ·    
        beforechangebrandmonthgpgrowthtotal=0
        for eachdetail in ATBeforeChangeBrandDetail.objects.filter(progressid__overallid__id=form.instance.id,is_active=True):
            # print('eachdetail',eachdetail)
            eachdetail.product=str(eachdetail.productid.product)
            eachdetail.code=str(eachdetail.productid.code) 
            eachdetail.originalsupplier=eachdetail.productid.supplier
            eachdetail.originalbrand=eachdetail.productid.brand
            eachdetail.spec=eachdetail.productid.spec
            eachdetail.unit=eachdetail.productid.unit
            eachdetail.purchaseqty=eachdetail.productid.purchaseqty
            eachdetail.recentcost=eachdetail.productid.purchasesum
            eachdetail.recentsales=eachdetail.productid.theoreticalvalue
            eachdetail.recentgp=eachdetail.productid.theoreticalgp         
            eachdetail.costperunit=eachdetail.productid.costperunit
            eachdetail.gppercent=eachdetail.productid.theoreticalgppercent
            eachdetail.save()   
            #costppl采购价/人份  = （采购价每单位 / 每单位人份数）
            eachdetail.costppl=eachdetail.costperunit/eachdetail.pplperunit
            #recentgpofsupplier半年度供应商盈利额  =（半年度采购数量/单位 X 每单位人份数 X（采购价/人份 -  市场价/人份 ) )
            eachdetail.recentgpofsupplier=eachdetail.purchaseqty*eachdetail.pplperunit*(eachdetail.costperunit/eachdetail.pplperunit-eachdetail.marketprice)
            #costfeepercent原采购价占收费比例 =（（采购价每单位 / 每单位人份数 ） /  LIS收费价 ）
            eachdetail.costfeepercent=(eachdetail.costperunit/eachdetail.pplperunit)/eachdetail.lisfee
            #marketpricefeepercent市场价占收费比例 =  （市场价/人份    /  LIS收费价 ）
            eachdetail.marketpricefeepercent=eachdetail.marketprice/eachdetail.lisfee
            #realmonthlyppl月开票人份数=半年度进货数量/单位 * 每单位人份数/6，  #【注意！！！看看到底是几个月】
            eachdetail.realmonthlyppl=eachdetail.purchaseqty*eachdetail.pplperunit/6
            #monthgp月毛利润 =   月开票人份数 *（（销售价每单位 / 每单位人份数）-（采购价每单位 / 每单位人份数））
            eachdetail.monthgp=eachdetail.purchaseqty/6 *(eachdetail.productid.priceperunit-eachdetail.costperunit)
            eachdetail.save()
            sku_history= [{'originalsupplier':eachdetail.originalsupplier,
                            'originalbrand':eachdetail.originalbrand,
                            'newsupplier':eachdetail.newsupplier,
                            'code':eachdetail.code,
                            'purchaseqty':str(eachdetail.purchaseqty),
                            'recentcost':str(eachdetail.recentcost),
                            'recentsales':str(eachdetail.recentsales),
                            'recentgp':str(eachdetail.recentgp),
                            'gppercent':str(eachdetail.gppercent),                        
                            'costperunit':str(eachdetail.costperunit),
                            'monthgp':str(round(eachdetail.monthgp,2)),
                            }]
            eachdetail.skuhistory=sku_history
            eachdetail.save()
            beforechangebrandmonthgpgrowthtotal+=eachdetail.monthgp
           
        #品牌替换后
        afterchangebrandmonthgpgrowthtotal=0
        for eachdetail in ATAfterChangeBrandDetail.objects.filter(progressid__overallid__id=form.instance.id,is_active=True):
            print('eachdetail',eachdetail)
          
            #costppl采购价/人份  = （采购价每单位 / 每单位人份数）
            eachdetail.costppl=eachdetail.costperunit/eachdetail.pplperunit
            #gppercent毛利率 （呈现%）  =  （LIS结算  -  采购价每单位 / 每单位人份数）/（LIS结算）
            eachdetail.gppercent=(eachdetail.lissettleprice-(eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.lissettleprice)
            #costfeepercent原采购价占收费比例 =（（采购价每单位 / 每单位人份数 ） /  LIS收费价 ）
            eachdetail.costfeepercent=(eachdetail.costperunit/eachdetail.pplperunit)/eachdetail.lisfee
            #marketpricefeepercent市场价占收费比例 =  （市场价/人份    /  LIS收费价 ）
            eachdetail.marketpricefeepercent=eachdetail.marketprice/eachdetail.lisfee
            #newcostdroprate 新采购价下降比例 =（（新采购价/人份   - （采购价每单位 / 每单位人份数）  ）/ （采购价每单位 / 每单位人份数））
            eachdetail.newcostdroprate=-(eachdetail.newcostppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
            #newgppercent新毛利率  =（LIS结算 -  新采购价/人份）/（LIS结算）
            eachdetail.newgppercent=(eachdetail.lissettleprice-eachdetail.newcostppl)/(eachdetail.lissettleprice)
            #newcostfeepercent新采购价占收费比例  =（新采购价/人份    /  LIS收费价 ）
            eachdetail.newcostfeepercent=eachdetail.newcostppl/eachdetail.lisfee
            #targetdropdate谈判下降比例 = （（谈判目标/元    -   （采购价每单位 / 每单位人份数） ）/ （采购价每单位 / 每单位人份数））
            eachdetail.targetdropdate=-(eachdetail.targetppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
            #monthgp月毛利润  **（预估每月lis开票的人份数   *（lis结算  -  新采购价/人份<mark>或者</mark> 谈判目标/元））** 
            if eachdetail.newcostppl  != 0:
                eachdetail.monthgp=(eachdetail.lissettleprice-eachdetail.newcostppl)*eachdetail.estimatemonthlyppl
            if  eachdetail.newcostppl  == 0 and eachdetail.targetppl  != 0:
                eachdetail.monthgp=(eachdetail.lissettleprice-eachdetail.targetppl)*eachdetail.estimatemonthlyppl
            if eachdetail.newcostppl == 0 and eachdetail.targetppl  == 0 :
                eachdetail.monthgp=(eachdetail.lissettleprice-(eachdetail.costperunit/eachdetail.pplperunit))*eachdetail.estimatemonthlyppl
            eachdetail.save()

            afterchangebrandmonthgpgrowthtotal+=eachdetail.monthgp
        brandchangegpgrowth=afterchangebrandmonthgpgrowthtotal-beforechangebrandmonthgpgrowthtotal

        if ATChangeBrandStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            print('changebrandobject',ATChangeBrandStatus.objects.get(overallid__id=form.instance.id,is_active=True))
            changebrandobject= ATChangeBrandStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            changebrandobject.monthgpgrowthbydetail  = brandchangegpgrowth
            changebrandobject.thisyeargpgrowthbydetail  = brandchangegpgrowth*(12-changebrandobject.completemonth)
            #根据销售填的月毛利增量预估来算今年度的：
            changebrandobject.thisyeargpgrowth  = changebrandobject.monthgpgrowth*(12-changebrandobject.completemonth)
            changebrandobject.save()
            progresses.append(changebrandobject.progress)
            completemonths.append(str(changebrandobject.completemonth) if changebrandobject.completemonth else '--' )
            supports.append(changebrandobject.support if changebrandobject.support else '--' )
            actionplan.append(changebrandobject.actionplan if changebrandobject.actionplan else '--' )
            relation.append(changebrandobject.relation if changebrandobject.relation else '--' )
            monthgpgrowthdetail.append(str('{:,.0f}'.format(changebrandobject.monthgpgrowth)) if changebrandobject.monthgpgrowth else '--' )
            thisyeargpgrowthdetail.append(str('{:,.0f}'.format(changebrandobject.thisyeargpgrowth)) if changebrandobject.thisyeargpgrowth else '--' )
        
            status_history= [{  'department':changebrandobject.overallid.department,
                                'semidepartment':changebrandobject.overallid.semidepartment,
                                'project':changebrandobject.overallid.project,
                                'purchasesum':str(changebrandobject.overallid.purchasesum),
                                'purchasesumpercent':str(changebrandobject.overallid.purchasesumpercent),
                                'theoreticalvalue':str(changebrandobject.overallid.theoreticalvalue),
                                'theoreticalgp':str(changebrandobject.overallid.theoreticalgp),
                                'theoreticalgppercent':str(changebrandobject.overallid.theoreticalgppercent),

                                'supplier':str(changebrandobject.overallid.supplier),
                                'supplierpurchasesum':str(changebrandobject.overallid.supplierpurchasesum),
                                'purchasesumpercentinproject':str(changebrandobject.overallid.purchasesumpercentinproject),
                                'suppliertheoreticalvalue':str(changebrandobject.overallid.suppliertheoreticalvalue),
                                'suppliertheoreticalgp':str(changebrandobject.overallid.suppliertheoreticalgp),
                                'suppliertheoreticalgppercent':str(changebrandobject.overallid.suppliertheoreticalgppercent),

                                'whygrowth':changebrandobject.whygrowth,
                                'status':changebrandobject.progress,
                                'completemonth':str(changebrandobject.completemonth),
                                'monthgpgrowth':str(changebrandobject.monthgpgrowth),
                                'thisyeargpgrowth':str(changebrandobject.thisyeargpgrowth),
                                'monthgpgrowthbydetail':str(changebrandobject.monthgpgrowthbydetail),
                                'thisyeargpgrowthbydetail':str(changebrandobject.thisyeargpgrowthbydetail),
                                'target':str(changebrandobject.target),
                                'reason':str(changebrandobject.reason),
                                'relation':str(changebrandobject.relation),
                                'support':str(changebrandobject.support),
                                'actionplan':str(changebrandobject.actionplan),
                                'memo':str(changebrandobject.memo),
                                'time':str(datetime.now())                               
                               }]
            if not changebrandobject.statushistory:
                changebrandobject.statushistory=status_history
            else:
                changebrandobject.statushistory.extend(status_history)
            changebrandobject.save()
        
        #套餐绑定
        setmonthgpgrowthtotal=0
        for eachdetail in ATSetDetail.objects.filter(progressid__overallid__id=form.instance.id,is_active=True):
            print('eachdetail',eachdetail)
            #costppl采购价/人份  = （采购价每单位 / 每单位人份数）
            eachdetail.costppl=eachdetail.costperunit/eachdetail.pplperunit
            #gppercent毛利率 （呈现%）  =  （LIS收费价 *  LIS结算%  -  采购价每单位 / 每单位人份数）/（LIS收费价 *  LIS结算%）
            eachdetail.gppercent=((eachdetail.lissettleprice)-(eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.lissettleprice)
            #costfeepercent原采购价占收费比例 =（（采购价每单位 / 每单位人份数 ） /  LIS收费价 ）
            eachdetail.costfeepercent=(eachdetail.costperunit/eachdetail.pplperunit)/eachdetail.lisfee
            #marketpricefeepercent市场价占收费比例 =  （市场价/人份    /  LIS收费价 ）
            eachdetail.marketpricefeepercent=eachdetail.marketprice/eachdetail.lisfee
            #newcostdroprate 新采购价下降比例 =（（新采购价/人份   - （采购价每单位 / 每单位人份数）  ）/ （采购价每单位 / 每单位人份数））
            eachdetail.newcostdroprate=-(eachdetail.newcostppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)
            #newgppercent新毛利率  =（LIS收费价 *  LIS结算%  -  新采购价/人份）/（LIS收费价 *  LIS结算%）
            eachdetail.newgppercent=((eachdetail.lissettleprice)-eachdetail.newcostppl)/(eachdetail.lissettleprice)
            #newcostfeepercent新采购价占收费比例  =（新采购价/人份    /  LIS收费价 ）
            eachdetail.newcostfeepercent=eachdetail.newcostppl/eachdetail.lisfee
            #targetdropdate谈判下降比例 = （（谈判目标/元    -   （采购价每单位 / 每单位人份数） ）/ （采购价每单位 / 每单位人份数））
            eachdetail.targetdropdate=-(eachdetail.targetppl  - (eachdetail.costperunit/eachdetail.pplperunit))/(eachdetail.costperunit/eachdetail.pplperunit)

            if eachdetail.newcostppl  != 0:#如果有新采购价（谈判后的） 就按这个算
                eachdetail.estmonthlygpgrowth=(eachdetail.lissettleprice-eachdetail.newcostppl)*eachdetail.estimatemonthlyppl
            if  eachdetail.newcostppl  == 0 and eachdetail.targetppl  != 0: #如果有谈判价就按这个预估
                eachdetail.estmonthlygpgrowth=(eachdetail.lissettleprice-eachdetail.targetppl)*eachdetail.estimatemonthlyppl
            if eachdetail.newcostppl == 0 and eachdetail.targetppl  == 0 : #啥都没有就按初始报价算
                eachdetail.estmonthlygpgrowth=(eachdetail.lissettleprice-(eachdetail.costperunit/eachdetail.pplperunit))*eachdetail.estimatemonthlyppl
            eachdetail.save()
            setmonthgpgrowthtotal+=eachdetail.estmonthlygpgrowth

        # print('newprojectmonthgpgrowthtotal',newprojectmonthgpgrowthtotal)
        if  ATSetStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            setobject= ATSetStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            setobject.monthgpgrowthbydetail  = setmonthgpgrowthtotal
            setobject.thisyeargpgrowthbydetail  = setmonthgpgrowthtotal*(12-setobject.completemonth)
            #根据销售填的月毛利增量预估来算今年度的：
            setobject.thisyeargpgrowth  = setobject.monthgpgrowth*(12-setobject.completemonth)
            setobject.save()
            progresses.append(setobject.progress)
            completemonths.append(str(setobject.completemonth) if setobject.completemonth else '--' )
            supports.append(setobject.support if setobject.support else '--' )
            actionplan.append(setobject.actionplan if setobject.actionplan else '--' )
            relation.append(setobject.relation if setobject.relation else '--' )
            monthgpgrowthdetail.append(str('{:,.0f}'.format(setobject.monthgpgrowth)) if setobject.monthgpgrowth else '--' )
            thisyeargpgrowthdetail.append(str('{:,.0f}'.format(setobject.thisyeargpgrowth))if setobject.thisyeargpgrowth else '--' )

            status_history= [{  'department':setobject.overallid.department,
                                'semidepartment':setobject.overallid.semidepartment,
                                'project':setobject.overallid.project,
                                'purchasesum':str(setobject.overallid.purchasesum),
                                'purchasesumpercent':str(setobject.overallid.purchasesumpercent),
                                'theoreticalvalue':str(setobject.overallid.theoreticalvalue),
                                'theoreticalgp':str(setobject.overallid.theoreticalgp),
                                'theoreticalgppercent':str(setobject.overallid.theoreticalgppercent),

                                'supplier':str(setobject.overallid.supplier),
                                'supplierpurchasesum':str(setobject.overallid.supplierpurchasesum),
                                'purchasesumpercentinproject':str(setobject.overallid.purchasesumpercentinproject),
                                'suppliertheoreticalvalue':str(setobject.overallid.suppliertheoreticalvalue),
                                'suppliertheoreticalgp':str(setobject.overallid.suppliertheoreticalgp),
                                'suppliertheoreticalgppercent':str(setobject.overallid.suppliertheoreticalgppercent),

                                'whygrowth':setobject.whygrowth,
                                'status':setobject.progress,
                                'completemonth':str(setobject.completemonth),
                                'monthgpgrowth':str(setobject.monthgpgrowth),
                                'thisyeargpgrowth':str(setobject.thisyeargpgrowth),
                                'monthgpgrowthbydetail':str(setobject.monthgpgrowthbydetail),
                                'thisyeargpgrowthbydetail':str(setobject.thisyeargpgrowthbydetail),
                                'target':str(setobject.target),
                                'reason':str(setobject.reason),
                                'relation':str(setobject.relation),
                                'support':str(setobject.support),
                                'actionplan':str(setobject.actionplan),
                                'memo':str(setobject.memo),
                                'time':str(datetime.now())                               
                               }]
            if not setobject.statushistory:
                setobject.statushistory=status_history
            else:
                setobject.statushistory.extend(status_history)
            setobject.save()

            
      #CALCULATE 用销售填报的月毛利额增量预估来填：
        if ATCalculate.objects.filter(overallid__id=form.instance.id,is_active=True):
            # print('原本有calculate：',ATCalculate.objects.get(overallid__id=form.instance.id,is_active=True))
            a=ATCalculate.objects.get(overallid__id=form.instance.id,is_active=True)
            a.estallgpgrowth=0
            a.estnewgpgrowth=0
            a.estnegogpgrowth=0    
            a.estchannelgpgrowth=0
            a.estbrandgpgrowth=0
            a.estsetgpgrowth=0
            
            if ATNewProjectStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                # print('有新的项目')
                newprojectobject = ATNewProjectStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                a.estnewgpgrowth += newprojectobject.monthgpgrowth 
                a.estallgpgrowth += newprojectobject.monthgpgrowth 
            if ATNegotiationStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                # print('有供应商谈判')
                negotiationobject = ATNegotiationStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                a.estnegogpgrowth += negotiationobject.monthgpgrowth 
                a.estallgpgrowth += negotiationobject.monthgpgrowth 
            if ATChangeChannelStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                changechannelobject = ATChangeChannelStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                a.estchannelgpgrowth += changechannelobject.monthgpgrowth 
                a.estallgpgrowth += changechannelobject.monthgpgrowth 
            if ATChangeBrandStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                changebrandobject = ATChangeBrandStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                a.estbrandgpgrowth += changebrandobject.monthgpgrowth 
                a.estallgpgrowth += changebrandobject.monthgpgrowth 
            if ATSetStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                # print('有新的项目')
                setobject = ATSetStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                a.estsetgpgrowth += setobject.monthgpgrowth 
                a.estallgpgrowth += setobject.monthgpgrowth 

            a.is_active=True
            a.save()
            print('原本有calculate，保存更新成功')

        else:
            print('不能获取对应的detailcalculate')            
            estallgpgrowth=0
            estnewgpgrowth=0
            estnegogpgrowth=0
            estchannelgpgrowth=0
            estbrandgpgrowth=0
            estsetgpgrowth=0

            if ATNewProjectStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                newprojectobject = ATNewProjectStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                estnewgpgrowth += newprojectobject.monthgpgrowth 
                estallgpgrowth += newprojectobject.monthgpgrowth 
            if ATNegotiationStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                negotiationobject = ATNegotiationStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                estnegogpgrowth += negotiationobject.monthgpgrowth 
                estallgpgrowth += negotiationobject.monthgpgrowth 
            if ATChangeChannelStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                changechannelobject = ATChangeChannelStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                estchannelgpgrowth += changechannelobject.monthgpgrowth 
                estallgpgrowth += changechannelobject.monthgpgrowth        
            if ATChangeBrandStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                changebrandobject = ATChangeBrandStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                estbrandgpgrowth += changebrandobject.monthgpgrowth 
                estallgpgrowth += changebrandobject.monthgpgrowth 
            if ATSetStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
                setobject = ATSetStatus.objects.get(overallid__id=form.instance.id,is_active=True)
                estsetgpgrowth += setobject.monthgpgrowth 
                estallgpgrowth += setobject.monthgpgrowth 
            ATCalculatedata={
                'overallid':form.instance,
                'estallgpgrowth':estallgpgrowth,
                'estnewgpgrowth':estnewgpgrowth,
                'estnegogpgrowth':estnegogpgrowth,                
                'estchannelgpgrowth':estchannelgpgrowth,
                'estbrandgpgrowth':estbrandgpgrowth,
                'estsetgpgrowth':estsetgpgrowth,
                'is_active':True,
            }
            ATCalculate.objects.create(**ATCalculatedata).save()
        

        overallobject= ATOverall.objects.get(id=form.instance.id)
        overallobject.whygrowth=whygrowth[:-1]
        overallobject.progress='|'.join(progresses)
        overallobject.completemonth='|'.join(completemonths)
        overallobject.support='|'.join(supports)
        overallobject.actionplan='|'.join(actionplan)
        overallobject.relation='|'.join(relation)
        overallobject.monthgpgrowthdetail='|'.join(monthgpgrowthdetail)
        overallobject.thisyeargpgrowthdetail='|'.join(thisyeargpgrowthdetail)
        overallmonthgpgrowth=0
        overallthisyeargpgrowth=0
        if ATNewProjectStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            newprojectobject = ATNewProjectStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            overallmonthgpgrowth += newprojectobject.monthgpgrowth 
            overallthisyeargpgrowth += newprojectobject.thisyeargpgrowth
        if ATNegotiationStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            negotiationobject = ATNegotiationStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            overallmonthgpgrowth += negotiationobject.monthgpgrowth 
            overallthisyeargpgrowth += negotiationobject.thisyeargpgrowth
        if ATChangeChannelStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            changechannelobject = ATChangeChannelStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            overallmonthgpgrowth += changechannelobject.monthgpgrowth 
            overallthisyeargpgrowth += changechannelobject.thisyeargpgrowth     
        if ATChangeBrandStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            changebrandobject = ATChangeBrandStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            overallmonthgpgrowth += changebrandobject.monthgpgrowth 
            overallthisyeargpgrowth += changebrandobject.thisyeargpgrowth      
        if ATSetStatus.objects.filter(overallid__id=form.instance.id,is_active=True):
            setobject = ATSetStatus.objects.get(overallid__id=form.instance.id,is_active=True)
            overallmonthgpgrowth += setobject.monthgpgrowth 
            overallthisyeargpgrowth += setobject.thisyeargpgrowth  

        overallobject.monthgpgrowth=overallmonthgpgrowth
        overallobject.thisyeargpgrowth=overallthisyeargpgrowth
        overallobject.save()
        print('save related 完结！')
  
    #只显示未被假删除的项目
    #------get_queryset-----------查询-------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser :
            return qs.filter(is_active=True,company_id=9)

        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True,company_id=9)
            
 #新增动作————统计按钮
    
    actions = ['calculate']   ######还没改完呢！！！！！
    def calculate(self, request, queryset):
        for i in queryset:
            overallmonthgpgrowth=0
            overallthisyeargpgrowth=0
            progresses=[]
            completemonths=[]
            supports=[]
            actionplan=[]
            monthgpgrowthdetail=[]
            thisyeargpgrowthdetail=[]
            relation=[]
            whygrowth=''
            if ATNewProjectStatus.objects.filter(overallid__id=i.id,is_active=True):
                newprojectobject = ATNewProjectStatus.objects.get(overallid__id=i.id,is_active=True)
                overallmonthgpgrowth += newprojectobject.monthgpgrowth 
                overallthisyeargpgrowth += newprojectobject.thisyeargpgrowth
                progresses.append(newprojectobject.progress)
                completemonths.append(str(newprojectobject.completemonth) if newprojectobject.completemonth else '--' )
                supports.append(newprojectobject.support if newprojectobject.support else '--' )
                actionplan.append(newprojectobject.actionplan if newprojectobject.actionplan else '--' )
                relation.append(newprojectobject.relation if newprojectobject.relation else '--' )
                monthgpgrowthdetail.append(str('{:,.0f}'.format(newprojectobject.monthgpgrowth)) if newprojectobject.monthgpgrowth else '--' )
                thisyeargpgrowthdetail.append(str('{:,.0f}'.format(newprojectobject.thisyeargpgrowth))if newprojectobject.thisyeargpgrowth else '--' )
                whygrowth+='新开项目,'
                newprojectestgpgrowth=0      
                for eachdata in ATNewProjectDetail.objects.filter(progressid__overallid__id=i.id,is_active=True):
                    newprojectestgpgrowth+=eachdata.estmonthlygpgrowth
                newprojectobject.monthgpgrowthbydetail=newprojectestgpgrowth
                newprojectobject.thisyeargpgrowthbydetail=newprojectestgpgrowth*(12-newprojectobject.completemonth)
                newprojectobject.save()

            if ATNegotiationStatus.objects.filter(overallid__id=i.id,is_active=True):
                negotiationobject = ATNegotiationStatus.objects.get(overallid__id=i.id,is_active=True)
                overallmonthgpgrowth += negotiationobject.monthgpgrowth 
                overallthisyeargpgrowth += negotiationobject.thisyeargpgrowth
                progresses.append(negotiationobject.progress)
                completemonths.append(str(negotiationobject.completemonth) if negotiationobject.completemonth else '--' )
                supports.append(negotiationobject.support if negotiationobject.support else '--' )
                actionplan.append(negotiationobject.actionplan if negotiationobject.actionplan else '--' )
                relation.append(negotiationobject.relation if negotiationobject.relation else '--' )
                monthgpgrowthdetail.append(str('{:,.0f}'.format(negotiationobject.monthgpgrowth)) if negotiationobject.monthgpgrowth else '--' )
                thisyeargpgrowthdetail.append(str('{:,.0f}'.format(negotiationobject.thisyeargpgrowth))if negotiationobject.thisyeargpgrowth else '--' )
                whygrowth+='供应商重新谈判,'
                negotiationestgpgrowth=0      
                for eachdata in ATNegotiationDetail.objects.filter(progressid__overallid__id=i.id,is_active=True):
                    negotiationestgpgrowth+=eachdata.estmonthlygpgrowth
                negotiationobject.monthgpgrowthbydetail=negotiationestgpgrowth
                negotiationobject.thisyeargpgrowthbydetail=negotiationestgpgrowth*(12-negotiationobject.completemonth)
                negotiationobject.save()

            if ATChangeChannelStatus.objects.filter(overallid__id=i.id,is_active=True):
                changechannelobject = ATChangeChannelStatus.objects.get(overallid__id=i.id,is_active=True)
                overallmonthgpgrowth += changechannelobject.monthgpgrowth 
                overallthisyeargpgrowth += changechannelobject.thisyeargpgrowth
                progresses.append(changechannelobject.progress)
                completemonths.append(str(changechannelobject.completemonth) if changechannelobject.completemonth else '--' )
                supports.append(changechannelobject.support if changechannelobject.support else '--' )
                actionplan.append(changechannelobject.actionplan if changechannelobject.actionplan else '--' )
                relation.append(changechannelobject.relation if changechannelobject.relation else '--' )
                monthgpgrowthdetail.append(str('{:,.0f}'.format(changechannelobject.monthgpgrowth)) if changechannelobject.monthgpgrowth else '--' )
                thisyeargpgrowthdetail.append(str('{:,.0f}'.format(changechannelobject.thisyeargpgrowth))if changechannelobject.thisyeargpgrowth else '--' )
                whygrowth+='渠道变更,'
                changechannelestgpgrowth=0      
                for eachdata in ATChangeChannelDetail.objects.filter(progressid__overallid__id=i.id,is_active=True):
                    changechannelestgpgrowth+=eachdata.estmonthlygpgrowth
                changechannelobject.monthgpgrowthbydetail=changechannelestgpgrowth
                changechannelobject.thisyeargpgrowthbydetail=changechannelestgpgrowth*(12-changechannelobject.completemonth)
                changechannelobject.save()

            if ATChangeBrandStatus.objects.filter(overallid__id=i.id,is_active=True):
                changebrandobject = ATChangeBrandStatus.objects.get(overallid__id=i.id,is_active=True)
                overallmonthgpgrowth += changebrandobject.monthgpgrowth 
                overallthisyeargpgrowth += changebrandobject.thisyeargpgrowth
                progresses.append(changebrandobject.progress)
                completemonths.append(str(changebrandobject.completemonth) if changebrandobject.completemonth else '--' )
                supports.append(changebrandobject.support if changebrandobject.support else '--' )  
                actionplan.append(changebrandobject.actionplan if changebrandobject.actionplan else '--' )
                relation.append(changebrandobject.relation if changebrandobject.relation else '--' )
                monthgpgrowthdetail.append(str('{:,.0f}'.format(changebrandobject.monthgpgrowth)) if changebrandobject.monthgpgrowth else '--' )
                thisyeargpgrowthdetail.append(str('{:,.0f}'.format(changebrandobject.thisyeargpgrowth))if changebrandobject.thisyeargpgrowth else '--' )
                whygrowth+='品牌替换,'
                beforechangebrandmonthgp=0      
                afterchangebrandmonthgp=0   
                for eachdata in ATBeforeChangeBrandDetail.objects.filter(progressid__overallid__id=i.id,is_active=True):
                    beforechangebrandmonthgp+=eachdata.monthgp
                for eachdata in ATAfterChangeBrandDetail.objects.filter(progressid__overallid__id=i.id,is_active=True):
                    afterchangebrandmonthgp+=eachdata.monthgp
                monthgpdelta=afterchangebrandmonthgp-beforechangebrandmonthgp
                changebrandobject.monthgpgrowthbydetail=monthgpdelta
                changebrandobject.thisyeargpgrowthbydetail=monthgpdelta*(12-changebrandobject.completemonth)
                changebrandobject.save()

            if ATSetStatus.objects.filter(overallid__id=i.id,is_active=True):
                setobject = ATSetStatus.objects.get(overallid__id=i.id,is_active=True)
                overallmonthgpgrowth += setobject.monthgpgrowth 
                overallthisyeargpgrowth += setobject.thisyeargpgrowth
                progresses.append(setobject.progress)
                completemonths.append(str(setobject.completemonth) if setobject.completemonth else '--' )
                supports.append(setobject.support if setobject.support else '--' )
                actionplan.append(setobject.actionplan if setobject.actionplan else '--' )
                relation.append(setobject.relation if setobject.relation else '--' )
                monthgpgrowthdetail.append(str('{:,.0f}'.format(setobject.monthgpgrowth)) if setobject.monthgpgrowth else '--' )
                thisyeargpgrowthdetail.append(str('{:,.0f}'.format(setobject.thisyeargpgrowth))if setobject.thisyeargpgrowth else '--' )
                whygrowth+='套餐绑定,'
                setestgpgrowth=0      
                for eachdata in ATSetDetail.objects.filter(progressid__overallid__id=i.id,is_active=True):
                    setestgpgrowth+=eachdata.estmonthlygpgrowth
                setobject.monthgpgrowthbydetail=setestgpgrowth
                setobject.thisyeargpgrowthbydetail=setestgpgrowth*(12-setobject.completemonth)
                setobject.save()

            # print(progresses,completemonths,supports)
            i.monthgpgrowth=overallmonthgpgrowth
            i.thisyeargpgrowth=overallthisyeargpgrowth
            i.progress='|'.join(progresses)
            # print(i.progress)
            i.completemonth='|'.join(completemonths)
            # print(i.completemonth)
            i.support='|'.join(supports)
            # print(i.support)
            i.actionplan='|'.join(actionplan)
            i.relation='|'.join(relation)
            i.monthgpgrowthdetail='|'.join(monthgpgrowthdetail)
            i.thisyeargpgrowthdetail='|'.join(thisyeargpgrowthdetail)
            i.whygrowth=whygrowth[:-1]
            i.save() 

    calculate.short_description = "统计" 
    calculate.type = 'info'
    calculate.style = 'color:white;'

    def field_purchasesum(self, obj):
        value = obj.purchasesum if obj.purchasesum else '--'
        return format_html('<div>{}</div>',  '{:,.0f}'.format(value))
    field_purchasesum.short_description = '项目1-6月成本'

    def field_purchasesumpercent(self, obj):
        value = obj.purchasesumpercent if obj.purchasesumpercent else '--'
        return format_html('<div>{}</div>',  '{:.1%}'.format(value))
    field_purchasesumpercent.short_description = '该项目占总成本占比'

    def field_theoreticalvalue(self, obj):
        value = obj.theoreticalvalue if obj.theoreticalvalue else '--'
        return format_html('<div>{}</div>',  '{:,.0f}'.format(value))
    field_theoreticalvalue.short_description = '项目销售额'

    def field_theoreticalgp(self, obj):
        value = obj.theoreticalgp if obj.theoreticalgp else '--'
        return format_html('<div>{}</div>',  '{:,.0f}'.format(value))
    field_theoreticalgp.short_description = '项目毛利润'

    def field_theoreticalgppercent(self, obj):
        value = obj.theoreticalgppercent if obj.theoreticalgppercent else '--'
        return format_html('<div>{}</div>',  '{:.1%}'.format(value))
    field_theoreticalgppercent.short_description = '项目毛利率'

#----------------------------
    def field_supplierpurchasesum(self, obj):
        value = obj.supplierpurchasesum if obj.supplierpurchasesum else '--'
        return format_html('<div>{}</div>',  '{:,.0f}'.format(value))
    field_supplierpurchasesum.short_description = '供应商1-6月成本'

    def field_purchasesumpercentinproject(self, obj):
        value = obj.purchasesumpercentinproject if obj.purchasesumpercentinproject else '--'
        return format_html('<div>{}</div>',  '{:.1%}'.format(value))
    field_purchasesumpercentinproject.short_description = '项目中各供应商成本占比'

    def field_suppliertheoreticalvalue(self, obj):
        value = obj.suppliertheoreticalvalue if obj.suppliertheoreticalvalue else '--'
        return format_html('<div>{}</div>',  '{:,.0f}'.format(value))
    field_suppliertheoreticalvalue.short_description = '供应商销售额'

    def field_suppliertheoreticalgp(self, obj):
        value = obj.suppliertheoreticalgp if obj.suppliertheoreticalgp else '--'
        return format_html('<div>{}</div>',  '{:,.0f}'.format(value))
    field_suppliertheoreticalgp.short_description = '供应商毛利润'

    def field_suppliertheoreticalgppercent(self, obj):
        value = obj.suppliertheoreticalgppercent if obj.suppliertheoreticalgppercent else '--'
        return format_html('<div>{}</div>',  '{:.1%}'.format(value))
    field_suppliertheoreticalgppercent.short_description = '供应商毛利率'


#----------------------------


    @admin.display(ordering="purchasesum",description=format_html('项目1-6月<br>销售成本'))
    def display_purchasesum(self, obj):
        return  '{:,.0f}'.format(obj.purchasesum)
    
    @admin.display(ordering="purchasesumpercent",description=format_html('该项目占<br>总成本<br>占比'))
    def display_purchasesumpercent(self, obj):
        return  '{:.1%}'.format(obj.purchasesumpercent)
    

    @admin.display(ordering="theoreticalvalue",description=format_html('项目1-6月<br>实际销售额'))
    def display_theoreticalvalue(self, obj):
        return  '{:,.0f}'.format(obj.theoreticalvalue)

    @admin.display(ordering="theoreticalgp",description=format_html('项目<br>毛利润'))
    def display_theoreticalgp(self, obj):
        return  '{:,.0f}'.format(obj.theoreticalgp)
    
    @admin.display(ordering="theoreticalgppercent",description=format_html('项目<br>毛利率'))
    def display_theoreticalgppercent(self, obj):
        return  '{:.1%}'.format(obj.theoreticalgppercent)
    
#----------------------------

    @admin.display(ordering="supplierpurchasesum",description=format_html('供应商1-6月<br>销售成本'))
    def display_supplierpurchasesum(self, obj):
        return  '{:,.0f}'.format(obj.supplierpurchasesum)
    
    @admin.display(ordering="purchasesumpercentinproject",description=format_html('项目中各<br>供应商<br>成本占比'))
    def display_purchasesumpercentinproject(self, obj):
        return  '{:.1%}'.format(obj.purchasesumpercentinproject)
    

    @admin.display(ordering="suppliertheoreticalvalue",description=format_html('供应商<br>实际销售额'))
    def display_suppliertheoreticalvalue(self, obj):
        return  '{:,.0f}'.format(obj.suppliertheoreticalvalue)

    @admin.display(ordering="suppliertheoreticalgp",description=format_html('供应商<br>毛利润'))
    def display_suppliertheoreticalgp(self, obj):
        return  '{:,.0f}'.format(obj.suppliertheoreticalgp)
    
    @admin.display(ordering="suppliertheoreticalgppercent",description=format_html('供应商<br>毛利率'))
    def display_suppliertheoreticalgppercent(self, obj):
        return  '{:.1%}'.format(obj.suppliertheoreticalgppercent)

#----------------------------
    @admin.display(ordering="supplier",description='供应商')
    def display_supplier(self, obj):
        if obj.supplier:
            name=obj.supplier
        else:
            name='--'  
        # div_width = '20%'    
        wrapped_name = textwrap.fill(name, width=15)
        return  format_html('<div style="width:100px;">{}</div>', wrapped_name) 


    @admin.display(ordering="progress",description='进度')
    def display_progress(self, obj):
        if obj.progress:
            name=obj.progress
        else:
            name='--'  
        wrapped_name = textwrap.fill(name, width=10)
        return  format_html('<div style="width: 100px;">{}</div>', wrapped_name)  
    
    @admin.display(ordering="support",description='所需支持')
    def display_support(self, obj):
        if obj.support:
            name=obj.support
        else:
            name='--'  
        # div_width = '20%'    
        wrapped_name = textwrap.fill(name, width=15)
        return  format_html('<div style="width:100px;">{}</div>', wrapped_name)  
    
    @admin.display(ordering="actionplan",description='行动计划')
    def display_actionplan(self, obj):
        if obj.actionplan:
            name=obj.actionplan
        else:
            name='--'  
        # div_width = '20%'    
        wrapped_name = textwrap.fill(name, width=15)
        return  format_html('<div style="width:100px;">{}</div>', wrapped_name)  


    @admin.display(ordering="monthgpgrowth",description=format_html('月毛利额<br>增量预估'))
    def display_monthgpgrowth(self, obj):
        return  '{:,}'.format(obj.monthgpgrowth)
    
    @admin.display(ordering="thisyeargpgrowth",description=format_html('23年毛利额<br>增量预估总计'))
    def display_thisyeargpgrowth(self, obj):
        return  '{:,}'.format(obj.thisyeargpgrowth)
#~~~~~~~~~~~

#新开项目状态
@admin.register(ATNewProjectStatus)
class ATNewProjectStatusAdmin(nested_admin.NestedModelAdmin):
 
    exclude = ('id','createtime','updatetime')
    readonly_fields= ('monthgpgrowthbydetail','thisyeargpgrowthbydetail')
    fields=['progress','completemonth','monthgpgrowth', 'thisyeargpgrowth','monthgpgrowthbydetail','thisyeargpgrowthbydetail','target','reason','relation','support','memo','advicedirector','adviceboss'] 
    empty_value_display = '--'
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    


#新开项目明细
@admin.register(ATNewProjectDetail)
class ATNewProjectDetailAdmin(nested_admin.NestedModelAdmin):
    exclude = ('id','createtime','updatetime')
    list_display_links=('progressid__overallid__project',)
    list_display = ('progressid__overallid__semidepartment','progressid__overallid__project','progressid__progress','originalsupplier','originalbrand',#newsupplier，beforeorafterbrandchange
                    'code','product','spec', 
                    'unit','pplperunit_display',#'recentsales','recentcost','recentgp','recentgpofsupplier',
                    'lisfee_display','lispercent_display','lissettleprice','costperunit_display','costppl',#'purchaseqty',
                    'costfeepercent_display','gppercent_display','marketprice_display','marketpricefeepercent_display',
                    'newcostppl','newcostdroprate_display','newcostfeepercent_display','newgppercent_display',
                    'targetppl_display','targetdropdate_display','estimatemonthlyppl_display',
                    'estmonthlygpgrowth', #'gpgrowthppl',
                    )
    # list_display_widths = {'estimatemonthlyppl': '50px', 'estmonthlygpgrowth': '150px'}
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    empty_value_display = '--'



    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    

    def delete_model(self, request, obj):
        print('我在DETAILADMIN delete_model,, obj.progressid.overallid.salesman',obj.progressid.overallid.salesman)
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or obj.progressid.overallid.salesman==request.user:              
            obj.is_active = False 
            obj.progressid.overallid.operator=request.user
            obj.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if actions.get('delete_selected'):
                del actions['delete_selected']
        return actions

    @admin.display(ordering="progressid__progress",description='项目进度')
    def progressid__progress(self, obj):
        return obj.progressid.progress
        
    @admin.display(ordering="progressid__overallid__department",description='科室')
    def progressid__overallid__department(self, obj):
        return obj.progressid.overallid.department    
    
    @admin.display(ordering="progressid__overallid__semidepartment",description='使用科室')
    def progressid__overallid__semidepartment(self, obj):
        return obj.progressid.overallid.semidepartment   
    
    @admin.display(ordering="progressid__overallid__project",description='项目大类')
    def progressid__overallid__project(self, obj):
        return obj.progressid.overallid.project

    @admin.display(ordering="pplperunit",description='每单位人份数')
    def pplperunit_display(self, obj):
        return obj.pplperunit

    @admin.display(ordering="lisfee",description='Lis收费')
    def lisfee_display(self, obj):
        return obj.lisfee
    
    @admin.display(ordering="marketprice",description='市场价/人份')
    def marketprice_display(self, obj):
        return obj.marketprice
    
    @admin.display(ordering="costperunit",description='采购价/单位')
    def costperunit_display(self, obj):
        return obj.costperunit
    
    @admin.display(ordering="targetppl",description='谈判目标')
    def targetppl_display(self, obj):
        return obj.targetppl

    @admin.display(ordering="lispercent",description='Lis结算比')
    def lispercent_display(self, obj):
        return '{:.1f}%'.format(obj.lispercent*100) 
    
    @admin.display(ordering="gppercent",description='原毛利率')
    def gppercent_display(self, obj):
        return '{:.1f}%'.format(obj.gppercent*100)  
       
    @admin.display(ordering="costfeepercent",description='原采购价占收费比')
    def costfeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.costfeepercent*100) 
    
    @admin.display(ordering="marketpricefeepercent",description='市场价占收费比')
    def marketpricefeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.marketpricefeepercent*100) 

    @admin.display(ordering="newcostdroprate",description='新采购价下降比')
    def newcostdroprate_display(self, obj):
        return '{:.1f}%'.format(obj.newcostdroprate*100) 
    
    @admin.display(ordering="newgppercent",description='新毛利率')
    def newgppercent_display(self, obj):
        return '{:.1f}%'.format(obj.newgppercent*100)  
       
    @admin.display(ordering="newcostfeepercent",description='新采购价占收费比')
    def newcostfeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.newcostfeepercent*100) 
    
    @admin.display(ordering="targetdropdate",description='谈判下降比')
    def targetdropdate_display(self, obj):
        return '{:.1f}%'.format(obj.targetdropdate*100)     


    @admin.display(ordering="estimatemonthlyppl",description='预估月开票人份数')
    def estimatemonthlyppl_display(self, obj):
        return obj.estimatemonthlyppl



#供应商重新谈判状态
@admin.register(ATNegotiationStatus)
class ATNegotiationStatusAdmin(nested_admin.NestedModelAdmin):
 
    exclude = ('id','createtime','updatetime')
    fields=['progress','target','relation','reason','memo','advicedirector','adviceboss'] 
    empty_value_display = '--'
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    

#供应商重新谈判明细
@admin.register(ATNegotiationDetail)
class ATNegotiationDetailAdmin(nested_admin.NestedModelAdmin):
    exclude = ('id','createtime','updatetime','skuhistory')
    list_display_links=('progressid__overallid__project',)

    list_display = ('progressid__overallid__semidepartment','progressid__overallid__project','progressid__progress','productid__supplier','productid__brand',#newsupplier，beforeorafterbrandchange
                    'code','productid__product','spec', 
                    'unit','pplperunit_display','recentsales_display','recentcost_display','recentgp_display','recentgpofsupplier_display',
                    'lisfee_display','lissettleprice','costperunit_display','costppl_display','purchaseqty_display', #'lispercent_display',
                    'gppercent_display','costfeepercent_display','marketprice_display','marketpricefeepercent_display',
                    'newcostppl_display','newcostdroprate_display','newgppercent_display','newcostfeepercent_display',
                    'targetppl_display','targetdropdate_display','realmonthlyppl_display',#'estimatemonthlyppl',
                    'gpgrowthppl_display','estmonthlygpgrowth_display', 
                    )
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    empty_value_display = '--'
    autocomplete_fields=['productid']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'productid': 
            kwargs["queryset"] = ATMenu.objects.filter(is_active=True) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if actions.get('delete_selected'):
                del actions['delete_selected']
        return actions

    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    

    
    @admin.display(ordering="progressid__progress",description='进度')
    def progressid__progress(self, obj):
        if obj.progressid.progress:
            name=obj.progressid.progress
        else:
            name='--'  
        wrapped_name = textwrap.fill(name, width=6)
        return format_html('<div style="width: 50px;">{}</div>',wrapped_name)   
        
    @admin.display(ordering="progressid__overallid__semidepartment",description='使用科室')
    def progressid__overallid__semidepartment(self, obj):
        if obj.progressid.overallid.semidepartment:
            name=obj.progressid.overallid.semidepartment
        else:
            name='--'  
        wrapped_name = textwrap.fill(name, width=6)
        return  format_html('<div style="width: 50px;">{}</div>', wrapped_name)  
    
    @admin.display(ordering="progressid__overallid__project",description='项目大类')
    def progressid__overallid__project(self, obj):
        return obj.progressid.overallid.project

    @admin.display(ordering="productid__supplier",description='供应商')
    def productid__supplier(self, obj):
        if obj.productid.supplier:
            name=obj.productid.supplier
        else:
            name='--'            
        wrapped_name = textwrap.fill(name, width=10)
        return  format_html('<div style="width: 100px;">{}</div>', wrapped_name)
    
    @admin.display(ordering="productid__brand",description='品牌')
    def productid__brand(self, obj):
        if obj.productid.brand:
            name=obj.productid.brand
        else:
            name='--'  
        wrapped_name = textwrap.fill(name, width=6)
        return  format_html('<div style="width: 50px;">{}</div>', wrapped_name)
    
    @admin.display(ordering="productid__product",description='产品名称')
    def productid__product(self, obj):
        if obj.productid.product:
            name=obj.productid.product
        else:
            name='--'  
        wrapped_name = textwrap.fill(name, width=18)
        return  format_html('<div style="width: 180px;">{}</div>', wrapped_name)



    @admin.display(ordering="pplperunit",description=format_html('每单位<br>人份数'))
    def pplperunit_display(self, obj):
        return obj.pplperunit
    
    @admin.display(ordering="recentsales",description=format_html('半年度开票额'))
    def recentsales_display(self, obj):
        return '{:,}'.format(obj.recentsales)

    @admin.display(ordering="recentcost",description=format_html('半年度采购额'))
    def recentcost_display(self, obj):
        return '{:,}'.format(obj.recentcost)

    @admin.display(ordering="recentgp",description=format_html('半年度盈亏额'))
    def recentgp_display(self, obj):
        return '{:,}'.format(obj.recentgp)
    
    @admin.display(ordering="recentgpofsupplier",description=format_html('半年度供应商<br>盈利额'))
    def recentgpofsupplier_display(self, obj):
        return '{:,}'.format(obj.recentgpofsupplier)
    
    @admin.display(ordering="lisfee",description='Lis收费')
    def lisfee_display(self, obj):
        return obj.lisfee
    
    @admin.display(ordering="marketprice",description=format_html('市场价<br>/人份'))
    def marketprice_display(self, obj):
        return '{:,}'.format(obj.marketprice)
    
    @admin.display(ordering="costperunit",description=format_html('原采购价<br>/单位'))
    def costperunit_display(self, obj):
        return '{:,}'.format(obj.costperunit)
    
    @admin.display(ordering="costppl",description=format_html('原采购价<br>/人份'))
    def costppl_display(self, obj):
        return obj.costppl
    
    @admin.display(ordering="newcostppl",description=format_html('新采购价<br>/人份'))
    def newcostppl_display(self, obj):
        return obj.newcostppl

    @admin.display(ordering="purchaseqty",description=format_html('半年度采购<br>数量/单位'))
    def purchaseqty_display(self, obj):
        return  '{:,}'.format(obj.purchaseqty)
    
    @admin.display(ordering="targetppl",description='谈判目标')
    def targetppl_display(self, obj):
        return obj.targetppl

    @admin.display(ordering="lispercent",description='Lis结算比')
    def lispercent_display(self, obj):
        return '{:.1f}%'.format(obj.lispercent*100) 
    
    @admin.display(ordering="gppercent",description='原毛利率')
    def gppercent_display(self, obj):
        return '{:.1f}%'.format(obj.gppercent*100)  
       
    @admin.display(ordering="costfeepercent",description=format_html('原采购价<br>占收费比'))
    def costfeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.costfeepercent*100) 
    
    @admin.display(ordering="marketpricefeepercent",description=format_html('市场价占<br>收费比'))
    def marketpricefeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.marketpricefeepercent*100) 

    @admin.display(ordering="newcostdroprate",description=format_html('新采购价<br>下降比'))
    def newcostdroprate_display(self, obj):
        return '{:.1f}%'.format(obj.newcostdroprate*100) 
    
    @admin.display(ordering="newgppercent",description='新毛利率')
    def newgppercent_display(self, obj):
        return '{:.1f}%'.format(obj.newgppercent*100)  
       
    @admin.display(ordering="newcostfeepercent",description=format_html('新采购价<br>占收费比'))
    def newcostfeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.newcostfeepercent*100) 
    
    @admin.display(ordering="targetdropdate",description='谈判下降比')
    def targetdropdate_display(self, obj):
        return '{:.1f}%'.format(obj.targetdropdate*100)   

    @admin.display(ordering="realmonthlyppl",description=format_html('每月lis开票<br>人份数'))
    def realmonthlyppl_display(self, obj):
        return obj.realmonthlyppl

    @admin.display(ordering="gpgrowthppl",description=format_html('毛利额增量<br>/人份'))
    def gpgrowthppl_display(self, obj):
        return obj.gpgrowthppl
    
    @admin.display(ordering="estmonthlygpgrowth",description=format_html('预估月毛利<br>额增量'))
    def estmonthlygpgrowth_display(self, obj):
        return obj.estmonthlygpgrowth

#渠道变更明细
@admin.register(ATChangeChannelDetail)
class ATChangeChannelDetailAdmin(nested_admin.NestedModelAdmin):
    exclude = ('id','createtime','updatetime','skuhistory')
    list_display_links=('progressid__overallid__project',)

    list_display = ('progressid__overallid__semidepartment','progressid__overallid__project','progressid__progress','originalsupplier','originalbrand','newsupplier',#，beforeorafterbrandchange
                    'code','product','spec', 
                    'unit','pplperunit','recentsales','recentcost','recentgp','recentgpofsupplier',
                    'lisfee','lispercent','lissettleprice','costperunit','costppl','purchaseqty',
                    'gppercent','costfeepercent','marketprice','marketpricefeepercent',
                    'newcostppl','newcostdroprate','newgppercent','newcostfeepercent',
                    'targetppl','targetdropdate','realmonthlyppl',#'estimatemonthlyppl',
                    'gpgrowthppl','estmonthlygpgrowth', 
                    )
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    empty_value_display = '--'
    autocomplete_fields=['productid']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'productid': 
            kwargs["queryset"] = ATMenu.objects.filter(is_active=True) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if actions.get('delete_selected'):
                del actions['delete_selected']
        return actions
    
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    
    @admin.display(ordering="progressid__progress",description='渠道变更进度')
    def progressid__progress(self, obj):
        return obj.progressid.progress
        
    @admin.display(ordering="progressid__overallid__department",description='科室')
    def progressid__overallid__department(self, obj):
        return obj.progressid.overallid.department    
    
    @admin.display(ordering="progressid__overallid__semidepartment",description='使用科室')
    def progressid__overallid__semidepartment(self, obj):
        return obj.progressid.overallid.semidepartment 
    
    @admin.display(ordering="progressid__overallid__project",description='项目大类')
    def progressid__overallid__project(self, obj):
        return obj.progressid.overallid.project




#品牌替换前明细
@admin.register(ATBeforeChangeBrandDetail)
class ATBeforeChangeBrandAdmin(nested_admin.NestedModelAdmin):
    exclude = ('id','createtime','updatetime','skuhistory')
    list_display_links=('progressid__overallid__project',)

    list_display = ('progressid__overallid__semidepartment','progressid__overallid__project','progressid__progress','originalsupplier','originalbrand',#，beforeorafterbrandchange
                    'code','product','spec', 
                    'unit','pplperunit','recentsales','recentcost','recentgp','recentgpofsupplier',
                    'lisfee','lispercent','lissettleprice','costperunit','costppl','purchaseqty',
                    'gppercent','costfeepercent','marketprice','marketpricefeepercent',
                    'newcostppl','newcostdroprate','newgppercent','newcostfeepercent',
                    'targetppl','targetdropdate','realmonthlyppl',#'estimatemonthlyppl',
                    'gpgrowthppl','estmonthlygpgrowth', 
                    )
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    empty_value_display = '--'
    autocomplete_fields=['productid']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'productid': 
            kwargs["queryset"] = ATMenu.objects.filter(is_active=True) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    
    @admin.display(ordering="progressid__progress",description='品牌替换进度')
    def progressid__progress(self, obj):
        return obj.progressid.progress
        
    @admin.display(ordering="progressid__overallid__department",description='科室')
    def progressid__overallid__department(self, obj):
        return obj.progressid.overallid.department    
    

    @admin.display(ordering="progressid__overallid__semidepartment",description='使用科室')
    def progressid__overallid__semidepartment(self, obj):
        return obj.progressid.overallid.semidepartment  
    
    @admin.display(ordering="progressid__overallid__project",description='项目大类')
    def progressid__overallid__project(self, obj):
        return obj.progressid.overallid.project




#品牌替换后明细
@admin.register(ATAfterChangeBrandDetail)
class ATAfterChangeBrandDetailAdmin(nested_admin.NestedModelAdmin):
    exclude = ('id','createtime','updatetime')
    list_display_links=('progressid__overallid__project',)
    list_display = ('progressid__overallid__department','progressid__overallid__project','progressid__progress','originalsupplier','originalbrand',#newsupplier，beforeorafterbrandchange
                    'code','product','spec', 
                    'unit','pplperunit_display',#'recentsales','recentcost','recentgp','recentgpofsupplier',
                    'lisfee_display','lispercent_display','lissettleprice','costperunit_display','costppl',#'purchaseqty',
                    'costfeepercent_display','gppercent_display','marketprice_display','marketpricefeepercent_display',
                    'newcostppl','newcostdroprate_display','newcostfeepercent_display','newgppercent_display',
                    'targetppl_display','targetdropdate_display','estimatemonthlyppl_display','monthgp'
                   # 'estmonthlygpgrowth', #'gpgrowthppl',
                    )
    # list_display_widths = {'estimatemonthlyppl': '50px', 'estmonthlygpgrowth': '150px'}
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    empty_value_display = '--'



    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    

    def delete_model(self, request, obj):
        print('我在DETAILADMIN delete_model,, obj.progressid.overallid.salesman',obj.progressid.overallid.salesman)
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or obj.progressid.overallid.salesman==request.user:              
            obj.is_active = False 
            obj.progressid.overallid.operator=request.user
            obj.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if actions.get('delete_selected'):
                del actions['delete_selected']
        return actions


    @admin.display(ordering="progressid__progress",description='品牌替换进度')
    def progressid__progress(self, obj):
        return obj.progressid.progress
        
    @admin.display(ordering="progressid__overallid__department",description='科室')
    def progressid__overallid__department(self, obj):
        return obj.progressid.overallid.department    
    
    @admin.display(ordering="progressid__overallid__project",description='项目大类')
    def progressid__overallid__project(self, obj):
        return obj.progressid.overallid.project

    @admin.display(ordering="pplperunit",description='每单位人份数')
    def pplperunit_display(self, obj):
        return obj.pplperunit

    @admin.display(ordering="lisfee",description='Lis收费')
    def lisfee_display(self, obj):
        return obj.lisfee
    
    @admin.display(ordering="marketprice",description='市场价/人份')
    def marketprice_display(self, obj):
        return obj.marketprice
    
    @admin.display(ordering="costperunit",description='采购价/单位')
    def costperunit_display(self, obj):
        return obj.costperunit
    
    @admin.display(ordering="targetppl",description='谈判目标')
    def targetppl_display(self, obj):
        return obj.targetppl

    @admin.display(ordering="lispercent",description='Lis结算比')
    def lispercent_display(self, obj):
        return '{:.1f}%'.format(obj.lispercent*100) 
    
    @admin.display(ordering="gppercent",description='原毛利率')
    def gppercent_display(self, obj):
        return '{:.1f}%'.format(obj.gppercent*100)  
       
    @admin.display(ordering="costfeepercent",description='原采购价占收费比')
    def costfeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.costfeepercent*100) 
    
    @admin.display(ordering="marketpricefeepercent",description='市场价占收费比')
    def marketpricefeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.marketpricefeepercent*100) 

    @admin.display(ordering="newcostdroprate",description='新采购价下降比')
    def newcostdroprate_display(self, obj):
        return '{:.1f}%'.format(obj.newcostdroprate*100) 
    
    @admin.display(ordering="newgppercent",description='新毛利率')
    def newgppercent_display(self, obj):
        return '{:.1f}%'.format(obj.newgppercent*100)  
       
    @admin.display(ordering="newcostfeepercent",description='新采购价占收费比')
    def newcostfeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.newcostfeepercent*100) 
    
    @admin.display(ordering="targetdropdate",description='谈判下降比')
    def targetdropdate_display(self, obj):
        return '{:.1f}%'.format(obj.targetdropdate*100)     


    @admin.display(ordering="estimatemonthlyppl",description='预估月开票人份数')
    def estimatemonthlyppl_display(self, obj):
        return obj.estimatemonthlyppl





#套餐绑定明细
@admin.register(ATSetDetail)
class ATSetDetailAdmin(nested_admin.NestedModelAdmin):
    exclude = ('id','createtime','updatetime')
    list_display_links=('progressid__overallid__project',)
    list_display = ('progressid__overallid__semidepartment','progressid__overallid__project','progressid__progress','originalsupplier','originalbrand',#newsupplier，beforeorafterbrandchange
                    'code','product','spec', 
                    'unit','pplperunit_display',#'recentsales','recentcost','recentgp','recentgpofsupplier',
                    'lisfee_display','lispercent_display','lissettleprice','costperunit_display','costppl',#'purchaseqty',
                    'costfeepercent_display','gppercent_display','marketprice_display','marketpricefeepercent_display',
                    'newcostppl','newcostdroprate_display','newcostfeepercent_display','newgppercent_display',
                    'targetppl_display','targetdropdate_display','estimatemonthlyppl_display',
                    'estmonthlygpgrowth', #'gpgrowthppl',
                    )
    # list_display_widths = {'estimatemonthlyppl': '50px', 'estmonthlygpgrowth': '150px'}
    view_group_list = ['boss','AT','allviewonly','JConlyview']
    empty_value_display = '--'



    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print('我在PMRResearchDetailInline-get_queryset')
        if request.user.is_superuser :
            # print('我在PMRResearchDetailInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True)
       #普通销售的话:
        return qs.filter(is_active=True)
    

    def delete_model(self, request, obj):
        print('我在DETAILADMIN delete_model,, obj.progressid.overallid.salesman',obj.progressid.overallid.salesman)
        if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss' or obj.progressid.overallid.salesman==request.user:              
            obj.is_active = False 
            obj.progressid.overallid.operator=request.user
            obj.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if actions.get('delete_selected'):
                del actions['delete_selected']
        return actions

    @admin.display(ordering="progressid__progress",description='进度')
    def progressid__progress(self, obj):
        return obj.progressid.progress
        
    @admin.display(ordering="progressid__overallid__department",description='科室')
    def progressid__overallid__department(self, obj):
        return obj.progressid.overallid.department    
    @admin.display(ordering="progressid__overallid__semidepartment",description='使用科室')
    def progressid__overallid__semidepartment(self, obj):
        return obj.progressid.overallid.semidepartment    
    
    @admin.display(ordering="progressid__overallid__project",description='项目大类')
    def progressid__overallid__project(self, obj):
        return obj.progressid.overallid.project

    @admin.display(ordering="pplperunit",description='每单位人份数')
    def pplperunit_display(self, obj):
        return obj.pplperunit

    @admin.display(ordering="lisfee",description='Lis收费')
    def lisfee_display(self, obj):
        return obj.lisfee
    
    @admin.display(ordering="marketprice",description='市场价/人份')
    def marketprice_display(self, obj):
        return obj.marketprice
    
    @admin.display(ordering="costperunit",description='采购价/单位')
    def costperunit_display(self, obj):
        return obj.costperunit
    
    @admin.display(ordering="targetppl",description='谈判目标')
    def targetppl_display(self, obj):
        return obj.targetppl

    @admin.display(ordering="lispercent",description='Lis结算比')
    def lispercent_display(self, obj):
        return '{:.1f}%'.format(obj.lispercent*100) 
    
    @admin.display(ordering="gppercent",description='原毛利率')
    def gppercent_display(self, obj):
        return '{:.1f}%'.format(obj.gppercent*100)  
       
    @admin.display(ordering="costfeepercent",description='原采购价占收费比')
    def costfeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.costfeepercent*100) 
    
    @admin.display(ordering="marketpricefeepercent",description='市场价占收费比')
    def marketpricefeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.marketpricefeepercent*100) 

    @admin.display(ordering="newcostdroprate",description='新采购价下降比')
    def newcostdroprate_display(self, obj):
        return '{:.1f}%'.format(obj.newcostdroprate*100) 
    
    @admin.display(ordering="newgppercent",description='新毛利率')
    def newgppercent_display(self, obj):
        return '{:.1f}%'.format(obj.newgppercent*100)  
       
    @admin.display(ordering="newcostfeepercent",description='新采购价占收费比')
    def newcostfeepercent_display(self, obj):
        return '{:.1f}%'.format(obj.newcostfeepercent*100) 
    
    @admin.display(ordering="targetdropdate",description='谈判下降比')
    def targetdropdate_display(self, obj):
        return '{:.1f}%'.format(obj.targetdropdate*100)     


    @admin.display(ordering="estimatemonthlyppl",description='预估月开票人份数')
    def estimatemonthlyppl_display(self, obj):
        return obj.estimatemonthlyppl




@admin.register(ATMenu)  
class ATMenuAdmin(GlobalAdmin):   
    search_fields=['brand','product','supplier']
    exclude = ('id','createtime','updatetime','is_active')
    
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            username = request.user.username
            project_name = 'AT'

            existed_redis_data = cache.get(username) #找到的结果可能是{'PZX': {'object_id': '10'}, 'AT': {'object_id': '2'}}
            if existed_redis_data:
                print(existed_redis_data,'class ATMenuAdmin(GlobalAdmin): ~~~~~~~~~~~~~~~')
                selected_id = existed_redis_data[project_name]['object_id']
                print('selected_id',selected_id)
                queryset=queryset.filter(is_active=True,overallid=int(selected_id)).order_by('id')
                print('queryset搜索完成')
            else:
                queryset=queryset.filter(is_active=True).order_by('id')
        return queryset,use_distinct 
    





@admin.register(ATOverallDELETE)
class ATOverallDELETEAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime','is_active','operator')
    search_fields=['department','project']
    list_filter = ['department','semidepartment','project','supplier']
    empty_value_display = '--'
    list_per_page = 10
    list_display = ('semidepartment','project','supplier')#'display_purchasesum','display_purchasesumpercent','display_theoreticalvalue','display_theoreticalgp', 'display_theoreticalgppercent',
    #                 'display_supplier','display_supplierpurchasesum','display_purchasesumpercentinproject','display_suppliertheoreticalvalue','display_suppliertheoreticalgp','display_suppliertheoreticalgppercent',                   
    #                 'relation','display_actionplan','whygrowth','display_progress','display_support',
    #                 'completemonth','monthgpgrowthdetail','thisyeargpgrowthdetail')#'display_monthgpgrowth',,'display_thisyeargpgrowth')
    ordering = ('id',)
    readonly_fields =  ('thisyeargpgrowth','progress','support','monthgpgrowth', 'completemonth',
                        'supplier','monthgpgrowthdetail','thisyeargpgrowthdetail','actionplan','relation',
                        'purchasesum','purchasesumpercent','theoreticalvalue','theoreticalgp','theoreticalgppercent',
                        'supplierpurchasesum','purchasesumpercentinproject','suppliertheoreticalvalue',
                        'suppliertheoreticalgp','suppliertheoreticalgppercent',
                        )
    
    # fieldsets = (('作战背景', {'fields': ('company','salesman','department','semidepartment','project',
    #                                   'field_purchasesum','field_purchasesumpercent','field_theoreticalvalue','field_theoreticalgp','field_theoreticalgppercent',
    #                                   'supplier','field_supplierpurchasesum','field_purchasesumpercentinproject','field_suppliertheoreticalvalue',
    #                                   'field_suppliertheoreticalgp','field_suppliertheoreticalgppercent',
    #                                 'relation','actionplan','whygrowth','progress','support','completemonth','monthgpgrowthdetail','monthgpgrowth',
    #                                 'thisyeargpgrowthdetail','thisyeargpgrowth'),
    #                         'classes': ('wide','extrapretty',),
    #                         'description': format_html(
    #         '<span style="color:{};font-size:13.0pt;">{}</span>','blue','注意：项目大类和增量来源是必填项。如增量来源选择多项，请在下方补充对应选项的进度和明细')}),
    #     )
    view_group_list = ['boss','AT','allviewonly','JConlyview']



 #只显示未被假删除的项目
    #------get_queryset-----------查询-------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser :
            return qs.filter(is_active=False,company_id=9)

        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=False,company_id=9)
            

    #````````````
    def has_delete_permission(self, request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        #配置恢复权限
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] == 'allviewonly' or request.user.groups.values()[0]['name'] =='JConlyview' :
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
            # print(i.atnewprojectstatusdelete_set.all())
            i.atnewprojectstatusdelete_set.all().update(is_active=True)
            for j in i.atnewprojectstatusdelete_set.all():
                if hasattr(j, 'ATnewprojectdetaildelete_set'):
                    j.atnewprojectdetaildelete_set.all().update(is_active=True)

            i.atnegotiationstatusdelete_set.all().update(is_active=True)
            for j in i.atnegotiationstatusdelete_set.all():
                # print('~~~~~!',j)
                # print('all',j.atnegotiationdetaildelete_set.all())
                if hasattr(j, 'atnegotiationdetaildelete_set'):
                    # print("~~~~~hasattratnegotiationdetaildelete", j.atnegotiationdetaildelete_set.all())
                    j.atnegotiationdetaildelete_set.all().update(is_active=True)

            i.atchangechannelstatusdelete_set.all().update(is_active=True)
            for j in i.atchangechannelstatusdelete_set.all():
                # print('~~~~~~',j)
                if hasattr(j, 'atchangechanneldetaildelete_set'):
                    # print("~~~~~", j.ATchangechanneldetaildelete_set.all())
                    j.atchangechanneldetaildelete_set.all().update(is_active=True)

            i.atchangebrandstatusdelete_set.all().update(is_active=True)
            
            for j in i.atchangebrandstatusdelete_set.all():
                if hasattr(j, 'atchangebranddetaildelete_set'):
                    j.atchangebranddetaildelete_set.all().update(is_active=True)

            i.atsetstatusdelete_set.all().update(is_active=True)
            for j in i.atsetstatusdelete_set.all():
                if hasattr(j, 'atsetdetaildelete_set'):
                    j.atsetdetaildelete_set.all().update(is_active=True)

            if hasattr(i, 'atcalculatedelete'):
                i.atcalculatedelete.is_active=True
                i.atcalculatedelete.save()  
            print('恢复') 
            i.operator=request.user
            i.save()           
        queryset.update(is_active=True)
        print('queryset已update')

    restore.short_description = "恢复数据至调研列表" 
    restore.type = 'info'
    restore.style = 'color:white;'





