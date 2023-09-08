
from django.contrib import admin
from PMRKA.models import *
from PMRKA.models_delete import *

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
from django.db.models import Avg,Sum,Count,Max,Min
import textwrap

from django.contrib.admin import SimpleListFilter
from django.db.models import Case, When, Value, IntegerField


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



#----------------------FORM-----------------------------------------------------------------------
class PMRResearchDetailPMRKAInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    class Meta: 
            model = PMRResearchDetailPMRKA
            exclude = ['id']
            widgets = {                
                'brand': AutocompleteSelect(
                    model._meta.get_field('brand'),
                    admin.site,
                    attrs={'style': 'width: 18ch'}),
                'department': forms.TextInput(attrs={'size':'6'}),
                'product': forms.TextInput(attrs={'size':'24'}),
                'machinemodel': forms.TextInput(attrs={'size':'24'}),
                'supplier': forms.TextInput(attrs={'size':'6'}),
                'relation': forms.TextInput(attrs={'size':'6'}),
                'adminmemo': forms.TextInput(attrs={'size':'6'}),

                'machinenumber' : forms.NumberInput(attrs={
                    'style': 'width:6ch'
                }),
                'testsperday' : forms.NumberInput(attrs={
                    'style': 'width:8ch'
                }),
                'salestotal' : forms.NumberInput(attrs={
                    'style': 'width:10ch'
                }),
                
            }



###------------------INLINE------------------------------------------------------------------------------------------------------------

class SalesmanPositionPMRKAInline(admin.TabularInline):
    model = SalesmanPositionPMRKA
    fk_name = "user"
    extra = 0
    fields=['user','company','position'] 
    verbose_name = verbose_name_plural = ('员工职位列表')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Company.objects.filter(is_active=True)    
        return super(SalesmanPositionPMRKAInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    

class SalesmanPositionPMRKAInline2(admin.TabularInline):
    model = SalesmanPositionPMRKA
    fk_name = "company"
    extra = 0
    fields=['user','company','position'] 
    verbose_name = verbose_name_plural = ('员工职位列表')



class PMRResearchDetailPMRKAInline(admin.TabularInline):
    form=PMRResearchDetailPMRKAInlineForm
    model = PMRResearchDetailPMRKA
    fk_name = "researchlist"
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 
    fields=('brand','ownbusiness','department','product','machinemodel','machinenumber','installdate','testsperday','salestotal','supplier','relation','adminmemo',) 
    autocomplete_fields=['brand']
    verbose_name = verbose_name_plural = ('调研详情表')
    PMRKA_view_group_list = ['boss','pmrmanager','allviewonly','pmrdirectsales']

    #在inline中显示isactive的detail的表
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print('我在PMRResearchDetailPMRKAInline-get_queryset')
        if request.user.is_superuser :
            print('我在PMRResearchDetailPMRKAInline-get_queryset-筛选active的')
            return qs.filter(is_active=True)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.PMRKA_view_group_list:
                return qs.filter(is_active=True)
            
       #普通销售的话:
        return qs.filter(Q(is_active=True)&Q(researchlist__salesman=request.user))




    def has_add_permission(self,request,obj):
        print('我在PMRResearchDetailPMRKAInlinehas add permission:::obj',obj,request.user) 
        if obj==None:
            if request.POST.get('salesman'):                
                if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                    return True
                elif request.POST.get('salesman')!= str(request.user.id) :
                    print('我在PMRResearchDetailPMRKAInlinehas add permission:: :obj==None FALSE request.POST.get(salesman)',request.POST.get('salesman'),request.user)
                    return False
                else:
                    return True
            else:    
                print('我在PMRResearchDetailPMRKAInlinehas add permission:: obj==None True 没有request.POST.get(salesman)')
                return True

        else:    
            if request.user.is_superuser or obj.salesman==request.user  or request.POST.get('salesman')==str(request.user.id) or request.user.groups.values()[0]['name'] =='boss':
                print('我在inline has add permission:::,obj.salesman if ',True)
                return True
            else:
                print('我在inline has add permission:::,obj.salesman else',False)
                return False

    def has_change_permission(self,request, obj=None):
        print('我在PMRResearchDetailPMRKAInlinehas change permission:: obj',obj)
        if obj==None:
                print('我在PMRResearchDetailPMRKAInlinehas change permission:::obj,request.POST.get(salesman)',True,request.POST.get('salesman'))
                return True            
        elif obj.salesman==request.user  or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            print('我在PMRResearchDetailPMRKAInlinehas change permission:::obj',True,obj.salesman)
            return True
        else:
            print('我在PMRResearchDetailPMRKAInlinehas change permission:::obj',False)
            return False

    def has_delete_permission(self,request, obj=None):
        print('我在inline has_delete_permission:::obj',obj)        
        return True
    




###------------------ADMIN-----------------------------------------------------------------------------------------------------------------------------------

@admin.register(UserInfoPMRKA)  
class UserInfoPMRKAAdmin(UserAdmin):  
        
    inlines=[SalesmanPositionPMRKAInline]
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
 

@admin.register(SalesmanPositionPMRKA)  
class SalesmanPositionPMRKAAdmin(GlobalAdmin):   
    exclude = ('id','createtime','updatetime')

    # 外键company只显示active的  定死普美瑞
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['adminform'].form.fields['company'].queryset = Company.objects.filter(is_active=True)
        return super(SalesmanPositionPMRKAAdmin, self).render_change_form(request, context, add, change, form_url, obj)


@admin.register(Company)  
class CompanyAdmin(GlobalAdmin):   
    inlines=[SalesmanPositionPMRKAInline2]
    exclude = ('id','createtime','updatetime','is_active')

 


@admin.register(PMRResearchListPMRKA)
class PMRResearchListPMRKAAdmin(GlobalAdmin):
    # form=GSMRResearchListForm
    inlines=[PMRResearchDetailPMRKAInline]
    empty_value_display = '--'
    list_display_links =('hospital',)
    exclude = ('operator','is_active')
    list_per_page = 10
 
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 37})}
    } 
    autocomplete_fields=['hospital']       
    ordering = ('id',)
        
    list_filter = ['hospital__district','hospital__hospitalclass','newold']
    search_fields = ['hospital__hospitalname','pmrresearchdetailpmrka__brand__brand','hospital__hospitalclass','hospital__district','pmrresearchdetailpmrka__machinemodel']
    fields = ('company','hospital','salesman','machinenumber','testspermonth','salestotal')

    list_display = ('hospital','display_brand','display_department','display_product','machinenumber','ownmachinenumber','display_ownmachinenumberpercent','testspermonth','owntestspermonth','display_owntestspermonthpercent','salestotal','ownsalestotal','display_ownsalestotalpercent')

    readonly_fields =  ('machinenumber', 'testspermonth','salestotal')
    PMRKA_view_group_list = ['boss','pmrmanager','allviewonly','pmrdirectsales']


    # 新增或修改数据时，设置外键可选值，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company': 
            kwargs["queryset"] = Company.objects.filter(is_active=True,id=1) 
        if db_field.name == 'hospital': 
            kwargs["queryset"] = Hospital.objects.filter(is_active=True) 

        if db_field.name == 'salesman': 
            kwargs["queryset"] = UserInfo.objects.filter(Q(is_active=True) & Q(username__in= ['fzj']))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    
    def has_delete_permission(self, request,obj=None):
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] == 'allviewonly':
                return False
            
        if obj==None:
            return True
        
        if request.POST.get('salesman'):
            if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                return True
            if request.POST.get('salesman')!=str(request.user.id) :
                return False
            else: 
                return True
        if obj.salesman==request.user or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            return True

        else:
            return False
        

    def has_change_permission(self,request, obj=None):
        if request.user.groups.values():
            if  request.user.groups.values()[0]['name'] == 'allviewonly':
                return False
        if obj==None:
            return True
        if request.POST.get('salesman'):
            if request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman)  True superuser!!!')
                return True
            if request.POST.get('salesman')!=str(request.user.id):
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman)  false!!!',request.POST.get('salesman'))
                return False
            else: 
                print('我在PmrResearchListAdmin has change permission request.POST.get(salesman)  true!!',request.POST.get('salesman'))
                return True
        if obj.salesman==request.user  or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss':
            print('我在PmrResearchListAdmin has change permission True obj.salesman ',obj.salesman)
            return True
        else:
            print('我在PmrResearchListAdmin has change permission else else else',False)
            return False


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
        qs = super(PMRResearchListPMRKAAdmin, self).get_queryset(request)
    
        if request.user.is_superuser :
            # print('我在PMRResearchListAdmin-get_queryset-筛选active的')            
            return qs.filter(is_active=True,company_id=1)
                
        user_in_group_list = request.user.groups.values('name')
        # print(user_in_group_list)
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.PMRKA_view_group_list:
                 # print('我在模型里')
                return qs.filter(is_active=True,company_id=1)
            
       #普通销售的话:
        return qs.filter(Q(is_active=True)&Q(salesman=request.user)&Q(company_id=1))
                      

# ------delete_model内层的红色删除键------------------------------
    def delete_model(self, request, obj):
        print('我在LISTADMIN delete_model')
        if request.user.is_superuser or obj.salesman==request.user or request.user.groups.values()[0]['name'] =='boss':             
            obj.is_active = False 
            obj.pmrresearchdetailpmrka_set.all().update(is_active=False)
            obj.operator=request.user   
            obj.save()


    def delete_queryset(self,request, queryset):        
            print('我在delete_queryset')
            for delete_obj in queryset:     
                print('delete_queryset delete_obj',delete_obj)                    
                if request.user.is_superuser or delete_obj.salesman==request.user or request.user.groups.values()[0]['name'] =='boss':     
                    delete_obj.is_active=False
                    print('list 已假删')
                    delete_obj.pmrresearchdetailpmrka_set.all().update(is_active=False)
                    delete_obj.operator=request.user
                    delete_obj.save()


    def save_model(self, request, obj, form, change):
        obj.operator = request.user
        super().save_model(request, obj, form, change)



    def save_related(self, request, form, formsets, change): 
        ###注意要判断是否共用仪器！！！！！！！如果我司仪器必填序列号，怎么validate？？？！？
        print('我在save_related')
        super().save_related(request, form, formsets, change)
        if form.cleaned_data.get('salesman')==request.user or request.user.is_superuser or request.user.groups.values()[0]['name'] =='boss': 
            machine_total_number=0
            machine_own_number=0

            totaltests=0
            owntests=0

            salestotal=0
            ownsalestotal=0

            brandscombine=[]
            suppliercombine=[]
            relationcombine=[]
            departmentcombine=[]
            productcombine=[]

            new_or_old_list=[]
            if len(formsets[0].cleaned_data) > 0:
                #formsets[1]是仪器详情表，显示inline的行数，删除的行也计算在内
                # print(len(formsets[1].cleaned_data))
                for each_inline in formsets[0].cleaned_data:
                    #循环列表中每一个字典，一个字典就是一行具体的数据
                        #是否我司业务不为空 且  没有被删除  且 仪器数量不为0         
                    print('each_inline',each_inline)  
                    # print(type(each_inline.get('id')))     
                    if  each_inline.get('DELETE')==False and each_inline.get('machinenumber')!=0:
                        machine_total_number += each_inline['machinenumber']  
                        totaltests += each_inline['testsperday'] *30
                        salestotal += each_inline['salestotal'] 

                        brandscombine.append(each_inline['brand'].brand)
                        suppliercombine.append(each_inline['supplier'])
                        departmentcombine.append(each_inline['department'])
                        relationcombine.append(each_inline['relation'])
                        productcombine.append(each_inline['product'])
                        new_or_old_list.append(str(each_inline['ownbusiness']))

                        if each_inline['ownbusiness']==True:
                            machine_own_number += each_inline['machinenumber']
                            owntests += each_inline['testsperday']*30 
                            ownsalestotal += each_inline['salestotal']

            if 'True' in new_or_old_list:
                newold='已有业务'
            else:
                newold='新商机'

            if machine_total_number == 0 or machine_own_number ==0:
                ownmachinepercent = 0
            else:
                ownmachinepercent= machine_own_number/machine_total_number

            if totaltests == 0 or owntests ==0:
                owntestspercent = 0
            else:
                owntestspercent= owntests/totaltests

            if salestotal == 0 or ownsalestotal ==0:
                ownsalestotalpercent = 0
            else:
                ownsalestotalpercent= ownsalestotal/salestotal



            #如果有（老数据修改），则以更新的方式
            if PMRResearchListPMRKA.objects.filter(id=form.instance.id):
                a=PMRResearchListPMRKA.objects.get(id=form.instance.id)
                # print(a)
                a.machinenumber=machine_total_number
                a.ownmachinenumber=machine_own_number
                a.ownmachinenumberpercent=ownmachinepercent
                a.newold=newold
                a.brand='|'.join(str(i) for i in brandscombine)
                a.supplier='|'.join(str(i) for i in suppliercombine)
                a.department='|'.join(str(i) for i in departmentcombine)
                a.relation='|'.join(str(i) for i in relationcombine)
                a.product='|'.join(str(i) for i in productcombine)

                a.testspermonth=totaltests
                a.owntestspermonth=owntests
                a.owntestspermonthpercent=owntestspercent

                a.salestotal=salestotal
                a.ownsalestotal=ownsalestotal
                a.ownsalestotalpercent =ownsalestotalpercent

                a.is_active=True
                a.save()

            for eachdetail in PMRResearchDetailPMRKA.objects.filter(researchlist_id=form.instance.id):
                # print('eachdetail',eachdetail)
                if not eachdetail.installdate:
                    ret = '--'
                else:
                    if (datetime.now().date() - eachdetail.installdate).days >= 1825:
                        ret = '已超5年'
                    else:
                        ret = '5年内'      
                eachdetail.expiration=ret
                eachdetail.save()

            print('saverelated 保存成功')
   
              

    @admin.display(ordering="-hospital__district", description='地区') 
    def hospital_district(self, obj):
        return obj.hospital.district
    
    @admin.display(ordering="hospital__hospitalclass",description='级别')
    def hospital_hospitalclass(self, obj):
        return obj.hospital.hospitalclass

    @admin.display(ordering="salesman__chinesename",description='责任人')
    def salesman_chinesename(self, obj):
        return obj.salesman.chinesename


    @admin.display(ordering="ownmachinenumber",description='我司仪器占比')
    def display_ownmachinenumberpercent(self, obj):
        if obj.ownmachinenumberpercent == 0 or not obj.ownmachinenumberpercent:
            return '--'
        else:
          return '{:.1f}%'.format(obj.ownmachinenumberpercent*100)
    

    @admin.display(ordering="owntestspermonth",description='我司测试数占比')
    def display_owntestspermonthpercent(self, obj):
        if obj.owntestspermonthpercent == 0 or not obj.owntestspermonthpercent:
            return '--'
        else:
            return '{:.1f}%'.format(obj.owntestspermonthpercent*100)


    @admin.display(ordering="ownsalestotal",description='我司开票占比')
    def display_ownsalestotalpercent(self, obj):
        if obj.ownsalestotalpercent == 0 or not obj.ownsalestotalpercent:
            return '--'
        else:
            return '{:.1f}%'.format(obj.ownsalestotalpercent*100)


    @admin.display(ordering="brand",description='品牌')
    def display_brand(self, obj):
        if obj.brand:
            name=obj.brand
        else:
            name='--'  
        wrapped_name = textwrap.fill(name, width=10)
        return  format_html('<div style="width:100px;">{}</div>', wrapped_name) 

    @admin.display(ordering="department",description='科室')
    def display_department(self, obj):
        if obj.department:
            name=obj.department
        else:
            name='--'  
        wrapped_name = textwrap.fill(name, width=10)
        return  format_html('<div style="width:100px;">{}</div>', wrapped_name) 


    @admin.display(ordering="product",description='产品')
    def display_product(self, obj):
        if obj.product:
            name=obj.product
        else:
            name='--'  
        wrapped_name = textwrap.fill(name, width=10)
        return  format_html('<div style="width:100px;">{}</div>', wrapped_name) 


 #新增动作————统计按钮
    
    actions = ['calculate']
    def calculate(self, request, queryset):
        for i in queryset:
            #更新是新客户还是老客户
            if i.pmrresearchdetailpmrka_set.filter(Q(is_active=True)&Q(ownbusiness=True) & ~Q(machinenumber='0')) :
                i.newold='已有业务'
            else:
                i.newold='新商机'
            
            
            #更新仪器总数量
            machinetotalqty= i.pmrresearchdetailpmrka_set.filter(is_active=True).aggregate(sumsum=Sum("machinenumber"))['sumsum']  
            if not machinetotalqty:
                machinetotalret=0
            else:
                machinetotalret=machinetotalqty
            i.machinenumber=machinetotalret


            #更新我司仪器数    
            machineqtyown= i.pmrresearchdetailpmrka_set.filter(Q(is_active=True) & Q(ownbusiness=True)).aggregate(sumsum=Sum("machinenumber"))['sumsum']
            # print('machineqtyown',machineqtyown)
            if not machineqtyown:
                machineownret=0
            else:
                machineownret=machineqtyown
            i.ownmachinenumber=machineownret

            #更新我司仪器占比     
            if  machinetotalret ==0:
                ownmachinenumberpercentret=0
            else:
                ownmachinenumberpercentret=machineownret/machinetotalret
            i.ownmachinenumberpercent=ownmachinenumberpercentret

            #---------------
            #更新测试总数量
            totaltestspermonth= i.pmrresearchdetailpmrka_set.filter(is_active=True).aggregate(sumsum=Sum("testsperday"))['sumsum']
            if not totaltestspermonth:
                totaltestspermonthret=0
            else:
                totaltestspermonthret=totaltestspermonth*30
            i.testspermonth=totaltestspermonthret

            #更新我司测试  
            owntestspermonth= i.pmrresearchdetailpmrka_set.filter(Q(is_active=True) & Q(ownbusiness=True)).aggregate(sumsum=Sum("testsperday"))['sumsum']
            if not owntestspermonth:
                owntestspermonthret=0
            else:
                owntestspermonthret=owntestspermonth *30
            i.owntestspermonth=owntestspermonthret

            #更新我司测试占比     
            if  totaltestspermonthret ==0:
                owntestspermonthpercentret=0
            else:
                owntestspermonthpercentret=owntestspermonthret/totaltestspermonthret
            i.owntestspermonthpercent=owntestspermonthpercentret

        
            #---------------
            #更新sum量
            salestotal= i.pmrresearchdetailpmrka_set.filter(is_active=True).aggregate(sumsum=Sum("salestotal"))['sumsum']    
            if not salestotal:
                salestotalret=0
            else:
                salestotalret=salestotal
            i.salestotal=salestotalret

            #更新我司sum   
            ownsalestotal= i.pmrresearchdetailpmrka_set.filter(Q(is_active=True) & Q(ownbusiness=True)).aggregate(sumsum=Sum("salestotal"))['sumsum']  
            if not ownsalestotal:
                ownsalestotalret=0
            else:
                ownsalestotalret=ownsalestotal
            i.ownsalestotal=ownsalestotalret

            #更新我司sum占比     
            if  salestotalret ==0:
                ownsalestotalcentret=0
            else:
                ownsalestotalcentret=ownsalestotalret/salestotalret
            i.ownsalestotalcent=ownsalestotalcentret


            #---------------
            #更新品牌集合在detailcalculate表中brandscombine
            brands= i.pmrresearchdetailpmrka_set.filter(is_active=True)
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
            i.brand=ret
            

            #更新科室集合
            departments= i.pmrresearchdetailpmrka_set.filter(is_active=True)
            if not departments:
                ret = '--'
            elif len(departments)>1:
                ret = '|'.join(str(i.department) for i in departments if i.machinenumber != 0)               
            else:
                if departments[0].machinenumber != 0:
                    ret=str(departments[0].department)
                else:
                    ret='--'
            i.department=ret

            #更新产品集合
            products= i.pmrresearchdetailpmrka_set.filter(is_active=True)
            if not products:
                ret = '--'
            elif len(products)>1:
                ret = '|'.join(str(i.product) for i in products if i.machinenumber != 0)               
            else:
                if products[0].machinenumber != 0:
                    ret=str(products[0].product)
                else:
                    ret='--'
            i.product=ret

            #更新关系点集合
            relations= i.pmrresearchdetailpmrka_set.filter(is_active=True)
            if not relations:
                ret = '--'
            elif len(relations)>1:
                ret = '|'.join(str(i.relation) for i in relations if i.machinenumber != 0)               
            else:
                if relations[0].machinenumber != 0:
                    ret=str(relations[0].relation)
                else:
                    ret='--'
            i.relation=ret

            #更新供应商集合
            suppliers= i.pmrresearchdetailpmrka_set.filter(is_active=True)
            if not suppliers:
                ret = '--'
            elif len(suppliers)>1:
                ret = '|'.join(str(i.supplier) for i in suppliers if i.machinenumber != 0)               
            else:
                if suppliers[0].machinenumber != 0:
                    ret=str(suppliers[0].supplier)
                else:
                    ret='--'
            i.supplier=ret


            i.save()


            #更新装机时间在detail表中
            qs_fk=i.pmrresearchdetailpmrka_set.all()
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
             


    calculate.short_description = "统计" 
    calculate.type = 'info'
    calculate.style = 'color:white;'







@admin.register(PMRResearchDetailPMRKA)
class PMRResearchDetailPMRKAAdmin(GlobalAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=['researchlist__hospital__hospitalname','brand__brand']
    list_filter = ['researchlist__hospital__district','researchlist__hospital__hospitalclass','expiration']

    list_display_links =('list_hospitalname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('list_district','list_hospitalname','list_hospitalclass','list_salesman',
                  'brand','ownbusiness','department','product','machinemodel','machinenumber','installdate','colored_expiration',
                  'testsperday','salestotal','supplier','relation','adminmemo'
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
                'researchlist__hospital__hospitalname','researchlist__salesman',)
    
    PMRKA_view_group_list = ['boss','pmrmanager','allviewonly','pmrdirectsales']


    def get_actions(self, request):
        actions = super(PMRResearchDetailPMRKAAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions



    #只显示未被假删除的项目
    #------get_queryset-----------查询-------------------
    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的服务器"""
        qs = super(PMRResearchDetailPMRKAAdmin, self).get_queryset(request)
        print('我在PMRResearchDetailAdmin-get_queryset')
        #通过外键连list中的负责人名称
        if request.user.is_superuser :
            return qs.filter(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__company_id=1))
        
                
        # <QuerySet [{'name': 'pmrdirectsales'}, {'name': 'QTmanager'}]>
        user_in_group_list = request.user.groups.values('name')
        print(user_in_group_list)
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.PMRKA_view_group_list:
                 # print('我在模型里')
                return qs.filter(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__company_id=1))            
        
        #detail active ,list active 同时人员是自己
        return qs.filter(Q(is_active=True) & Q(researchlist__is_active=True)&Q(researchlist__salesman=request.user)&Q(researchlist__company_id=1))

        

    #用来控制list表中的inline的删除权限??????????????
    def has_delete_permission(self, request,obj=None):
        if obj==None:
            return True
        if request.user.is_superuser: 
            print('我在PmrResearchDETAILAdmin has delete permission: SUPERUSER ',super().has_delete_permission(request, obj))
            return super().has_delete_permission(request, obj)      
        elif obj.researchlist.salesman==request.user or request.user.groups.values()[0]['name'] =='boss':          
            print('我在PmrResearchDETAILAdmin has delete permission:ELIF obj.salesman',obj.researchlist.salesman)
            return True  
       
        else:
            print('我在PmrResearchDETAILAdmin has delete permission:else')
            return False   
    
    #控制detail详情表中点进去后的红色删除
    def delete_model(self, request, obj):
        print('我在DETAILADMIN delete_model,, obj.researchlist.salesman',obj.researchlist.salesman)
        if request.user.is_superuser or obj.researchlist.salesman==request.user or request.user.groups.values()[0]['name'] =='boss':   
            # print('delete_model detail 已假删')          
            obj.is_active = False 
            obj.researchlist.operator=request.user
            obj.save()


    #一下变化，在list的inline中有体现，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'researchlist': 
            kwargs["queryset"] = PMRResearchListPMRKA.objects.filter(is_active=True) 
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
    


    @admin.display(ordering="researchlist__salesman",description='负责人')
    def list_salesman(self, obj): #用relatedname
        return obj.researchlist.salesman.chinesename
    



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
    




@admin.register(PMRResearchListPMRKADELETE)
class PMRResearchListPMRKADELETEAdmin(admin.ModelAdmin):

    empty_value_display = '--'
    # list_display_links =('hospital',)
    exclude = ('operator','is_active')
    readonly_fields=('company','hospital','salesman',)
    search_fields=['hospital']

    PMRKA_view_group_list = ['boss','pmrmanager','allviewonly','pmrdirectsales']

    def get_queryset(self, request):
        qs = super(PMRResearchListPMRKADELETEAdmin,self).get_queryset(request)
  
        if request.user.is_superuser :
            print('我在PMRResearchListAdmin-get_queryset-筛选active的')        
            return qs.filter(is_active=False,company_id=1)
        
        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.PMRKA_view_group_list:
                return qs.filter(is_active=False,company_id=1)      

       #普通销售的话:
        return qs.filter(Q(is_active=False)&Q(salesman=request.user)&Q(company_id=1))
    

    def has_delete_permission(self, request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request):
        return False

    def get_actions(self, request):
        actions = super(PMRResearchListPMRKADELETEAdmin, self).get_actions(request)

        #配置恢复权限
        if request.user.groups.values():
            if request.user.groups.values()[0]['name'] == 'pmronlyview'  or request.user.groups.values()[0]['name'] == 'allviewonly':
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
            i.pmrresearchdetailpmrkadelete_set.all().update(is_active=True)
            print('恢复') 
            i.save()           
        queryset.update(is_active=True)
        print('queryset已update')

    restore.short_description = "恢复数据至调研列表" 
    restore.type = 'info'
    restore.style = 'color:white;'
