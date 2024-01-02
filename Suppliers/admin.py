from django.contrib import admin
from Suppliers.models import *
# Register your models here.


class XEY_Supplier_Product_SummaryInline(admin.TabularInline):
    model = XEY_Supplier_Product_Summary
    fk_name = "supplierrank"
    extra = 0
    fields=['supplier','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum'] 
    # readonly_fields = ('sumpermonth',)
    verbose_name = verbose_name_plural = ('徐二院供应商销量明细')


@admin.register(SupplierInfo)  
class SupplierInfoAdmin(admin.ModelAdmin):   
    search_fields=['supplier']
    exclude = ('id','createtime','updatetime','is_active')
    list_display = ('supplier','contact','payterm','tax','delivery','project',)

    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super().get_search_results(request, queryset, search_term)
        if 'autocomplete' in request.path:
            queryset=queryset.filter(is_active=True).order_by('id')
        return queryset,use_distinct 
    
@admin.register(XEY_Supplier_Rank)
class XEY_Supplier_RankAdmin(admin.ModelAdmin):
    inlines=[XEY_Supplier_Product_SummaryInline]
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)

    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    ordering = ('rank',)


@admin.register(XEY_Supplier_Product_Summary)
class XEY_Supplier_Product_SummaryAdmin(admin.ModelAdmin):
    exclude = ('id','createtime','updatetime')
    search_fields=('supplier',)

    list_display_links =('supplier',)
    empty_value_display = '--'
    list_per_page = 15
    list_display = ('rank','supplier','contact','payterm','tax','delivery','productcode','productname','spec','unit','brand', 'recentdate','price','qty21','qty21','qty22','qty23','qty24','totalqty','sum21','sum22','sum23','sum24','totalsum')
    ordering = ('rank',)
