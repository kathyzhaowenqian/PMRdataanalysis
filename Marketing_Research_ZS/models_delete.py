# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.forms import Textarea
from django_pandas.managers import DataFrameManager
from multiselectfield import MultiSelectField
from Marketing_Research.models import UserInfo
from django.db.models import JSONField


def get_compmany_default_value():
    return CompanyDelete.objects.get(id=5).company


class GSMRUserInfoDelete(UserInfo):

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

class CompanyDelete(models.Model):
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
 

class HospitalDelete(models.Model):
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


class ProjectDelete(models.Model):
    # id = models.BigAutoField(primary_key=True)
    project = models.CharField(verbose_name='项目名称',max_length=255, blank=True, null=True)
    company = models.ForeignKey('CompanyDelete', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"Project'
        verbose_name_plural = '项目列表'
        ordering = ['project']

    def __str__(self):
        return self.project

    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在删除')
        self.is_active = False
        self.save()

   

class BrandDelete(models.Model):
    # id = models.BigAutoField(primary_key=True)
    brand = models.CharField(verbose_name='仪器品牌',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"Brand'
        verbose_name_plural = '品牌列表'

    def __str__(self):
            return self.brand




class GSMRSalesmanPositionDelete(models.Model):
    # id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('GSMRUserInfoDelete', models.CASCADE, db_column='user',to_field='id') #settings.AUTH_USER_MODEL
    company = models.ForeignKey('CompanyDelete', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    position = models.CharField(verbose_name='岗位',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"SalesmanPosition'
        verbose_name_plural = '员工职位列表'


class GSMRResearchListDelete(models.Model):
    progress_choices = (
        ('待拜访', '待拜访'),
        ('初期了解中', '初期了解中'),
        ('有意向', '有意向'),
        ('申报预算', '申报预算'),
        ('审批中', '审批中'),
        ('审批通过', '审批通过'),
        ('待招标', '待招标'),
        ('招标完成', '招标完成'),
        ('仪器装机启用', '仪器装机启用'),
        ('仪器试剂均开票','仪器试剂均开票'))
    company = models.ForeignKey('CompanyDelete', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    hospital = models.ForeignKey('HospitalDelete', models.CASCADE, db_column='hospital',to_field='id',verbose_name= '医院')
    project = models.ForeignKey('ProjectDelete', models.CASCADE, db_column='project',to_field='id',verbose_name= '项目')
    salesman1 = models.ForeignKey('GSMRUserInfoDelete', models.CASCADE, db_column='salesman1',to_field='id',related_name='salesman1zsdelete',verbose_name= '第一负责人')
    salesman2 = models.ForeignKey('GSMRUserInfoDelete', models.CASCADE, db_column='salesman2',to_field='id',related_name='salesman2zsdelete',verbose_name= '第二负责人')

    director = models.CharField(verbose_name='科室主任',max_length=255, blank=True, null=True)
    saleschannel = models.TextField(verbose_name='销售路径',max_length=255, blank=True, null=True)
    support = models.TextField(verbose_name='所需支持',max_length=500, blank=True, null=True)
    progress=models.CharField(verbose_name='进展(新项目必选)',max_length=25,choices=progress_choices,blank=True, null=True)

    operator = models.ForeignKey('GSMRUserInfoDelete', models.CASCADE, db_column='operator',to_field='id',related_name='operatorzsdelete',verbose_name= '最后操作人')
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    uniquestring=models.CharField(verbose_name='联合唯一值',max_length=255, blank=True, null=True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"GSMRResearchList'
        verbose_name_plural = '招商调研列表2'
    
    def __str__(self):
        return self.uniquestring

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model.py的删除') 
        self.is_active = False
        self.save()
        #可以把相关联得 Objects 也一起伪删除
        GSMRResearchDetailDelete.objects.filter(researchlist=self).update(is_active=False)
        GSMRSalesTargetDelete.objects.filter(researchlist=self).update(is_active=False)
        GSMRDetailCalculateDelete.objects.filter(researchlist=self).update(is_active=False)



class GSMRResearchDetailDelete(models.Model):
    type_choices = (
        ('非我司业务', '非我司业务'),
        ('国赛美瑞-招商', '国赛美瑞-招商'),
        ('普美瑞-招商','普美瑞-招商'),
        ('普美瑞-直销','普美瑞-直销'),
        ('普美瑞-集成','普美瑞-集成'),
        )
    # id = models.BigAutoField(primary_key=True)
    researchlist = models.ForeignKey('GSMRResearchListDelete', models.CASCADE, db_column='researchlist',to_field='id',verbose_name= '调研列表')
    brand = models.ForeignKey('BrandDelete', models.CASCADE, db_column='brand',to_field='id',verbose_name= '品牌',null=True)
    type= models.CharField(verbose_name='分类',max_length=25,choices=type_choices,default='非我司业务')
    testspermonth = models.PositiveIntegerField(verbose_name='该品牌月测试数',default = 0)
    testprice = models.DecimalField(verbose_name='代理商价格',max_digits=25, decimal_places=2, blank=True, null=True,default = 0.00)
    sumpermonth = models.DecimalField(verbose_name='月产出额',max_digits=25, decimal_places=2, blank=True, null=True,default = 0.00,help_text=u'国赛美瑞-招商的业务，此处必填')
    machinenumber = models.PositiveIntegerField(verbose_name='仪器数量',default = 1)
    installdate = models.DateField(verbose_name='装机日期',blank=True, null=True,help_text=u'例:2023/07/01,如有多台，填最老的那台')

    endsupplier = models.CharField(verbose_name='代理商名称',max_length=255, blank=True, null=True)
    expiration=models.CharField(verbose_name='装机时效',max_length=255, blank=True, null=True)
    
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"GSMRResearchDetail'
        verbose_name_plural = '招商调研详情表2'

    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model删除')
        self.is_active = False
        self.save()




class GSMRSalesTargetDelete(models.Model): 
    Q1completemonth_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3','3'))
    Q2completemonth_choices = (
        ('4', '4'),
        ('5', '5'),
        ('6','6'))
    Q3completemonth_choices = (
        ('7', '7'),
        ('8', '8'),
        ('9','9'))
    Q4completemonth_choices = (
        ('10', '10'),
        ('11', '11'),
        ('12','12'))
    year_choices = (
        ('2023', '2023'),
        ('2024', '2024'),)
    # id = models.BigAutoField(primary_key=True)
    researchlist = models.ForeignKey('GSMRResearchListDelete', models.CASCADE, db_column='researchlist',to_field='id',verbose_name= '调研列表')
    year = models.CharField(verbose_name='年份',max_length=25, choices=year_choices, default=2023)
    q1target = models.DecimalField(verbose_name='Q1目标额/元',max_digits=25, decimal_places=2, default = 0,validators=[MinValueValidator(0)])
    q2target = models.DecimalField(verbose_name='Q2目标额/元',max_digits=25, decimal_places=2, default = 0,validators=[MinValueValidator(0)])
    q3target = models.DecimalField(verbose_name='Q3目标额/元',max_digits=25, decimal_places=2, default = 0,validators=[MinValueValidator(0)])
    q4target = models.DecimalField(verbose_name='Q4目标额/元',max_digits=25, decimal_places=2, default = 0,validators=[MinValueValidator(0)])
   
    q1completemonth=models.CharField(verbose_name='Q1目标完成月',max_length=25,blank=True, null=True,choices=Q1completemonth_choices,default=3)
    q2completemonth=models.CharField(verbose_name='Q2目标完成月',max_length=25,blank=True, null=True,choices=Q2completemonth_choices,default=6)
    q3completemonth=models.CharField(verbose_name='Q3目标完成月',max_length=25,blank=True, null=True,choices=Q3completemonth_choices,default=9)
    q4completemonth=models.CharField(verbose_name='Q4目标完成月',max_length=25,blank=True, null=True,choices=Q4completemonth_choices,default=12)

    q1actualsales= models.DecimalField(verbose_name='Q1实际销售额',max_digits=25, decimal_places=2, blank=True, null=True,default = 0)
    q2actualsales= models.DecimalField(verbose_name='Q2实际销售额',max_digits=25, decimal_places=2, blank=True, null=True,default = 0)
    q3actualsales= models.DecimalField(verbose_name='Q3实际销售额',max_digits=25, decimal_places=2, blank=True, null=True,default = 0)
    q4actualsales= models.DecimalField(verbose_name='Q4实际销售额',max_digits=25, decimal_places=2, blank=True, null=True,default = 0)

    q1finishrate = models.DecimalField(verbose_name='Q1完成率',max_digits=25, decimal_places=2, blank=True, null=True)
    q2finishrate = models.DecimalField(verbose_name='Q2完成率',max_digits=25, decimal_places=2, blank=True, null=True)
    q3finishrate = models.DecimalField(verbose_name='Q3完成率',max_digits=25, decimal_places=2, blank=True, null=True)
    q4finishrate = models.DecimalField(verbose_name='Q4完成率',max_digits=25, decimal_places=2, blank=True, null=True)
   
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    
    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"GSMRSalesTarget'
        verbose_name_plural = '销售目标及完成率表'

    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我model在删除')
        self.is_active = False
        self.save()




class GSMRDetailCalculateDelete(models.Model):
    id = models.BigAutoField(primary_key=True)
    researchlist = models.OneToOneField('GSMRResearchListDelete', models.CASCADE, db_column='researchlist',to_field='id',verbose_name= '调研列表')

    totalmachinenumber = models.PositiveIntegerField(verbose_name='仪器总数',default = 0)
    ownmachinenumber = models.PositiveIntegerField(verbose_name='国赛仪器总数',default = 0)
    ownmachinepercent = models.DecimalField(verbose_name='仪器数占比',max_digits=25, decimal_places=2, blank=True, null=True)
    newold=models.CharField(verbose_name='业务类型',max_length=255, blank=True, null=True)
   
    totaltestspermonth = models.PositiveIntegerField(verbose_name='总月测试数',default = 0)
    owntestspermonth = models.PositiveIntegerField(verbose_name='国赛月测试数',default = 0)
    owntestspercent = models.DecimalField(verbose_name='测试数占比',max_digits=25, decimal_places=2, blank=True, null=True)

    salespermonth = models.DecimalField(verbose_name='总月产出额',max_digits=25, decimal_places=2, blank=True, null=True,default = 0.00)
    ownsalespermonth = models.DecimalField(verbose_name='国赛美瑞招商月产出额',max_digits=25, decimal_places=2, blank=True, null=True,default = 0.00)
    ownsalespercent = models.DecimalField(verbose_name='月产出额占比',max_digits=25, decimal_places=2, blank=True, null=True)

    brandscombine=models.CharField(verbose_name='品牌集合',max_length=255, blank=True, null=True)
    testspermonthcombine=models.CharField(verbose_name='品牌集合',max_length=255, blank=True, null=True)
    progresshistory=JSONField(verbose_name='历史进展',blank=True, null=True)

    
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"GSMRDetailCalculate'
        verbose_name_plural = '项目统计结果表'









