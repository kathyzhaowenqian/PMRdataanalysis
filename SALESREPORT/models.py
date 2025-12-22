from django.db import models


from Marketing_Research.models import UserInfo


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


class ReportUserInfo(UserInfo):   
    
    class Meta:
        proxy =True
        managed=False
        db_table =  'django_admin_v2\".\"auth_user'
        verbose_name = "用户"
        verbose_name_plural = "用户表"

    def __str__(self):
        if self.chinesename:
            # 如果不为空则返回中文用户名
            return self.chinesename
        else:
            # 如果用户名为空则返回不能为空的对象
            return self.username
        
class Company(models.Model):
    # id = models.BigAutoField(primary_key=True)
    company = models.CharField(verbose_name='公司',max_length=255, blank=True, null=True,)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"Company'
        # verbose_name = '公司列表'
        verbose_name_plural = '公司列表'

    def __str__(self):
            return self.company
    

class SalesReport(models.Model):
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司')
    salesman = models.ForeignKey('ReportUserInfo', models.CASCADE, db_column='salesman',to_field='id',related_name='salesmanreport',verbose_name= '负责人')
    date1 = models.DateField(verbose_name='填报日期',blank=True, null=False)
    project = models.CharField(verbose_name='项目',max_length=255, blank=False, null=False)
    name = models.CharField(verbose_name='主要人员',max_length=255, blank=False, null=False)
    desc = models.TextField(verbose_name='工作简述',max_length=255, blank=False, null=False)
    type = models.CharField(verbose_name='工作类型',max_length=255, blank=False, null=False)
    state = models.CharField(verbose_name='最新推进状态',max_length=255, blank=False, null=False)
    stage = models.CharField(verbose_name='已完成阶段',max_length=255, blank=False, null=False, choices=SALES_STAGE_CHOICES)
    date2 = models.DateField(verbose_name='上一阶段反馈时间',blank=True, null=False)
    date3 = models.DateField(verbose_name='最近计划反馈时间',blank=True, null=False)
    operator = models.ForeignKey('ReportUserInfo', models.CASCADE, db_column='operator',to_field='id',related_name='operatorreport',verbose_name= '最后操作人')   
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=True
        db_table = 'marketing_research_v2\".\"JcReport'
        verbose_name_plural = '集成业务日报'

    def __str__(self):
        return self.project

 