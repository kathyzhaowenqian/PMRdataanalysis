"""
重构后的Admin管理界面
支持客户、项目、阶段历史、销售日报的管理
"""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q, Count, Sum
from django import forms
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponse
import openpyxl
import textwrap
import nested_admin

from .models import (
    Customer, Project, ProjectStageHistory, SalesReport,
    ReportUserInfo, Company, SALES_STAGE_CHOICES
)


# ==================== 自定义过滤器 ====================

class SalesmanFilter(SimpleListFilter):
    """负责人过滤器"""
    title = '负责人'
    parameter_name = 'salesman'

    def lookups(self, request, model_admin):
        # 动态获取所有在销售日报中出现过的销售人员
        salesman_ids = SalesReport.objects.values_list('salesman', flat=True).distinct()
        salesmans = ReportUserInfo.objects.filter(id__in=salesman_ids).order_by('chinesename')
        return [(s.id, s.chinesename or s.username) for s in salesmans]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(salesman__id=self.value())
        return queryset


class ProjectCustomerFilter(SimpleListFilter):
    """项目管理中的客户/医院过滤器"""
    title = '医院'
    parameter_name = 'customer'

    def lookups(self, request, model_admin):
        # 动态获取所有在项目中出现过的客户
        customer_ids = Project.objects.values_list('customer', flat=True).distinct()
        customers = Customer.objects.filter(id__in=customer_ids, is_active=True).order_by('name')
        return [(c.id, c.name) for c in customers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(customer__id=self.value())
        return queryset


class ReportCustomerFilter(SimpleListFilter):
    """销售日报中的客户/医院过滤器"""
    title = '医院'
    parameter_name = 'customer'

    def lookups(self, request, model_admin):
        # 动态获取所有在销售日报中出现过的客户
        customer_ids = SalesReport.objects.filter(
            project__isnull=False
        ).values_list('project__customer', flat=True).distinct()
        customers = Customer.objects.filter(id__in=customer_ids, is_active=True).order_by('name')
        return [(c.id, c.name) for c in customers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__customer__id=self.value())
        return queryset


class ProjectStatusFilter(SimpleListFilter):
    """项目状态过滤器"""
    title = '项目状态'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('active', '进行中'),
            ('won', '已赢单'),
            ('lost', '已流失'),
            ('suspended', '暂停跟进'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class StageFilter(SimpleListFilter):
    """阶段过滤器"""
    title = '当前阶段'
    parameter_name = 'current_stage'

    def lookups(self, request, model_admin):
        return SALES_STAGE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(current_stage=self.value())
        return queryset


class FromStageFilter(SimpleListFilter):
    """原阶段过滤器"""
    title = '原阶段'
    parameter_name = 'from_stage'

    def lookups(self, request, model_admin):
        return SALES_STAGE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(from_stage=self.value())
        return queryset


# ==================== Admin 类 ====================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """客户管理"""
    list_display = ('name', 'customer_type', 'level', 'salesman_name',
                   'contact_person', 'contact_phone', 'project_count', 'updatetime')
    list_filter = ('customer_type', 'level', 'is_active')
    search_fields = ('name', 'contact_person', 'contact_phone')
    readonly_fields = ('createtime', 'updatetime')
    list_per_page = 20

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'customer_type', 'level', 'region')
        }),
        ('联系信息', {
            'fields': ('contact_person', 'contact_phone', 'address')
        }),
        ('其他', {
            'fields': ('remark', 'is_active', 'createtime', 'updatetime')
        }),
    )

    @admin.display(description='负责人')
    def salesman_name(self, obj):
        # 获取该客户最新的活跃项目的负责人
        latest_project = obj.projects.filter(is_active=True).order_by('-updatetime').first()
        if latest_project and latest_project.salesman:
            name = latest_project.salesman.chinesename or latest_project.salesman.username
            return str(name)
        return '-'

    @admin.display(description='项目数量')
    def project_count(self, obj):
        count = obj.projects.filter(is_active=True).count()
        return format_html('<b>{}</b>', count)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(project_count_annotation=Count('projects'))


class ProjectStageHistoryInline(nested_admin.NestedTabularInline):
    """项目阶段历史内联显示"""
    model = ProjectStageHistory
    extra = 0
    can_delete = False  # 不允许删除
    readonly_fields = [
        'from_stage', 'to_stage', 'change_time',
        'days_in_previous_stage', 'change_reason'
    ]
    fields = ['from_stage', 'to_stage', 'change_time', 'days_in_previous_stage', 'change_reason']
    verbose_name = "阶段变更历史"
    verbose_name_plural = "阶段变更历史"

    # 添加 nested_admin 需要的属性
    sortable_options = {}

    def has_add_permission(self, request, obj=None):
        return False  # 禁止添加

    def has_delete_permission(self, request, obj=None):
        return False  # 禁止删除

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-change_time')


class SalesReportInline(nested_admin.NestedTabularInline):
    """销售日报内联显示"""
    model = SalesReport
    extra = 0
    can_delete = False  # 不允许删除
    readonly_fields = ['date1', 'type', 'desc', 'state']
    fields = ['date1', 'type', 'desc', 'state']
    verbose_name = "销售日报"
    verbose_name_plural = "销售日报记录（按时间倒序）"

    # 添加 nested_admin 需要的属性
    sortable_options = {}

    def has_add_permission(self, request, obj=None):
        return False  # 禁止添加

    def has_delete_permission(self, request, obj=None):
        return False  # 禁止删除

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-date1')


@admin.register(Project)
class ProjectAdmin(nested_admin.NestedModelAdmin):
    """项目/商机管理"""
    list_display = ('project_code_link', 'name', 'customer', 'current_stage_tag',
                   'status_tag', 'win_probability_bar', 'salesman_name',
                   'estimated_amount_display', 'actual_amount_display', 'updatetime')
    list_filter = (ProjectStatusFilter, StageFilter, SalesmanFilter, ProjectCustomerFilter, 'lost_reason')
    search_fields = ('name', 'project_code', 'customer__name')
    readonly_fields = ('project_code', 'createtime', 'updatetime', 'operator')
    list_per_page = 20
    date_hierarchy = 'createtime'

    fieldsets = (
        ('项目基本信息', {
            'fields': ('project_code', 'name', 'customer', 'company')
        }),
        ('销售信息', {
            'fields': ('salesman', 'team_members')
        }),
        ('项目状态', {
            'fields': ('current_stage', 'status', 'win_probability')
        }),
        ('金额和时间', {
            'fields': ('estimated_amount', 'actual_amount', 'expected_close_date', 'actual_close_date')
        }),
        ('输单信息', {
            'fields': ('lost_reason', 'lost_stage', 'competitor_info', 'lost_detail'),
            'classes': ('collapse',)
        }),
        ('暂停信息', {
            'fields': ('suspend_reason', 'expected_resume_date'),
            'classes': ('collapse',)
        }),
        ('说明', {
            'fields': ('description', 'remark'),
            'classes': ('collapse',)
        }),
        ('系统信息', {
            'fields': ('is_active', 'createtime', 'updatetime', 'operator'),
            'classes': ('collapse',)
        }),
    )

    inlines = [ProjectStageHistoryInline, SalesReportInline]

    class Media:
        css = {
            'all': ('admin/css/inline_tables.css',)
        }

    @admin.display(ordering='project_code', description='项目编号')
    def project_code_link(self, obj):
        url = reverse('admin:SALESREPORT_project_change', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.project_code)

    @admin.display(ordering='current_stage', description='当前阶段')
    def current_stage_tag(self, obj):
        stage_colors = {
            '线索获取': 'gray',
            '线索验证/建档': 'gray',
            '商机立项': 'blue',
            '需求调研': 'blue',
            '方案/报价': 'orange',
            '测试/验证': 'orange',
            '准入/关键人认可': 'purple',
            '商务谈判': 'purple',
            '招采/挂网/比选': 'green',
            '中标/赢单': 'green',
            '装机/验收': 'darkgreen',
            '收单': 'darkgreen',
        }
        color = stage_colors.get(obj.current_stage, 'gray')
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 8px; '
            'border-radius:3px; font-size:11px;">{}</span>',
            color, obj.current_stage
        )

    @admin.display(ordering='status', description='状态')
    def status_tag(self, obj):
        status_map = {
            'active': ('进行中', '#409EFF'),
            'won': ('已赢单', '#67C23A'),
            'lost': ('已流失', '#F56C6C'),
            'suspended': ('暂停', '#909399'),
        }
        text, color = status_map.get(obj.status, (obj.status, 'gray'))
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color, text
        )

    @admin.display(ordering='win_probability', description='赢单概率')
    def win_probability_bar(self, obj):
        prob = obj.win_probability
        if prob >= 70:
            color = '#67C23A'
        elif prob >= 40:
            color = '#E6A23C'
        else:
            color = '#909399'

        return format_html(
            '<div style="width:100px; background:#f0f0f0; border-radius:3px;">'
            '<div style="width:{}%; background:{}; color:white; text-align:center; '
            'border-radius:3px; padding:2px 0; font-size:11px;">{}%</div></div>',
            int(prob), color, int(prob)
        )

    @admin.display(ordering='salesman__chinesename', description='负责人')
    def salesman_name(self, obj):
        name = obj.salesman.chinesename or obj.salesman.username
        return str(name) if name else '-'

    @admin.display(ordering='estimated_amount', description='预计金额')
    def estimated_amount_display(self, obj):
        if obj.estimated_amount:
            formatted = '¥{:,.2f}'.format(float(obj.estimated_amount))
            return format_html('{}', formatted)
        return '-'

    @admin.display(ordering='actual_amount', description='实际成交金额')
    def actual_amount_display(self, obj):
        if obj.actual_amount:
            formatted = '¥{:,.2f}'.format(float(obj.actual_amount))
            return format_html('{}', formatted)
        return '-'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.username == 'zwq8zhj':
            return qs
        # 普通销售只能看自己的项目
        return qs.filter(salesman=request.user)

    actions = ['export_projects_to_excel']

    @admin.action(description='导出项目到Excel')
    def export_projects_to_excel(self, request, queryset):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = '项目列表'

        # 表头
        columns = ['项目编号', '项目名称', '客户名称', '负责人', '当前阶段',
                  '项目状态', '赢单概率(%)', '预计金额', '预计成交时间', '创建时间']
        worksheet.append(columns)

        # 数据
        for obj in queryset:
            status_map = {
                'active': '进行中', 'won': '已赢单',
                'lost': '已流失', 'suspended': '暂停'
            }
            worksheet.append([
                obj.project_code,
                obj.name,
                obj.customer.name,
                obj.salesman.chinesename or obj.salesman.username,
                obj.current_stage,
                status_map.get(obj.status, obj.status),
                obj.win_probability,
                float(obj.estimated_amount) if obj.estimated_amount else None,
                obj.expected_close_date,
                obj.createtime.strftime('%Y-%m-%d %H:%M'),
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="projects.xlsx"'
        workbook.save(response)
        return response


@admin.register(ProjectStageHistory)
class ProjectStageHistoryAdmin(admin.ModelAdmin):
    """项目阶段历史管理"""
    list_display = ('project_link', 'customer_name', 'from_stage', 'arrow', 'to_stage',
                   'change_time', 'days_in_previous_stage', 'operator_name')
    list_filter = (FromStageFilter, 'to_stage', 'change_time')
    search_fields = ('project__name', 'project__project_code', 'project__customer__name')
    readonly_fields = ('project', 'from_stage', 'to_stage', 'change_time',
                      'days_in_previous_stage', 'operator', 'createtime')
    date_hierarchy = 'change_time'
    list_per_page = 30

    @admin.display(description='项目')
    def project_link(self, obj):
        url = reverse('admin:SALESREPORT_project_change', args=[obj.project.pk])
        return format_html('<a href="{}">{}</a>', url, obj.project.name)

    @admin.display(ordering='project__customer__name', description='客户名称')
    def customer_name(self, obj):
        return obj.project.customer.name if obj.project and obj.project.customer else '-'

    @admin.display(description='')
    def arrow(self, obj):
        return '→'

    @admin.display(description='操作人')
    def operator_name(self, obj):
        if obj.operator:
            return obj.operator.chinesename or obj.operator.username
        return '-'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class SalesReportForm(forms.ModelForm):
    """销售日报表单"""

    class Meta:
        model = SalesReport
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        # 如果是编辑模式且不是当天的记录，设置为只读
        if self.instance.pk is not None and self.instance.date1 != today:
            for field in self.fields:
                self.fields[field].disabled = True


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    """销售日报管理"""
    form = SalesReportForm
    list_display = ('formatted_date1', 'project_link', 'customer_name', 'company', 'salesman_name',
                   'type_display', 'desc_short', 'state_short')
    list_filter = (ReportCustomerFilter, SalesmanFilter, 'date1', 'type')
    search_fields = ('project__name', 'project__project_code', 'project__customer__name',
                    'salesman__chinesename', 'desc', 'state')
    readonly_fields = ('salesman', 'date1', 'company', 'operator',
                      'createtime', 'updatetime')
    list_per_page = 20
    date_hierarchy = 'date1'

    fieldsets = (
        ('基本信息', {
            'fields': ('project', 'salesman', 'company', 'date1')
        }),
        ('工作内容', {
            'fields': ('type', 'desc', 'state')
        }),
        ('时间规划', {
            'fields': ('last_feedback_date', 'next_plan_date')
        }),
        ('系统信息', {
            'fields': ('operator', 'createtime', 'updatetime', 'is_active'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(ordering='date1', description='填报日期')
    def formatted_date1(self, obj):
        return obj.date1.strftime("%m月%d日")

    @admin.display(description='项目')
    def project_link(self, obj):
        url = reverse('admin:SALESREPORT_project_change', args=[obj.project.pk])
        return format_html('<a href="{}">{}</a>', url, obj.project.name)

    @admin.display(ordering='project__customer__name', description='客户名称')
    def customer_name(self, obj):
        return obj.project.customer.name if obj.project and obj.project.customer else '-'

    @admin.display(ordering='salesman__chinesename', description='填报人')
    def salesman_name(self, obj):
        name = obj.salesman.chinesename or obj.salesman.username
        return format_html('<div style="width:50px;">{}</div>', name)

    @admin.display(ordering='type', description='活动类型')
    def type_display(self, obj):
        type_map = {
            '阶段推进': '🎯 阶段推进',
            '客户活动': '👥 客户活动',
            '内部工作': '📝 内部工作',
        }
        return type_map.get(obj.type, obj.type or '-')

    @admin.display(description='工作简述')
    def desc_short(self, obj):
        text = textwrap.shorten(obj.desc, width=50, placeholder='...')
        return format_html('<div style="width:200px;">{}</div>', text)

    @admin.display(description='推进状态')
    def state_short(self, obj):
        text = textwrap.shorten(obj.state, width=50, placeholder='...')
        return format_html('<div style="width:200px;">{}</div>', text)

    def has_add_permission(self, request, obj=None):
        return False  # 通过前端表单提交

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.date1 != timezone.now().date():
            return False
        # Boss组不能删除
        if request.user.groups.filter(name__in=['boss', 'JCboss']).exists():
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        # 非当天记录不可修改
        if obj is not None and obj.date1 != timezone.now().date():
            return False
        # Boss组只读
        if request.user.groups.filter(name__in=['boss', 'JCboss']).exists():
            return False
        # 只能修改自己的记录
        if obj is not None and obj.date1 == timezone.now().date():
            return obj.salesman == request.user or request.user.is_superuser or request.user.username == 'zwq8zhj'
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.username == 'zwq8zhj':
            return qs
        # Boss组可以查看所有
        if request.user.groups.filter(name__in=['boss', 'JCboss']).exists():
            return qs
        # 普通销售只看自己的
        return qs.filter(salesman=request.user)

    actions = ['export_to_excel']

    @admin.action(description='导出到Excel')
    def export_to_excel(self, request, queryset):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = '销售日报'

        columns = ['填报日期', '项目名称', '医院', '填报人', '工作简述',
                  '工作类型', '最新推进状态', '下次计划跟进时间']
        worksheet.append(columns)

        for obj in queryset:
            worksheet.append([
                obj.date1,
                obj.project.name,
                obj.company.company,
                obj.salesman.chinesename or obj.salesman.username,
                obj.desc,
                obj.type,
                obj.state,
                obj.next_plan_date,
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'
        workbook.save(response)
        return response
