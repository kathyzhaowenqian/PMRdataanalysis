
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.forms import Textarea
from Marketing_Research.models import UserInfo
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator
 
def get_compmany_default_value():
    return Company.objects.get(id=2).company


class UserInfoMindray(UserInfo):    
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
    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_active = False
        self.save()

class Hospital(models.Model):
    district_choices=(
        ('黄浦', '黄浦'),
        ('徐汇', '徐汇'),
        ('长宁', '长宁'),
        ('静安', '静安'),
        ('普陀', '普陀'),
        ('虹口', '虹口'),
        ('杨浦', '杨浦'), 
        ('浦东', '浦东'), 
        ('闵行', '闵行'), 
        ('宝山', '宝山'), 
        ('嘉定', '嘉定'), 
        ('金山', '金山'), 
        ('松江', '松江'), 
        ('青浦', '青浦'), 
        ('奉贤', '奉贤'),         
        ('崇明', '崇明'),      
    )
    hospitalclass_choices=(
        ('三级', '三级'),
        ('二级', '二级'),
        ('一级', '一级'),
        ('未定级', '未定级'),
    )
    # id = models.BigAutoField(primary_key=True)
    district = models.CharField(verbose_name='区域',max_length=255,choices=district_choices)
    hospitalclass = models.CharField(verbose_name='医院级别',max_length=255,choices=hospitalclass_choices)
    hospitalname = models.CharField(verbose_name='医院名称',max_length=255)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)


    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"Hospital'
        verbose_name_plural = '医院列表'

    def __str__(self):
        return self.hospitalname
    
    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_active = False
        self.save()

class Brand(models.Model):
    # id = models.BigAutoField(primary_key=True)
    brand = models.CharField(verbose_name='品牌',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"Brand'
        verbose_name_plural = '品牌列表'

    def __str__(self):
            return self.brand

class CompetitionRelation(models.Model):
    # id = models.BigAutoField(primary_key=True)
    competitionrelation = models.CharField(verbose_name='竞品关系点',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"CompetitionRelation'
        verbose_name_plural = '竞品关系列表'
    def __str__(self):
            return self.competitionrelation
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        self.is_active = False
        self.save()

class SalesmanPositionMindray(models.Model):
    # id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('UserInfoMindray', models.CASCADE, db_column='user',to_field='id') #settings.AUTH_USER_MODEL
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    position = models.CharField(verbose_name='岗位',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"SalesmanPosition'
        verbose_name_plural = '员工职位列表'

class MindrayBloodCellProject(models.Model):
    """血球仪器的具体项目表"""
    PROJECT_CHOICES = [
        ('CRP', 'CRP'),
        ('SAA', 'SAA'),
        ('ESR', '血沉'),
        ('CBC', '血常规'),
    ]
    
    instrument_survey = models.ForeignKey(
        "MindrayInstrumentSurvey", 
        on_delete=models.CASCADE, 
        verbose_name='仪器调研',
        related_name='blood_projects'
    )
    project_type = models.CharField(
        max_length=10, 
        choices=PROJECT_CHOICES, 
        verbose_name='具体项目'
    )
    sample_volume = models.IntegerField(
        default=0, 
        verbose_name='标本量', 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0)]
    )
    competitionrelation = models.ForeignKey(
        'CompetitionRelation', 
        models.CASCADE, 
        db_column='competitionrelation',
        to_field='id',
        verbose_name='竞品关系点',
        blank=True, null=True
    )
    dealer_name = models.CharField(
        max_length=200, 
        verbose_name='经销商名称', 
        blank=True, 
        null=True
    )
    
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(verbose_name='是否呈现', null=False, default=True)

    class Meta:
        db_table = 'marketing_research_v2\".\"MindrayBloodCellProject'
        verbose_name_plural = '血球项目详情'
        # 确保同一个仪器的同一个项目类型不重复
        unique_together = ['instrument_survey', 'project_type']

    def __str__(self):
        return 'id:'+str(self.pk)  
        # return f"{self.instrument_survey} - {self.get_project_type_display()}"

   
    def save(self, *args, **kwargs):
        """重写save方法，保存后更新仪器的汇总信息"""
        super().save(*args, **kwargs)
        
        # 更新对应仪器的汇总信息
        if self.instrument_survey:
            self.instrument_survey.calculate_all_blood_summaries()
            self.instrument_survey.save(update_fields=[
                'sample_volume', 'blood_project_types', 
                'blood_project_details',               # 新增字段
                'blood_competition_relations', 'blood_dealer_names', 'updatetime'
            ])
            
            # 触发医院调研统计更新
            if self.instrument_survey.hospital_survey:
                from django.utils import timezone
                hospital_survey = self.instrument_survey.hospital_survey
                hospital_survey.calculate_all_statistics()
                hospital_survey.updatetime = timezone.now()
                hospital_survey.save(update_fields=[
                    'crp_total_volume', 'saa_total_volume', 
                    'esr_total_volume', 'routine_total_volume',
                    'blood_cell_total_count', 'glycation_total_count', 'urine_total_count',
                    'blood_cell_summary', 'glycation_summary', 'urine_summary',
                    'updatetime'
                ])
    
    
    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除，并更新仪器汇总信息"""
        # 在删除前保存相关引用
        instrument_survey = self.instrument_survey
        hospital_survey = None
        if instrument_survey and instrument_survey.hospital_survey:
            hospital_survey = instrument_survey.hospital_survey
        
        # 执行逻辑删除
        self.is_active = False
        self.save()
        
        # 更新仪器的汇总信息
        if instrument_survey:
            instrument_survey.calculate_all_blood_summaries()
            instrument_survey.save(update_fields=[
                'sample_volume', 'blood_project_types', 
                'blood_project_details',               # 新增字段
                'blood_competition_relations', 'blood_dealer_names', 'updatetime'
            ])
        
        # 触发hospital_survey统计更新
        if hospital_survey:
            from django.utils import timezone
            hospital_survey.calculate_all_statistics()
            hospital_survey.updatetime = timezone.now()
            hospital_survey.save(update_fields=[
                'crp_total_volume', 'saa_total_volume', 
                'esr_total_volume', 'routine_total_volume',
                'blood_cell_total_count', 'glycation_total_count', 'urine_total_count',
                'blood_cell_summary', 'glycation_summary', 'urine_summary',
                'updatetime'
            ])

class MindrayHospitalSurvey(models.Model):
    FAMILIARITY_CHOICES = [
        ('red', '不认识'),
        ('yellow', '有商机在跟进'), 
        ('green', '有明确代理商'),
        ('blue', '成单'),
    ]
    
    SALES_MODE_CHOICES = [
        ('direct', '直销'),
        ('distribution', '分销'),
        ('notours', '非我司业务'),
    ]

    hospital = models.OneToOneField("Hospital", on_delete=models.CASCADE, verbose_name='医院')
    qitian_manager = models.ForeignKey('UserInfoMindray', models.CASCADE, db_column='qitian_manager',to_field='id',related_name='qitian_manager',verbose_name= '其田负责人')

    mindray_manager = models.CharField(max_length=100, verbose_name='迈瑞负责人', blank=True, null=True)
    
    # 主任信息
    director_name = models.CharField(max_length=100, verbose_name='主任姓名', blank=True, null=True)
    director_contact = models.ForeignKey('UserInfoMindray', models.CASCADE, db_column='director_contact',to_field='id',related_name='director_contact',verbose_name= '主任对接人', blank=True, null=True)
    director_familiarity = models.CharField(max_length=10, choices=FAMILIARITY_CHOICES,default='red', blank=True, null=True, verbose_name='主任客情')
    
    # 组长信息
    leader_name = models.CharField(max_length=100, verbose_name='组长姓名', blank=True, null=True)
    leader_contact = models.ForeignKey('UserInfoMindray', models.CASCADE, db_column='leader_contact',to_field='id',related_name='leader_contact',verbose_name= '组长对接人', blank=True, null=True)
    leader_familiarity = models.CharField(max_length=10, choices=FAMILIARITY_CHOICES,default='red', blank=True, null=True, verbose_name='组长客情')
    
    # 操作老师信息
    operator_name = models.CharField(max_length=100, verbose_name='操作老师姓名', blank=True, null=True)
    operator_contact = models.ForeignKey('UserInfoMindray', models.CASCADE, db_column='operator_contact',to_field='id',related_name='operator_contact',verbose_name= '操作老师对接人', blank=True, null=True)

    # 销售模式
    sales_mode = models.CharField(max_length=20, choices=SALES_MODE_CHOICES, verbose_name='销售模式', blank=True, null=True)
    distribution_channel = models.CharField(max_length=200, blank=True, null=True, verbose_name='分销渠道')

    
    created_by = models.ForeignKey('UserInfoMindray',  models.CASCADE, db_column='created_by',to_field='id',related_name='created_by', verbose_name='修改人')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    # 添加计算字段
    crp_total_volume = models.IntegerField('CRP总标本量', default=0, blank=True)
    saa_total_volume = models.IntegerField('SAA总标本量', default=0, blank=True) 
    esr_total_volume = models.IntegerField('血沉总标本量', default=0, blank=True)
    routine_total_volume = models.IntegerField('血常规总标本量', default=0, blank=True)
    
    # 新增：糖化和尿液标本量字段
    glycation_total_volume = models.IntegerField('糖化总标本量', default=0, blank=True)
    urine_total_volume = models.IntegerField('尿液总标本量', default=0, blank=True)


    # 新增：各类仪器总台数
    blood_cell_total_count = models.IntegerField('血球仪器总台数', default=0, blank=True)
    glycation_total_count = models.IntegerField('糖化仪器总台数', default=0, blank=True)
    urine_total_count = models.IntegerField('尿液仪器总台数', default=0, blank=True)
    
    # 新增：血球仪器汇总信息
    blood_cell_summary = models.TextField('血球品牌-型号-台数-装机年份-标本量', blank=True, null=True)
     # 新增：糖化和尿液仪器汇总信息
    glycation_summary = models.TextField('糖化品牌-型号-台数-装机年份-标本量', blank=True, null=True)
    urine_summary = models.TextField('尿液品牌-型号-台数-装机年份-标本量', blank=True, null=True)
    
    sales_opportunities_summary = models.TextField('商机项目-型号-标本量-落地时间', blank=True, null=True)

    def calculate_project_volumes(self):
        """计算各项目总标本量"""
        from django.db.models import Sum
        
        # 使用聚合查询更高效
        project_volumes = MindrayBloodCellProject.objects.filter(
            instrument_survey__hospital_survey=self,
            instrument_survey__is_active=True,
            instrument_survey__category__name="血球",
            is_active=True
        ).values('project_type').annotate(
            total_volume=Sum('sample_volume')
        )
        
        # 初始化
        volumes = {'CRP': 0, 'SAA': 0, 'ESR': 0, 'CBC': 0}
        
        # 更新实际值
        for item in project_volumes:
            project_type = item['project_type']
            total_volume = item['total_volume'] or 0
            if project_type in volumes:
                volumes[project_type] = total_volume
        
        # 更新模型字段
        self.crp_total_volume = volumes['CRP']
        self.saa_total_volume = volumes['SAA']
        self.esr_total_volume = volumes['ESR']
        self.routine_total_volume = volumes['CBC']
        
        return volumes
    
     
    def calculate_instrument_counts(self):
        """计算各类仪器总台数"""
        from django.db.models import Sum
        
        # 分别计算每个分类的仪器台数
        blood_cell_count = MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True,
            category__name="血球"
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        glycation_count = MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True,
            category__name="糖化"
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        urine_count = MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True,
            category__name="尿液"
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        # 更新模型字段
        self.blood_cell_total_count = blood_cell_count
        self.glycation_total_count = glycation_count
        self.urine_total_count = urine_count
        
        return {
            '血球': blood_cell_count,
            '糖化': glycation_count,
            '尿液': urine_count
        }
    
    def calculate_blood_cell_summary(self):
        """计算血球仪器汇总信息"""
        from django.db.models import Sum
        
        # # 获取血球仪器及其项目标本量汇总
        # blood_instruments = MindrayInstrumentSurvey.objects.filter(
        #     hospital_survey=self,
        #     is_active=True,
        #     category__name="血球"
        # ).prefetch_related('blood_projects')

        # 获取血球仪器及其项目标本量汇总 - 修改：添加一致的排序
        blood_instruments = MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True,
            category__name="血球"
        ).select_related(
            'brand', 'model', 'category'
        ).order_by('category__id', 'brand__id', 'createtime')  # 修改：添加排序规则


        summaries = []
        
        for instrument in blood_instruments:
            # 计算该仪器下所有血球项目的标本量总和
            total_sample_volume = MindrayBloodCellProject.objects.filter(
                instrument_survey=instrument,
                is_active=True
            ).aggregate(
                total=Sum('sample_volume')
            )['total'] or 0
            
            # 格式化：（品牌-型号-台数-装机年份-标本量总和）
            brand_name = instrument.brand.brand if instrument.brand else "未知"
            # model_name = instrument.model or "未知"
            model_name = instrument.model.model_name if instrument.model else "未知"
            quantity = instrument.quantity or 0
            installation_year = instrument.installation_year or "未知"
            
            summary = f"({brand_name}-{model_name}-{quantity}台-{installation_year}-{total_sample_volume})"
            summaries.append(summary)
        
        # 用 "/" 连接所有仪器信息
        self.blood_cell_summary = "\n".join(summaries) if summaries else "无"
        
        return self.blood_cell_summary
    
    def calculate_glycation_summary(self):
        """计算糖化仪器汇总信息"""
        # 获取糖化仪器
        glycation_instruments = MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True,
            category__name="糖化"
        )
        
        summaries = []
        
        for instrument in glycation_instruments:
            # 直接取sample_volume值
            sample_volume = instrument.sample_volume or 0
            
            # 格式化：（品牌-型号-台数-装机年份-标本量）
            brand_name = instrument.brand.brand if instrument.brand else "未知"
            # model_name = instrument.model or "未知"
            model_name = instrument.model.model_name if instrument.model else "未知"
            quantity = instrument.quantity or 0
            installation_year = instrument.installation_year or "未知"
            
            summary = f"({brand_name}-{model_name}-{quantity}台-{installation_year}-{sample_volume})"
            summaries.append(summary)
        
        # 用 "/" 连接所有仪器信息
        self.glycation_summary = "\n".join(summaries) if summaries else "无"
        
        return self.glycation_summary
    
    def calculate_urine_summary(self):
        """计算尿液仪器汇总信息"""
        # 获取尿液仪器
        urine_instruments = MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True,
            category__name="尿液"
        )
        
        summaries = []
        
        for instrument in urine_instruments:
            # 直接取sample_volume值
            sample_volume = instrument.sample_volume or 0
            
            # 格式化：（品牌-型号-台数-装机年份-标本量）
            brand_name = instrument.brand.brand if instrument.brand else "未知"
            # model_name = instrument.model or "未知"
            model_name = instrument.model.model_name if instrument.model else "未知"
            quantity = instrument.quantity or 0
            installation_year = instrument.installation_year or "未知"
            
            summary = f"({brand_name}-{model_name}-{quantity}台-{installation_year}-{sample_volume})"
            summaries.append(summary)
        
        # 用 "/" 连接所有仪器信息
        self.urine_summary = "\n".join(summaries) if summaries else "无"
        
        return self.urine_summary

    def calculate_glycation_urine_volumes(self):
        """计算糖化和尿液仪器标本量总和"""
        from django.db.models import Sum
        
        # 计算糖化仪器标本量总和
        glycation_volume = MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True,
            category__name="糖化"
        ).aggregate(total=Sum('sample_volume'))['total'] or 0
        
        # 计算尿液仪器标本量总和
        urine_volume = MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True,
            category__name="尿液"
        ).aggregate(total=Sum('sample_volume'))['total'] or 0
        
        # 更新模型字段
        self.glycation_total_volume = glycation_volume
        self.urine_total_volume = urine_volume
        
        return {
            '糖化标本量': glycation_volume,
            '尿液标本量': urine_volume
        }

    def calculate_sales_opportunities_summary(self):
        """计算商机汇总信息"""
        opportunities = SalesOpportunity.objects.filter(
            hospital_survey=self,
            is_active=True
        ).order_by('createtime')
        
        summaries = []
        
        for opp in opportunities:
            # 格式化：（型号-项目-标本量-落地时间）
            # model_name = opp.opportunity_model or "未知"
            model_name = opp.opportunity_model.model_name if opp.opportunity_model else "未知"

            project_name = opp.get_opportunity_project_display()
            sample_volume = opp.sample_volume or 0
            landing_time = opp.landing_time or "未知"
            
            summary = f"({project_name}-{model_name}-{sample_volume}-{landing_time})"
            summaries.append(summary)
        
        # 用 "/" 连接所有商机信息
        self.sales_opportunities_summary = "\n".join(summaries) if summaries else "无"
        
        return self.sales_opportunities_summary
    
    def calculate_all_statistics(self):
        """一次性计算所有统计信息（修改现有方法）"""
        self.calculate_project_volumes()
        self.calculate_instrument_counts()
        self.calculate_glycation_urine_volumes()
        self.calculate_blood_cell_summary()
        self.calculate_glycation_summary()
        self.calculate_urine_summary()
        self.calculate_sales_opportunities_summary()  # 新增
        
        return {
            'project_volumes': {
                'CRP': self.crp_total_volume,
                'SAA': self.saa_total_volume,
                'ESR': self.esr_total_volume,
                'CBC': self.routine_total_volume
            },
            'instrument_volumes': {
                '糖化标本量': self.glycation_total_volume,
                '尿液标本量': self.urine_total_volume
            },
            'instrument_counts': {
                '血球': self.blood_cell_total_count,
                '糖化': self.glycation_total_count,
                '尿液': self.urine_total_count
            },
            'blood_cell_summary': self.blood_cell_summary,
            'glycation_summary': self.glycation_summary,
            'urine_summary': self.urine_summary,
            'sales_opportunities_summary': self.sales_opportunities_summary  # 新增
        }
  
 
    class Meta:
        # managed=False
        db_table = 'marketing_research_v2\".\"MindrayHospitalSurvey'
        verbose_name_plural = '其田市场调研列表'
    
    def __str__(self):
            return self.hospital.hospitalname if self.hospital else "未指定医院"

    
    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除，级联删除所有关联数据"""
        print(self,'我在model.py的删除') 
        
        # 1. 先逻辑删除所有关联的血球项目（通过仪器间接关联）
        MindrayBloodCellProject.objects.filter(
            instrument_survey__hospital_survey=self,
            is_active=True
        ).update(is_active=False)
        
        # 2. 逻辑删除所有关联的仪器调研
        MindrayInstrumentSurvey.objects.filter(
            hospital_survey=self,
            is_active=True
        ).update(is_active=False)
        
        # 3. 逻辑删除所有关联的销售商机
        SalesOpportunity.objects.filter(
            hospital_survey=self,
            is_active=True
        ).update(is_active=False)
        
        # 4. 最后删除医院调研本身
        self.is_active = False
        self.save()
        
        print(f"已级联逻辑删除医院调研及所有关联数据: {self}")


class MindrayInstrumentCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='仪器分类')
    order = models.IntegerField(default=0, verbose_name='排序')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"MindrayInstrumentCategory'
        verbose_name_plural = '仪器分类'
        ordering = ['order']
    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model删除')
        self.is_active = False
        self.save()
        # 级联假删除相关的仪器调研数据
        MindrayInstrumentSurvey.objects.filter(category=self).update(is_active=False)

class InstrumentModel(models.Model):
    model_name = models.CharField(verbose_name='型号名称', max_length=255, blank=True, null=True)
    brand = models.ForeignKey('Brand', models.CASCADE, db_column='brand', to_field='id', verbose_name='所属品牌', blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(verbose_name='是否呈现', null=False, default=True)

    class Meta:
        db_table = 'marketing_research_v2\".\"MindrayInstrumentModel'
        verbose_name_plural = '仪器型号列表'
        ordering = ['model_name']

    def __str__(self):
        return self.model_name or "未知型号"

class MindrayInstrumentSurvey(models.Model):
    IS_OUR_CHOICES = [
        (True, '是'),
        (False, '否'),
    ]
    
    SALES_CHANNEL_CHOICES = [
        ('direct', '直销'),
        ('distribution', '分销'),
    ]
    installation_location_CHOICES = [
        ('outpatient', '门诊'),
        ('emergency', '急诊'),
        ('inpatient', '病房'),
        ('fever_clinic', '发热门诊'),
        ('physical_exam', '体检'),
        
    ]

    hospital_survey = models.ForeignKey("MindrayHospitalSurvey", db_column='hospital_survey',on_delete=models.CASCADE, verbose_name='医院调研')
    category = models.ForeignKey("MindrayInstrumentCategory", db_column='category',on_delete=models.CASCADE, verbose_name='仪器分类')
    
    is_our_instrument = models.BooleanField(choices=IS_OUR_CHOICES, verbose_name='是否我司仪器')
    our_sales_channel = models.CharField(max_length=20, choices=SALES_CHANNEL_CHOICES, blank=True, verbose_name='我司业务销售渠道')
    
    brand = models.ForeignKey("Brand", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='品牌')
    model = models.ForeignKey("InstrumentModel", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='型号')
    modelmemo = models.CharField(max_length=500, verbose_name='型号备注', blank=True, null=True)


    quantity = models.IntegerField(default=1, verbose_name='台数', blank=True, null=True)
    installation_year = models.CharField(
        max_length=4,
        verbose_name='装机年份',
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{4}$', '请输入4位数字年份')]
    )
    installation_location = models.CharField(max_length=200, choices=installation_location_CHOICES, blank=True, verbose_name='仪器安装地')

    # 针对非血球类别的字段（糖化和尿液）
    sample_volume = models.IntegerField(default=0, verbose_name='标本量', blank=True, null=True,validators=[MinValueValidator(0)])
    competitionrelation = models.ForeignKey('CompetitionRelation', models.CASCADE, db_column='competitionrelation',to_field='id',verbose_name= '竞品关系点', blank=True, null=True)
    dealer_name = models.CharField(max_length=200, verbose_name='经销商名称', blank=True, null=True)

    # 新增：血球项目汇总字段
    blood_project_types = models.CharField(max_length=200, verbose_name='血球项目汇总', blank=True, null=True)
    blood_competition_relations = models.TextField(verbose_name='血球竞品关系点汇总', blank=True, null=True)
    blood_dealer_names = models.TextField(verbose_name='血球经销商汇总', blank=True, null=True)

    # 新增：血球项目详细汇总字段
    blood_project_details = models.TextField(verbose_name='血球项目详细汇总', blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(verbose_name='是否呈现', null=False, default=True)


    # 在MindrayInstrumentSurvey模型中添加
    last_modified_by = models.ForeignKey(
        UserInfoMindray,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='最后修改人',
        related_name='modified_instrument_surveys'
    )
    class Meta:
        db_table = 'marketing_research_v2\".\"MindrayInstrumentSurvey'
        verbose_name_plural = '仪器具体信息'
        ordering = ['category__order', 'id']

   
    @property
    def is_blood_category(self):
        """判断是否为血球类别"""
        return self.category and self.category.name == '血球'

    
    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除，并触发统计更新"""
        # 在删除前保存hospital_survey引用
        hospital_survey = self.hospital_survey
        
        # 1. 先逻辑删除所有关联的血球项目
        MindrayBloodCellProject.objects.filter(
            instrument_survey=self,
            is_active=True
        ).update(is_active=False)
        
        # 2. 执行逻辑删除仪器本身
        self.is_active = False
        self.save()
        
        # 3. 触发hospital_survey统计更新
        if hospital_survey:
            from django.utils import timezone
            hospital_survey.calculate_all_statistics()
            hospital_survey.updatetime = timezone.now()
            hospital_survey.save(update_fields=[
                'crp_total_volume', 'saa_total_volume', 
                'esr_total_volume', 'routine_total_volume',
                'glycation_total_volume', 'urine_total_volume',
                'blood_cell_total_count', 'glycation_total_count', 'urine_total_count',
                'blood_cell_summary', 'glycation_summary', 'urine_summary',
                'sales_opportunities_summary',
                'updatetime'
            ])
            print(f"模型删除后更新医院调研统计完成: {hospital_survey}")
            
    def calculate_blood_sample_volume(self):
        """计算血球仪器的标本量总和"""
        if self.is_blood_category:
            from django.db.models import Sum
            total = MindrayBloodCellProject.objects.filter(
                instrument_survey=self,
                is_active=True
            ).aggregate(total=Sum('sample_volume'))['total'] or 0
            
            # 更新sample_volume字段
            self.sample_volume = total
            return total
        return self.sample_volume or 0

 
    def calculate_blood_project_summaries(self):
        """计算血球项目的汇总信息"""
        if not self.is_blood_category:
            return
            
        projects = MindrayBloodCellProject.objects.filter(
            instrument_survey=self,
            is_active=True
        ).select_related('competitionrelation').order_by('project_type', 'id')  # 添加这个排序
        
        if not projects.exists():
            self.blood_project_types = ""
            self.blood_competition_relations = ""
            self.blood_dealer_names = ""
            return
        
        # 汇总项目类型
        project_types = []
        competition_relations = []
        dealer_names = []
        
        for project in projects:
            # 项目类型
            if project.project_type:
                display_name = project.get_project_type_display()
                if display_name not in project_types:
                    project_types.append(display_name)
            
            # 竞品关系点 - 空值显示"未知竞品关系点"
            if project.competitionrelation and project.competitionrelation.competitionrelation:
                relation = project.competitionrelation.competitionrelation
                if relation not in competition_relations:
                    competition_relations.append(relation)
            else:
                # 如果没有竞品关系点，添加"未知竞品关系点"（但避免重复）
                unknown_relation = "未知"
                if unknown_relation not in competition_relations:
                    competition_relations.append(unknown_relation)
            
            # 经销商名称 - 空值显示"未知经销商"
            if project.dealer_name and project.dealer_name.strip():
                dealer = project.dealer_name.strip()
                if dealer not in dealer_names:
                    dealer_names.append(dealer)
            else:
                # 如果没有经销商名称，添加"未知经销商"（但避免重复）
                unknown_dealer = "未知"
                if unknown_dealer not in dealer_names:
                    dealer_names.append(unknown_dealer)
        
        # 用"/"连接各项信息
        self.blood_project_types = "/".join(project_types) if project_types else ""
        self.blood_competition_relations = "/".join(competition_relations) if competition_relations else ""
        self.blood_dealer_names = "/".join(dealer_names) if dealer_names else ""
        
        return {
            'project_types': self.blood_project_types,
            'competition_relations': self.blood_competition_relations,
            'dealer_names': self.blood_dealer_names
        }   
     
    def calculate_blood_project_details(self):
        """计算血球项目详细汇总信息"""
        if not self.is_blood_category:
            self.blood_project_details = ""
            return
            
        projects = MindrayBloodCellProject.objects.filter(
            instrument_survey=self,
            is_active=True
        ).select_related('competitionrelation').order_by('project_type','createtime', 'id')  # 添加这个排序
        
        if not projects.exists():
            self.blood_project_details = ""
            return
        
        # 构建详细汇总信息
        project_details = []
        
        for project in projects:
            # 项目类型显示名
            project_name = project.get_project_type_display()
            
            # 标本量
            sample_volume = project.sample_volume or 0
            
            # 竞品关系点 - 空值显示"未知竞品关系点"
            competition = "未知"
            if project.competitionrelation and project.competitionrelation.competitionrelation:
                competition = project.competitionrelation.competitionrelation
            
            # 经销商名称 - 空值显示"未知经销商"
            dealer = "未知"
            if project.dealer_name and project.dealer_name.strip():
                dealer = project.dealer_name.strip()
            
            # 格式化单个项目：(血球项目-标本量-竞品关系点-经销商名称)
            detail = f"({project_name}-{sample_volume}-{competition}-{dealer})"
            project_details.append(detail)
        
        # 用"/"连接所有项目详情
        self.blood_project_details = "\n".join(project_details) if project_details else ""
        
        return self.blood_project_details
     

    def calculate_all_blood_summaries(self):
        """一次性计算所有血球汇总信息"""
        if self.is_blood_category:
            self.calculate_blood_sample_volume()
            self.calculate_blood_project_summaries()
            self.calculate_blood_project_details()  # 新增：计算详细汇总

    def save(self, *args, **kwargs):
        """重写save方法，自动计算血球仪器的汇总信息"""
        # 如果是血球仪器，自动计算汇总信息
        if self.is_blood_category:
            # 先保存，确保对象存在
            super().save(*args, **kwargs)
            # 然后计算并更新汇总信息
            self.calculate_all_blood_summaries()
            # 只有当汇总信息确实有变化时才再次保存
            super().save(update_fields=[
                'sample_volume', 'blood_project_types', 
                'blood_project_details',               # 新增字段
                'blood_competition_relations', 'blood_dealer_names', 'updatetime'
            ])
        else:
            super().save(*args, **kwargs)
        
        # 触发医院调研统计更新
        if self.hospital_survey:
            self.hospital_survey.calculate_all_statistics()


# 初始化3个分类
def init_categories():
    categories = [
        ('血球', 1),
        ('糖化', 2), 
        ('尿液', 3)
     
    ]
    for name, order in categories:
        MindrayInstrumentCategory.objects.get_or_create(name=name, defaults={'order': order})


# ======================商机======================
class SalesOpportunity(models.Model):
    """销售商机表"""
    
    PROJECT_CHOICES = [
        ('BLOOD_CELL', '血球'),
        ('GLYCATION', '糖化'), 
        ('URINE', '尿液'),
    ]
    hospital_survey = models.ForeignKey(
        'MindrayHospitalSurvey', 
        on_delete=models.CASCADE, 
        verbose_name='医院调研'
    )
    # salesperson 字段保留，但会自动设置
    salesperson = models.ForeignKey(
        'UserInfoMindray', 
        on_delete=models.CASCADE, 
        verbose_name='销售人员',
        related_name='sales_opportunities',
        editable=False  # 添加这个，使其在admin表单中不可编辑
    )
    
    
    # opportunity_model = models.CharField(
    #     max_length=100, 
    #     verbose_name='商机型号',       
    # )

    opportunity_model = models.ForeignKey(
        'InstrumentModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='商机型号'
    )

    opportunity_project = models.CharField(
        max_length=10, 
        choices=PROJECT_CHOICES,
        verbose_name='商机项目'
    )
    sample_volume = models.IntegerField(
        verbose_name='商机标本量',         
        blank=True,null=True,default=0,validators=[MinValueValidator(0)]
    )
    landing_time = models.CharField(
        max_length=7,
        verbose_name='落地时间',
        help_text='格式：YYYY-MM，如：2024-03',
        validators=[RegexValidator(r'^\d{4}-\d{2}$', '格式：YYYY-MM')]
    )
    opportunity_status = models.TextField(
        verbose_name='商机情况',
        blank=True,null=True
    )
    
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(verbose_name='是否有效', default=True)
    
    class Meta:
        db_table = 'marketing_research_v2\".\"MindraySalesOpportunity'
        verbose_name = '销售商机'
        verbose_name_plural = '销售商机管理'
        ordering = ['-createtime']
        
    def __str__(self):
        hospital_name = self.hospital_survey.hospital.hospitalname if self.hospital_survey and self.hospital_survey.hospital else '未知医院'
        # return f"{hospital_name} - {self.opportunity_model} - {self.get_opportunity_project_display()}"
        return 'id:'+str(self.pk) 
    
    @property
    def hospital(self):
        """便捷访问医院信息"""
        return self.hospital_survey.hospital if self.hospital_survey else None
    
    @property
    def hospital_manager(self):
        """便捷访问医院负责人"""
        return self.hospital_survey.qitian_manager if self.hospital_survey else None
 

    def save(self, *args, **kwargs):
        """保存时自动设置销售人员为医院调研负责人，并更新医院调研汇总"""
        if self.hospital_survey and self.hospital_survey.qitian_manager:
            self.salesperson = self.hospital_survey.qitian_manager
        
        super().save(*args, **kwargs)
        
        # 更新医院调研的商机汇总
        if self.hospital_survey:
            from django.utils import timezone
            self.hospital_survey.calculate_sales_opportunities_summary()
            self.hospital_survey.updatetime = timezone.now()
            self.hospital_survey.save(update_fields=['sales_opportunities_summary', 'updatetime'])
    
    def delete(self, using=None, keep_parents=False):
        """重写删除方法实现逻辑删除，并更新医院调研汇总"""
        hospital_survey = self.hospital_survey  # 在删除前保存引用
        
        self.is_active = False
        self.save()
        
        # 更新医院调研的商机汇总
        if hospital_survey:
            from django.utils import timezone
            hospital_survey.calculate_sales_opportunities_summary()
            hospital_survey.updatetime = timezone.now()
            hospital_survey.save(update_fields=['sales_opportunities_summary', 'updatetime'])
 
# 修改代理模型，基于SalesOpportunity
class SalesOpportunitySummary(SalesOpportunity):
    """销售商机汇总代理模型"""
    class Meta:
        proxy = True
        verbose_name = "医院商机汇总"
        verbose_name_plural = "医院商机汇总展示"



