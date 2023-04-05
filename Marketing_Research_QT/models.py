from django.db import models
# Create your models here.
from django.db import models
# Create your models here.
from django.db import models
# Create your models here.
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.forms import Textarea
from Marketing_Research.models import UserInfo
from multiselectfield import MultiSelectField



def get_compmany_default_value():
    return Company.objects.get(id=2).company



class UserInfo3(UserInfo):
    
    # id = models.OneToOneField(UserInfo,models.CASCADE, db_column='id',to_field='id',verbose_name= '用户id')
    # username = models.OneToOneField(UserInfo,models.CASCADE, db_column='username',to_field='username',verbose_name= '名')

    # chinesename = models.CharField(verbose_name='中文名',max_length=255,null=True)
    # createtime = models.DateTimeField(auto_now_add=True)
    # updatetime = models.DateTimeField(auto_now=True)
    # is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    
    
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


class Project(models.Model):
    # id = models.BigAutoField(primary_key=True)
    project = models.CharField(verbose_name='项目名称',max_length=255, blank=True, null=True)
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
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

    



class ProjectDetail3(models.Model):
    # id = models.BigAutoField(primary_key=True)
    # project = models.ForeignKey('Project', models.CASCADE, db_column='project',to_field='id')
    detailedproject = models.CharField(verbose_name='项目明细',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"ProjectDetail'
        verbose_name_plural = '项目细分列表'

    def __str__(self):
        return self.detailedproject
    

class Brand(models.Model):
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


class SalesmanPosition3(models.Model):
    # id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('UserInfo3', models.CASCADE, db_column='user',to_field='id') #settings.AUTH_USER_MODEL
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    position = models.CharField(verbose_name='岗位',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"SalesmanPosition'
        verbose_name_plural = '员工职位列表'


class PMRResearchList3(models.Model):
    salesmode_choices=[
        ('我司业务',
        (('直销', '直销'), ('代理', '代理'))
        ),
        ('第二类:非我司业务',
          (('竞品', '竞品'),('空白市场', '空白市场'))
        )
    ]
    # id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    hospital = models.ForeignKey('Hospital', models.CASCADE, db_column='hospital',to_field='id',verbose_name= '医院')
    project = models.ForeignKey('Project', models.CASCADE, db_column='project',to_field='id',verbose_name= '项目')
    salesman1 = models.ForeignKey('UserInfo3', models.CASCADE, db_column='salesman1',to_field='id',related_name='salesman1qt',verbose_name= '第一负责人')
    salesman2 = models.ForeignKey('UserInfo3', models.CASCADE, db_column='salesman2',to_field='id',related_name='salesman2qt',verbose_name= '第二负责人')

    salesmode=MultiSelectField(verbose_name='销售模式',max_length=25,choices=salesmode_choices,blank=True,null=True)

    testspermonth = models.PositiveIntegerField(verbose_name='月总测试数',default = 0)
    owntestspermonth = models.PositiveIntegerField(verbose_name='我司业务月测试数',default = 0)
    contactname = models.CharField(verbose_name='主任姓名',max_length=255, blank=True, null=True)
    contactmobile = models.CharField(verbose_name='联系方式',max_length=255, blank=True, null=True)
    saleschannel = models.TextField(verbose_name='销售路径',max_length=255, blank=True, null=True)
    support = models.TextField(verbose_name='所需支持',max_length=500, blank=True, null=True)
    adminmemo=models.TextField(verbose_name='备注',max_length=500, blank=True, null=True)
    operator = models.ForeignKey('UserInfo3', models.CASCADE, db_column='operator',to_field='id',related_name='operatorqt',verbose_name= '最后操作人')
    olddata = models.BooleanField(verbose_name='原始数据',max_length=255, default = False)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    uniquestring=models.CharField(verbose_name='联合唯一值',max_length=255, blank=True, null=True)
    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"PMRResearchList'
        verbose_name_plural = '市场调研列表'
    
    def __str__(self):
            # return ('公司:{}, 医院:{}, 项目:{}, 第一责任人:{}'.format(self.company,self.hospital,self.project,self.salesman1))
            return self.uniquestring

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model.py的删除') 
        self.is_active = False
        self.save()
        #可以把相关联得 Objects 也一起伪删除
        PMRResearchDetail3.objects.filter(researchlist=self).update(is_active=False)
        SalesTarget3.objects.filter(researchlist=self).update(is_active=False)
        DetailCalculate3.objects.filter(researchlist=self).update(is_active=False)





class PMRResearchDetail3(models.Model):
    ownbusiness_choices = (
        (True, '是'),
        (False, '否'),)
    # id = models.BigAutoField(primary_key=True)
    researchlist = models.ForeignKey('PMRResearchList3', models.CASCADE, db_column='researchlist',to_field='id',verbose_name= '调研列表')
    #是否要关联detailproject表？？？
    detailedproject = models.ForeignKey('ProjectDetail3', models.CASCADE, db_column='detailedproject',to_field='id',verbose_name= '项目细分(注意根据本页主项目填报)',help_text=u"例如:本页项目为流式,则项目细分为流式项目下的具体细分",null=True)

    # detailedproject2=models.CharField(verbose_name='项目细分',max_length=255, blank=True, null=True)
    ownbusiness=models.BooleanField(verbose_name='是否我司业务',null=False, default = False,choices=ownbusiness_choices)
    brand = models.ForeignKey('Brand', models.CASCADE, db_column='brand',to_field='id',verbose_name= '品牌',null=True)
    machinemodel = models.CharField(verbose_name='仪器型号',max_length=255, blank=True, null=True)
    machineseries = models.CharField(verbose_name='序列号(我司仪器必填)',max_length=255, blank=True, null=True)
    machinenumber = models.PositiveIntegerField(verbose_name='仪器数量',default = 1)
    installdate = models.DateField(verbose_name='装机日期',blank=True, null=True,help_text=u'例: 2023/02/01')
    testprice = models.DecimalField(verbose_name='单价',max_digits=25, decimal_places=2, blank=True, null=True)
    sumpermonth = models.DecimalField(verbose_name='22年我司月均销售额',max_digits=25, decimal_places=2, blank=True, null=True,default = 0)
    expiration=models.CharField(verbose_name='装机时间',max_length=255, blank=True, null=True)
    endsupplier = models.CharField(verbose_name='终端商(医院收票供应商)',max_length=255, blank=True, null=True)
    competitionrelation = models.ForeignKey('CompetitionRelation', models.CASCADE, db_column='competitionrelation',to_field='id',verbose_name= '竞品关系点',blank=True,null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"PMRResearchDetail'
        verbose_name_plural = '市场调研详情表'

    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model删除')
        self.is_active = False
        self.save()



class SalesTarget3(models.Model): 
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
    researchlist = models.ForeignKey('PMRResearchList3', models.CASCADE, db_column='researchlist',to_field='id',verbose_name= '调研列表')
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
        db_table = 'marketing_research_v2\".\"SalesTarget'
        verbose_name_plural = '销售目标及完成率表'

    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我model在删除')
        self.is_active = False
        self.save()




class DetailCalculate3(models.Model):
    id = models.BigAutoField(primary_key=True)
    researchlist = models.OneToOneField('PMRResearchList3', models.CASCADE, db_column='researchlist',to_field='id',verbose_name= '调研列表')
    totalmachinenumber = models.PositiveIntegerField(verbose_name='仪器总数',default = 0)
    ownmachinenumber = models.PositiveIntegerField(verbose_name='我司仪器总数',default = 0)
    ownmachinepercent = models.DecimalField(verbose_name='我司仪器数占比',max_digits=25, decimal_places=2, blank=True, null=True)
    newold=models.CharField(verbose_name='业务类型',max_length=255, blank=True, null=True)
    totalsumpermonth = models.DecimalField(verbose_name='22年我司月均销售额总计',max_digits=25, decimal_places=2, blank=True, null=True,default = 0)

    detailedprojectcombine=models.CharField(verbose_name='项目细分集合',max_length=255, blank=True, null=True)
    ownbusinesscombine=models.CharField(verbose_name='是否我司业务集合',max_length=255, blank=True, null=True)
    brandscombine=models.CharField(verbose_name='品牌集合',max_length=255, blank=True, null=True)
    machinemodelcombine=models.CharField(verbose_name='仪器型号集合',max_length=255, blank=True, null=True)
    machineseriescombine=models.CharField(verbose_name='序列号集合',max_length=255, blank=True, null=True)
    installdatescombine = models.CharField(verbose_name='装机时间集合',max_length=255, blank=True, null=True)
    competitionrelationcombine = models.CharField(verbose_name='竞品关系点集合',max_length=255, blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"DetailCalculate'
        verbose_name_plural = '项目统计结果表'






