from django.contrib import admin

# Register your models here.
from django.contrib import admin
from NANXIANG.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from django.db.models import Q


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
    



@admin.register(NXUserInfo)  
class NXUserAdmin(UserAdmin):  
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



@admin.register(NXSPDList)
class NXSPDListAdmin(GlobalAdmin):
    exclude = ('id','createtime','updatetime','is_active','operator')
    search_fields=['supplier','brand']
    # list_filter = ['hospital__district','hospital__hospitalclass','jcornot']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 10
    list_display = ('salesman_chinesename','supplier','brand','department','product','machinemodel','listotal_formatted','salestotal_formatted','display_salestotalpercent','purchasetotal_formatted','display_gppercent','relation',
                    )
    ordering = ('id',)
    view_group_list = ['boss','NX','allviewonly','JConlyview']

    # 新增或修改数据时，设置外键可选值，
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company': 
            kwargs["queryset"] = Company.objects.filter(is_active=True,id=10) 
        if db_field.name == 'salesman': 
            kwargs["queryset"] = UserInfo.objects.filter(Q(is_active=True) & Q(username__in= ['zxl']))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ------delete_model内层的红色删除键------------------------------
    def delete_model(self, request, obj):
        print('NX delete_model')
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
            return qs.filter(is_active=True,company_id=10)

        user_in_group_list = request.user.groups.values('name')
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in self.view_group_list:
                return qs.filter(is_active=True,company_id=10)

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