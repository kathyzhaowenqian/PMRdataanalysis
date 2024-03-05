from django.contrib import admin
from Suppliers.models import *
# Register your models here.
import textwrap

@admin.register(SupplierInfo)  
class SupplierInfoAdmin(admin.ModelAdmin):   
    search_fields=['supplier']
    exclude = ('id','createtime','updatetime','is_active')
    list_display = ('supplier','contact','payterm','tax','delivery','project',)
    ordering = ('project','supplier')
    list_filter = ['project','supplier']
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            queryset=queryset.filter(is_active=True).order_by('id')
        return queryset,use_distinct 

#徐二院=================================================================
class XEY_Supplier_Product_SummaryInline(admin.TabularInline):
    model = XEY_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('徐二院供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(XEY_Supplier_Rank)
class XEY_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[XEY_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(XEY_Supplier_Product_Summary)
class XEY_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    

@admin.register(XEY_Product_Rank)
class XEY_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec



#南桥=================================================================
class NQ_Supplier_Product_SummaryInline(admin.TabularInline):
    model = NQ_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('南桥供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(NQ_Supplier_Rank)
class NQ_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[NQ_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(NQ_Supplier_Product_Summary)
class NQ_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(NQ_Product_Rank)
class NQ_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec






#普中心=================================================================
class PZX_Supplier_Product_SummaryInline(admin.TabularInline):
    model = PZX_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('普中心供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(PZX_Supplier_Rank)
class PZX_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[PZX_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(PZX_Supplier_Product_Summary)
class PZX_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(PZX_Product_Rank)
class PZX_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec






#新沂=================================================================
class XINYI_Supplier_Product_SummaryInline(admin.TabularInline):
    model = XINYI_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('新沂供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(XINYI_Supplier_Rank)
class XINYI_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[XINYI_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(XINYI_Supplier_Product_Summary)
class XINYI_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(XINYI_Product_Rank)
class XINYI_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec



#邳州=================================================================
class PIZHOU_Supplier_Product_SummaryInline(admin.TabularInline):
    model = PIZHOU_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('邳州供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(PIZHOU_Supplier_Rank)
class PIZHOU_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[PIZHOU_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(PIZHOU_Supplier_Product_Summary)
class PIZHOU_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(PIZHOU_Product_Rank)
class PIZHOU_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec






#安亭=================================================================
class ANTING_Supplier_Product_SummaryInline(admin.TabularInline):
    model = ANTING_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('安亭供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(ANTING_Supplier_Rank)
class ANTING_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[ANTING_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(ANTING_Supplier_Product_Summary)
class ANTING_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(ANTING_Product_Rank)
class ANTING_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec


#南翔=================================================================
class NANXIANG_Supplier_Product_SummaryInline(admin.TabularInline):
    model = NANXIANG_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('南翔供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(NANXIANG_Supplier_Rank)
class NANXIANG_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[NANXIANG_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(NANXIANG_Supplier_Product_Summary)
class NANXIANG_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(NANXIANG_Product_Rank)
class NANXIANG_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec





#齐贤=================================================================
class QIXIAN_Supplier_Product_SummaryInline(admin.TabularInline):
    model = QIXIAN_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('齐贤供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(QIXIAN_Supplier_Rank)
class QIXIAN_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[QIXIAN_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(QIXIAN_Supplier_Product_Summary)
class QIXIAN_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(QIXIAN_Product_Rank)
class QIXIAN_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec



#申养=================================================================
class SHENYANG_Supplier_Product_SummaryInline(admin.TabularInline):
    model = SHENYANG_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('申养供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(SHENYANG_Supplier_Rank)
class SHENYANG_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[SHENYANG_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(SHENYANG_Supplier_Product_Summary)
class SHENYANG_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(SHENYANG_Product_Rank)
class SHENYANG_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec

#四团=================================================================
class SITUAN_Supplier_Product_SummaryInline(admin.TabularInline):
    model = SITUAN_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('四团供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(SITUAN_Supplier_Rank)
class SITUAN_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[SITUAN_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(SITUAN_Supplier_Product_Summary)
class SITUAN_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(SITUAN_Product_Rank)
class SITUAN_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec

#四五五=================================================================
class SIWUWU_Supplier_Product_SummaryInline(admin.TabularInline):
    model = SIWUWU_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('四五五供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(SIWUWU_Supplier_Rank)
class SIWUWU_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[SIWUWU_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(SIWUWU_Supplier_Product_Summary)
class SIWUWU_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(SIWUWU_Product_Rank)
class SIWUWU_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec

#亭林=================================================================
class TINGLIN_Supplier_Product_SummaryInline(admin.TabularInline):
    model = TINGLIN_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('亭林供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(TINGLIN_Supplier_Rank)
class TINGLIN_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[TINGLIN_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    list_filter = ['supplier']
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(TINGLIN_Supplier_Product_Summary)
class TINGLIN_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(TINGLIN_Product_Rank)
class TINGLIN_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec

#西渡=================================================================
class XIDU_Supplier_Product_SummaryInline(admin.TabularInline):
    model = XIDU_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('西渡供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(XIDU_Supplier_Rank)
class XIDU_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[XIDU_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    list_filter = ['supplier']
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(XIDU_Supplier_Product_Summary)
class XIDU_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(XIDU_Product_Rank)
class XIDU_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec

#直销===c==============================================================
class ZHIXIAO_Supplier_Product_SummaryInline(admin.TabularInline):
    model = ZHIXIAO_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    readonly_fields= ('rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum')
    fields=['rank','productcode','productname','field_spec','unit','brand', 'recentdate','price','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('直销供应商销量明细')

    def field_spec(self, obj):
        value = obj.spec if obj.spec else '--'
        style = 'width: 15ch'
        return format_html('<div style="{}">{}</div>', style, value)
    field_spec.short_description = '规格'

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
@admin.register(ZHIXIAO_Supplier_Rank)
class ZHIXIAO_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[ZHIXIAO_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)

    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(ZHIXIAO_Supplier_Product_Summary)
class ZHIXIAO_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname')
    readonly_fields = ('supplierrank','project','rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
@admin.register(ZHIXIAO_Product_Rank)
class ZHIXIAO_Product_RankAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','productcode','productname','display_spec','unit','supplier','brand', 'recentdate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec

#=======total
    
@admin.register(Total_Supplier_Rank)
class TOTAL_Supplier_RankAdmin(admin.ModelAdmin):
    search_fields=('supplier',)
    readonly_fields= ('project','rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','project','supplier','display_qty21','display_qty22','display_qty23','display_qty24','display_totalqty','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    list_filter = ['project','supplier']
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="rank",description='排行')
    def display_rank(self, obj):
        wrapped_name = textwrap.fill(obj.rank, width=5)
        return  format_html('<div style="width:5px;">{}</div>', wrapped_name) 

    @admin.display(ordering="qty21",description=format_html('21年数量'))
    def display_qty21(self, obj):
        return  '{:,.0f}'.format(obj.qty21)

    @admin.display(ordering="qty22",description=format_html('22年数量'))
    def display_qty22(self, obj):
        return  '{:,.0f}'.format(obj.qty22)
    
    @admin.display(ordering="qty23",description=format_html('23年数量'))
    def display_qty23(self, obj):
        return  '{:,.0f}'.format(obj.qty23)

    @admin.display(ordering="qty24",description=format_html('24年数量'))
    def display_qty24(self, obj):
        return  '{:,.0f}'.format(obj.qty24)

    @admin.display(ordering="totalqty",description=format_html('总数量'))
    def display_totalqty(self, obj):
        return  '{:,.0f}'.format(obj.totalqty)

    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    
@admin.register(Total_Product_Rank)
class TOTAL_Product_RankAdmin(admin.ModelAdmin):
    search_fields=('supplier','productcode','productname','brand')
    readonly_fields = ('project','rank','productcode','productname','spec','unit','supplier','brand', 'invoicedate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    list_filter = ['project','supplier','brand']
    list_display_links =('productname',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','project','productcode','productname','display_spec','unit','supplier','brand', 'invoicedate','price','display_sum21','display_sum22','display_sum23','display_sum24','display_totalsum')
    ordering = ('id',)
    def has_delete_permission(self,request, obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

    def has_change_permission(self,request, obj=None):
        return False
    
    @admin.display(ordering="sum21",description=format_html('21年采购额'))
    def display_sum21(self, obj):
        return  '{:,.0f}'.format(obj.sum21)

    @admin.display(ordering="sum22",description=format_html('22年采购额'))
    def display_sum22(self, obj):
        return  '{:,.0f}'.format(obj.sum22)
    
    @admin.display(ordering="sum23",description=format_html('23年采购额'))
    def display_sum23(self, obj):
        return  '{:,.0f}'.format(obj.sum23)
    
    @admin.display(ordering="sum24",description=format_html('24年采购额'))
    def display_sum24(self, obj):
        return  '{:,.0f}'.format(obj.sum24)
    
    @admin.display(ordering="totalsum",description=format_html('总采购额'))
    def display_totalsum(self, obj):
        return  '{:,.0f}'.format(obj.totalsum)
    
    @admin.display(ordering="spec",description='规格')
    def display_spec(self, obj):
        max_length = 15
        if len(obj.spec) > max_length:
            return obj.spec[:max_length] + '...'
        else:
            return obj.spec
