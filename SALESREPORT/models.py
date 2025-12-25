"""
重构后的销售日报数据模型
基于CRM最佳实践设计：Customer -> Project -> StageHistory + SalesReport
"""

from django.db import models
from Marketing_Research.models import UserInfo
from django.utils import timezone


# ==================== 常量定义 ====================

# 销售阶段选择
SALES_STAGE_CHOICES = [
    ('线索获取', '线索获取'),
    ('线索验证/建档', '线索验证/建档'),
    ('商机立项', '商机立项'),
    ('需求调研', '需求调研'),
    ('方案/报价', '方案/报价'),
    ('测试/验证', '测试/验证'),
    ('准入/关键人认可', '准入/关键人认可'),
    ('商务谈判', '商务谈判'),
    ('招采/挂网/比选', '招采/挂网/比选'),
    ('中标/赢单', '中标/赢单'),
    ('装机/验收', '装机/验收'),
    ('收单', '收单'),
]

# 项目状态
PROJECT_STATUS_CHOICES = [
    ('active', '进行中'),
    ('won', '已赢单'),
    ('lost', '已流失'),
    ('suspended', '暂停跟进'),
]

# 客户级别
CUSTOMER_LEVEL_CHOICES = [
    ('A', 'A类客户'),
    ('B', 'B类客户'),
    ('C', 'C类客户'),
]

# 销售活动类型（简化版 - 使用中文值）
ACTIVITY_TYPE_CHOICES = [
    ('阶段推进', '🎯 阶段推进'),
    ('客户活动', '👥 客户活动'),      # 原：客户拜访、电话沟通、技术演示、商务谈判
    ('内部工作', '📝 内部工作'),      # 原：方案准备、内部协调、招标准备
]

# 旧版活动类型映射（用于数据迁移）
LEGACY_ACTIVITY_TYPE_MAPPING = {
    # 旧的英文详细类型 -> 新的中文简化类型
    'customer_visit': '客户活动',
    'phone_call': '客户活动',
    'tech_demo': '客户活动',
    'negotiation': '客户活动',
    'proposal_prep': '内部工作',
    'internal_coord': '内部工作',
    'bid_prep': '内部工作',
    'other': '内部工作',
    'stage_advance': '阶段推进',
    # 中间版本的英文值 -> 新的中文值
    'customer': '客户活动',
    'internal': '内部工作',
}

# 输单原因
LOST_REASON_CHOICES = [
    ('price', '价格因素'),
    ('competitor', '竞争对手中标'),
    ('budget_cancel', '客户预算取消'),
    ('product_mismatch', '产品不符合需求'),
    ('timing', '时机不合适'),
    ('other', '其他'),
]


# ==================== 代理模型 ====================

class ReportUserInfo(UserInfo):
    """用户信息代理模型"""

    class Meta:
        proxy = True
        managed = False
        db_table = 'django_admin_v2"."auth_user'
        verbose_name = "用户"
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.chinesename if self.chinesename else self.username


class Company(models.Model):
    """公司/医院信息"""

    company = models.CharField(verbose_name='公司', max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(verbose_name='是否呈现', null=False, default=True)

    class Meta:
        managed = False
        db_table = 'marketing_research_v2"."Company'
        verbose_name_plural = '公司列表'

    def __str__(self):
        return self.company


# ==================== 核心业务模型 ====================

class Customer(models.Model):
    """客户主表"""

    name = models.CharField(verbose_name='客户名称', max_length=255)
    region = models.CharField(verbose_name='所属区域', max_length=100, blank=True)
    customer_type = models.CharField(verbose_name='客户类型', max_length=50,
                                    choices=[('hospital', '医院'), ('dealer', '经销商'), ('other', '其他')],
                                    default='hospital')
    level = models.CharField(verbose_name='客户级别', max_length=10,
                           choices=CUSTOMER_LEVEL_CHOICES,
                           blank=True, default='C')
    contact_person = models.CharField(verbose_name='关键联系人', max_length=100, blank=True)
    contact_phone = models.CharField(verbose_name='联系电话', max_length=50, blank=True)
    address = models.CharField(verbose_name='地址', max_length=500, blank=True)
    remark = models.TextField(verbose_name='备注', blank=True)

    createtime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    is_active = models.BooleanField(verbose_name='是否启用', default=True)

    class Meta:
        managed = True
        db_table = 'marketing_research_v2"."Customer'
        verbose_name = '客户'
        verbose_name_plural = '客户管理'
        ordering = ['-updatetime']

    def __str__(self):
        return self.name


class Project(models.Model):
    """项目/商机主表"""

    # 基本信息
    name = models.CharField(verbose_name='项目名称', max_length=255)
    project_code = models.CharField(verbose_name='项目编号', max_length=100, unique=True,
                                   help_text='自动生成或手动输入，用于唯一标识项目')
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT,
                                verbose_name='客户', related_name='projects')
    company = models.ForeignKey('Company', on_delete=models.CASCADE,
                               db_column='company', to_field='id',
                               verbose_name='所属公司')

    # 销售信息
    salesman = models.ForeignKey('ReportUserInfo', on_delete=models.PROTECT,
                                db_column='salesman', to_field='id',
                                related_name='owned_projects',
                                verbose_name='负责销售')
    team_members = models.ManyToManyField('ReportUserInfo',
                                         related_name='participated_projects',
                                         verbose_name='协同人员',
                                         blank=True)

    # 项目阶段和状态
    current_stage = models.CharField(verbose_name='当前阶段', max_length=50,
                                    choices=SALES_STAGE_CHOICES,
                                    default='线索获取')
    status = models.CharField(verbose_name='项目状态', max_length=20,
                            choices=PROJECT_STATUS_CHOICES,
                            default='active')

    # 金额和概率
    estimated_amount = models.DecimalField(verbose_name='预计金额(元)',
                                          max_digits=12, decimal_places=2,
                                          null=True, blank=True)
    win_probability = models.IntegerField(verbose_name='赢单概率(%)',
                                         default=0,
                                         help_text='0-100之间的整数')

    # 时间信息
    expected_close_date = models.DateField(verbose_name='预计成交时间',
                                          null=True, blank=True)
    actual_close_date = models.DateField(verbose_name='实际成交时间',
                                        null=True, blank=True)

    # 备注和说明
    description = models.TextField(verbose_name='项目描述', blank=True)
    remark = models.TextField(verbose_name='备注', blank=True)

    # 输单相关字段
    lost_reason = models.CharField(
        verbose_name='流失原因',
        max_length=50,
        choices=LOST_REASON_CHOICES,
        blank=True,
        null=True,
        help_text='项目输单时的主要原因'
    )
    lost_stage = models.CharField(
        verbose_name='流失时所在阶段',
        max_length=50,
        choices=SALES_STAGE_CHOICES,
        blank=True,
        null=True,
        help_text='项目流失时所处的销售阶段，用于分析各阶段流失率'
    )
    competitor_info = models.CharField(
        verbose_name='主要竞争对手',
        max_length=200,
        blank=True,
        null=True,
        help_text='如因竞争对手失败，记录竞争对手信息'
    )
    lost_detail = models.TextField(
        verbose_name='流失详细说明',
        blank=True,
        null=True,
        help_text='详细描述项目流失的原因和经过'
    )

    # 暂停跟进字段
    suspend_reason = models.TextField(
        verbose_name='暂停原因',
        blank=True,
        null=True,
        help_text='项目暂停跟进的原因'
    )
    expected_resume_date = models.DateField(
        verbose_name='预计恢复时间',
        blank=True,
        null=True,
        help_text='预计恢复跟进的时间'
    )

    # 实际成交金额（与estimated_amount区分）
    actual_amount = models.DecimalField(
        verbose_name='实际成交金额(元)',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='项目赢单后的实际成交金额'
    )

    # 系统字段
    createtime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    operator = models.ForeignKey('ReportUserInfo', on_delete=models.SET_NULL,
                                db_column='operator', to_field='id',
                                related_name='operated_projects',
                                verbose_name='最后操作人', null=True)
    is_active = models.BooleanField(verbose_name='是否启用', default=True)

    class Meta:
        managed = True
        db_table = 'marketing_research_v2"."SalesProject'
        verbose_name = '项目/商机'
        verbose_name_plural = '项目管理'
        ordering = ['-updatetime']
        indexes = [
            models.Index(fields=['project_code']),
            models.Index(fields=['salesman', 'status']),
            models.Index(fields=['current_stage']),
        ]

    def __str__(self):
        return f"{self.project_code} - {self.name}"

    def update_current_stage(self):
        """根据最新的阶段历史更新当前阶段"""
        latest_history = self.stage_histories.order_by('-change_time').first()
        if latest_history:
            self.current_stage = latest_history.to_stage
            self.save(update_fields=['current_stage', 'updatetime'])


class ProjectStageHistory(models.Model):
    """项目阶段变更历史"""

    project = models.ForeignKey('Project', on_delete=models.CASCADE,
                               related_name='stage_histories',
                               verbose_name='项目')
    from_stage = models.CharField(verbose_name='原阶段', max_length=50,
                                 choices=SALES_STAGE_CHOICES,
                                 null=True, blank=True,
                                 help_text='首次创建项目时为空')
    to_stage = models.CharField(verbose_name='新阶段', max_length=50,
                               choices=SALES_STAGE_CHOICES)

    change_time = models.DateTimeField(verbose_name='变更时间', default=timezone.now)
    days_in_previous_stage = models.IntegerField(verbose_name='上一阶段停留天数',
                                                 default=0,
                                                 help_text='在原阶段停留的天数')

    change_reason = models.TextField(verbose_name='变更原因/说明', blank=True,
                                    help_text='阶段推进的关键事件或原因')

    operator = models.ForeignKey('ReportUserInfo', on_delete=models.SET_NULL,
                                db_column='operator', to_field='id',
                                verbose_name='操作人', null=True)

    createtime = models.DateTimeField(verbose_name='记录时间', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'marketing_research_v2"."ProjectStageHistory'
        verbose_name = '阶段变更记录'
        verbose_name_plural = '项目阶段历史'
        ordering = ['-change_time']
        indexes = [
            models.Index(fields=['project', '-change_time']),
        ]

    def __str__(self):
        from_stage_display = self.from_stage or '初始'
        return f"{self.project.name}: {from_stage_display} → {self.to_stage}"

    def save(self, *args, **kwargs):
        """保存时自动计算停留天数"""
        if self.from_stage and self.project_id:
            # 查找上一次进入from_stage的时间
            previous_entry = ProjectStageHistory.objects.filter(
                project=self.project,
                to_stage=self.from_stage,
                change_time__lt=self.change_time
            ).order_by('-change_time').first()

            if previous_entry:
                delta = self.change_time.date() - previous_entry.change_time.date()
                self.days_in_previous_stage = delta.days

        super().save(*args, **kwargs)

        # 更新项目的当前阶段
        self.project.update_current_stage()


class SalesReport(models.Model):
    """销售日报 - 记录每日工作内容"""

    project = models.ForeignKey('Project', on_delete=models.CASCADE,
                               related_name='daily_reports',
                               verbose_name='关联项目',
                               null=True, blank=True)
    salesman = models.ForeignKey('ReportUserInfo', on_delete=models.PROTECT,
                                db_column='salesman', to_field='id',
                                related_name='salesmanreport',
                                verbose_name='填报人')
    company = models.ForeignKey('Company', on_delete=models.CASCADE,
                               db_column='company', to_field='id',
                               verbose_name='公司')

    date1 = models.DateField(verbose_name='填报日期')
    desc = models.TextField(verbose_name='工作简述', max_length=1000)
    type = models.CharField(
        verbose_name='活动类型',
        max_length=50,
        choices=ACTIVITY_TYPE_CHOICES,
        blank=True,
        help_text='销售活动的类型'
    )
    state = models.CharField(verbose_name='最新推进状态', max_length=255,
                           blank=True,
                           help_text='本次工作的具体进展')

    # 时间规划
    last_feedback_date = models.DateField(
        verbose_name='上一阶段反馈时间（已弃用）',
        null=True,
        blank=True,
        help_text='此字段已弃用，请使用ProjectStageHistory查询阶段历史'
    )
    next_plan_date = models.DateField(verbose_name='下次计划跟进时间',
                                     null=True, blank=True)

    # 系统字段
    operator = models.ForeignKey('ReportUserInfo', on_delete=models.SET_NULL,
                                db_column='operator', to_field='id',
                                related_name='operatorreport',
                                verbose_name='最后操作人', null=True)
    createtime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    is_active = models.BooleanField(verbose_name='是否启用', default=True)

    class Meta:
        managed = True
        db_table = 'marketing_research_v2"."SalesReport'
        verbose_name = '销售日报'
        verbose_name_plural = '销售日报管理'
        ordering = ['-date1', '-createtime']
        indexes = [
            models.Index(fields=['project', '-date1']),
            models.Index(fields=['salesman', '-date1']),
        ]

    def __str__(self):
        return f"{self.project.name} - {self.date1}"


# ==================== 兼容性：保留旧的SalesReport模型用于数据迁移 ====================

class SalesReportOld(models.Model):
    """旧的销售日报模型 - 仅用于数据迁移"""

    company = models.ForeignKey('Company', models.CASCADE, db_column='company',
                               to_field='id', verbose_name='公司')
    salesman = models.ForeignKey('ReportUserInfo', models.CASCADE,
                                db_column='salesman', to_field='id',
                                related_name='old_salesmanreport',
                                verbose_name='负责人')
    date1 = models.DateField(verbose_name='填报日期')
    project = models.CharField(verbose_name='项目', max_length=255)
    desc = models.TextField(verbose_name='工作简述', max_length=255)
    type = models.CharField(verbose_name='工作类型', max_length=255)
    state = models.CharField(verbose_name='最新推进状态', max_length=255)
    stage = models.CharField(verbose_name='已完成阶段', max_length=255,
                           choices=SALES_STAGE_CHOICES)
    date2 = models.DateField(verbose_name='上一阶段反馈时间', null=True)
    date3 = models.DateField(verbose_name='最近计划反馈时间', null=True)
    operator = models.ForeignKey('ReportUserInfo', models.CASCADE,
                                db_column='operator', to_field='id',
                                related_name='old_operatorreport',
                                verbose_name='最后操作人')
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(verbose_name='是否呈现', default=True)

    class Meta:
        managed = False  # 不让Django管理，使用现有表
        db_table = 'marketing_research_v2"."JcReport'
        verbose_name_plural = '旧销售日报(迁移用)'
