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
from django_pandas.managers import DataFrameManager
from multiselectfield import MultiSelectField
from Marketing_Research.models import UserInfo
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
def get_compmany_default_value():
    return Company.objects.get(id=7).company

class PZXUserInfo(UserInfo):   
    
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

class PZXSalesmanPosition(models.Model):
    # id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('PZXUserInfo', models.CASCADE, db_column='user',to_field='id') #settings.AUTH_USER_MODEL
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    position = models.CharField(verbose_name='岗位',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"SalesmanPosition'
        verbose_name_plural = '员工职位列表'

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

class PZXSPDList(models.Model):
    # id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    salesman = models.ForeignKey('PZXUserInfo', models.CASCADE, db_column='salesman',to_field='id',related_name='salesmanpzx',verbose_name= '负责人')

    supplier = models.CharField(verbose_name='供应商',max_length=255, blank=True, null=True)
    brand = models.CharField(verbose_name='品牌',max_length=255, blank=True, null=True)
    department = models.CharField(verbose_name='科室',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品',max_length=255, blank=True, null=True)
    machinemodel = models.CharField(verbose_name='仪器型号',max_length=255, blank=True, null=True)
    listotal = models.DecimalField(verbose_name='LIS收入',max_digits=25, decimal_places=2, blank=True, null=True)
    salestotal = models.DecimalField(verbose_name='年开票额',max_digits=25, decimal_places=2, blank=True, null=True)
    salestotalpercent = models.DecimalField(verbose_name='开票占比',max_digits=25, decimal_places=6, blank=True, null=True)
    purchasetotal = models.DecimalField(verbose_name='年采购额',max_digits=25, decimal_places=2, blank=True, null=True)
    gppercent = models.DecimalField(verbose_name='毛利率',max_digits=25, decimal_places=6, blank=True, null=True)
    relation = models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)

    operator = models.ForeignKey('PZXUserInfo', models.CASCADE, db_column='operator',to_field='id',related_name='operatorpzx',verbose_name= '最后操作人')   
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    
    class Meta:
        db_table = 'marketing_research_v2\".\"SPDList'
        verbose_name_plural = 'SPD战略地图'
    
    def __str__(self):
        return self.supplier


#============================================================
class PZXOverall(models.Model):
    whygrowth_choices=[       
        ('新开项目', '新开项目'),
        ('供应商重新谈判', '供应商重新谈判'),
        ('渠道变更', '渠道变更'),
        ('品牌替换', '品牌替换'),
        ('套餐绑定', '套餐绑定'),
        ('--', '--'),]
    # completemonth_choices = (
    #     ('1', '1'),
    #     ('2', '2'),
    #     ('3', '3'), 
    #     ('4', '4'),
    #     ('5', '5'),
    #     ('6', '6'),
    #     ('7', '7'),
    #     ('8', '8'),
    #     ('9', '9'),
    #     ('10', '10'),
    #     ('11', '11'),
    #     ('12','12'))
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_compmany_default_value)
    salesman = models.ForeignKey('PZXUserInfo', models.CASCADE, db_column='salesman',to_field='id',related_name='salesmanpzxoverall',verbose_name= '负责人',default=25)
    department = models.CharField(verbose_name='科室',max_length=255, blank=False, null=False)
    semidepartment=models.CharField(verbose_name='使用科室',max_length=255, blank=False, null=False)
    project = models.CharField(verbose_name='项目大类',help_text=u"项目大类必填",max_length=255, blank=False, null=False)

    purchasesum=models.DecimalField(verbose_name='项目1-6月采购额', max_digits=25, decimal_places=2,default=0)
    purchasesumpercent=models.DecimalField(verbose_name='该项目占总采购额占比', max_digits=25, decimal_places=4,default=0)
    theoreticalvalue=models.DecimalField(verbose_name='项目理论销售额', max_digits=25, decimal_places=2,default=0)
    theoreticalgp=models.DecimalField(verbose_name='项目理论毛利润', max_digits=25, decimal_places=2,default=0)
    theoreticalgppercent=models.DecimalField(verbose_name='项目理论毛利率', max_digits=25, decimal_places=4,default=0)

    supplier = models.CharField(verbose_name='供应商',max_length=255, blank=False, null=False)
    supplierpurchasesum=models.DecimalField(verbose_name='供应商1-6月采购额', max_digits=25, decimal_places=2,default=0)
    purchasesumpercentinproject=models.DecimalField(verbose_name='项目中各供应商采购额占比', max_digits=25, decimal_places=4,default=0)
    suppliertheoreticalvalue=models.DecimalField(verbose_name='供应商理论销售额', max_digits=25, decimal_places=2,default=0)
    suppliertheoreticalgp=models.DecimalField(verbose_name='供应商理论毛利润', max_digits=25, decimal_places=2,default=0)
    suppliertheoreticalgppercent=models.DecimalField(verbose_name='供应商理论毛利率', max_digits=25, decimal_places=4,default=0)


    relation=models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)
    actionplan=models.CharField(verbose_name='行动计划',max_length=255, blank=True, null=True)

    whygrowth = MultiSelectField(verbose_name='增量来源',help_text=u"（按住Ctrl键可多选, 选择后, 请在下方填写每一个增量来源的详情）",max_length=255,choices=whygrowth_choices)
    progress = models.CharField(verbose_name='进度',max_length=255, blank=True, null=True)
    support = models.CharField(verbose_name='所需支持',max_length=255, blank=True, null=True)

    monthgpgrowth = models.DecimalField(verbose_name='月毛利额增量预估总计/元', max_digits=25, decimal_places=2,default=0)
    monthgpgrowthdetail = models.CharField(verbose_name='月毛利额增量预估',max_length=255, blank=True, null=True) #用|隔开的

    completemonth=models.CharField(verbose_name='预计落地月份',max_length=25,blank=True, null=True) #,choices=completemonth_choices
    
    thisyeargpgrowth = models.DecimalField(verbose_name='23年毛利额增量预估总计/元',max_digits=25, decimal_places=2, default=0)
    thisyeargpgrowthdetail = models.CharField(verbose_name='23年毛利额增量预估',max_length=255, blank=True, null=True) #用|隔开的
   
    operator = models.ForeignKey('PZXUserInfo', models.CASCADE, db_column='operator',to_field='id',related_name='operatorpzxoverall',verbose_name= '最后操作人')   
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDPlanOverall'
        verbose_name_plural = '作战计划'
    
    def __str__(self):
        return self.project

#新项目---------------------
class PZXNewProjectStatus(models.Model):
    completemonth_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12,12))
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
    overallid = models.ForeignKey('PZXOverall', models.CASCADE, db_column='overallid',to_field='id',verbose_name= '作战计划')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='新开项目')

    progress=models.CharField(verbose_name='进度(必填)',max_length=25,choices=progress_choices,default='待拜访')
    
    completemonth=models.PositiveIntegerField(verbose_name='预计落地月份(默认12月,请修改)',choices=completemonth_choices,default=12)
    monthgpgrowth = models.DecimalField(verbose_name='月毛利额增量预估/元',  max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default=0)
    thisyeargpgrowth = models.DecimalField(verbose_name='23年毛利额增量预估/元',max_digits=25, decimal_places=2, blank=True, null=True)
    
    monthgpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算月毛利额增量', max_digits=25, decimal_places=2, blank=True, null=True)
    thisyeargpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算23年毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)

    target = models.TextField(verbose_name='谈判目标(文字描述,具体金额在下方明细填报)',max_length=255, blank=True, null=True)
    reason = models.TextField(verbose_name='理由',max_length=255, blank=True, null=True)

    relation = models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)
    support = models.CharField(verbose_name='所需支持',max_length=255, blank=True, null=True)
    actionplan=models.TextField(verbose_name='行动计划',max_length=255, blank=True, null=True)

    memo = models.TextField(verbose_name='备注',max_length=255, blank=True, null=True)
    advicedirector = models.CharField(verbose_name='倪日磊意见',max_length=255, blank=True, null=True)
    adviceboss = models.CharField(verbose_name='陈海敏意见',max_length=255, blank=True, null=True)
    statushistory=JSONField(verbose_name='历史status',blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)


    class Meta:
        db_table = 'marketing_research_v2\".\"SPDNewProjectStatus'
        verbose_name_plural = '新开项目状态'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 新项目状态删除')
        self.is_active = False
        self.save()
  

class PZXNewProjectDetail(models.Model):
    brand_choices = (
        ('置换前', '置换前'),
        ('置换后', '置换后'),)
    progressid = models.ForeignKey('PZXNewProjectStatus', models.CASCADE, db_column='progressid',to_field='id',verbose_name= '进度状态')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='新项目明细')

    originalsupplier = models.CharField(verbose_name='供应商',help_text=u"请按系统中供应商名称填报",max_length=255, blank=True, null=True)
    originalbrand = models.CharField(verbose_name='品牌',help_text=u"请按系统中品牌名称填报",max_length=255, blank=True, null=True)
    newsupplier = models.CharField(verbose_name='新供应商 ',max_length=255, blank=True, null=True)
    beforeorafterbrandchange = models.CharField(verbose_name='品牌是置换前还是置换后',max_length=255, blank=True, null=True,choices=brand_choices)
    code = models.CharField(verbose_name='产品编码U8 ',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品名称U8',help_text=u"请按系统名称填报",max_length=255, blank=True, null=True)
    spec = models.CharField(verbose_name='规格',max_length=255, blank=True, null=True)
    unit = models.CharField(verbose_name='单位',max_length=255, blank=True, null=True)

    pplperunit = models.PositiveIntegerField(verbose_name='每单位人份数(必填)',help_text=u"举例：单位是盒，规格是60T/盒，则该处填60。液体类产品请大家仔细斟酌后填报",validators=[MinValueValidator(1)],default = 0)
    recentsales = models.DecimalField(verbose_name='半年度开票额 ',help_text=u"半年度采购数量/单位 X 每单位人份数 X LIS收费单价 X LIS结算%", max_digits=25, decimal_places=2, blank=True, null=True)
    recentcost = models.DecimalField(verbose_name='半年度采购额',help_text=u"半年度采购数量/单位 X 采购价/单位", max_digits=25, decimal_places=2, blank=True, null=True)
    recentgp = models.DecimalField(verbose_name='半年度盈亏额',max_digits=25, decimal_places=2, blank=True, null=True)
    recentgpofsupplier = models.DecimalField(verbose_name='半年度供应商盈利额',max_digits=25, decimal_places=2, blank=True, null=True)
     
    lisfee = models.DecimalField(verbose_name='LIS收费价(必填)',max_digits=25, decimal_places=2,validators=[MinValueValidator(0.01)],default = 0)
    lispercent = models.DecimalField(verbose_name='LIS结算比例(必填,≤1)',max_digits=25, decimal_places=3,validators=[MinValueValidator(0.01),MaxValueValidator(1)],default = 0)
    lissettleprice = models.DecimalField(verbose_name='LIS结算价',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    costperunit = models.DecimalField(verbose_name='采购价/单位(报价)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default = 0)
    purchaseqty = models.DecimalField(verbose_name='半年度采购数量/单位',max_digits=25, decimal_places=1, blank=True, null=True,validators=[MinValueValidator(0)])
    costppl = models.DecimalField(verbose_name='采购价/人份',help_text=u"采购价每单位 / 每单位人份数",max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0)])
    gppercent = models.DecimalField(verbose_name='毛利率',max_digits=25, decimal_places=2, blank=True, null=True)
    costfeepercent = models.DecimalField(verbose_name='原采购价占收费比例',max_digits=25, decimal_places=2, blank=True, null=True)
        
    marketprice = models.DecimalField(verbose_name='市场价/人份(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    marketpricefeepercent = models.DecimalField(verbose_name='市场价占收费比例',max_digits=25, decimal_places=2, blank=True, null=True)
    newcostppl = models.DecimalField(verbose_name='新采购价/人份',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    newcostdroprate = models.DecimalField(verbose_name='新采购价下降比例',max_digits=25, decimal_places=2, blank=True, null=True)
    newgppercent = models.DecimalField(verbose_name='新毛利率',max_digits=25, decimal_places=2, blank=True, null=True)
    newcostfeepercent = models.DecimalField(verbose_name='新采购价占收费比例',max_digits=25, decimal_places=2, blank=True, null=True)
    targetppl = models.DecimalField(verbose_name='谈判目标/元(必填)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    targetdropdate = models.DecimalField(verbose_name='谈判下降比例',max_digits=25, decimal_places=2, blank=True, null=True)
    realmonthlyppl = models.PositiveIntegerField(verbose_name='每月lis开票人份数',default = 0)
    estimatemonthlyppl = models.PositiveIntegerField(verbose_name='预估每月lis开票人份数(必填)',default = 0)
    gpgrowthppl = models.DecimalField(verbose_name='毛利额增量/人份',max_digits=25, decimal_places=2, blank=True, null=True)
    estmonthlygpgrowth = models.DecimalField(verbose_name='预估月毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgp = models.DecimalField(verbose_name='月毛利额',max_digits=25, decimal_places=2, blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDNewProjectDetail'
        verbose_name_plural = '新开项目明细'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 新项目明细删除')
        self.is_active = False
        self.save()


#供应商重新谈判----------------------

class PZXNegotiationStatus(models.Model):
    completemonth_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12,12))
    progress_choices = (
        ('待谈判', '待谈判'),
        ('已谈判等回复', '已谈判等回复'),
        ('新价格已确认', '新价格已确认'),
      )
    overallid = models.ForeignKey('PZXOverall', models.CASCADE, db_column='overallid',to_field='id',verbose_name= '作战计划')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='供应商重新谈判')

    progress=models.CharField(verbose_name='进度(必填)',max_length=25,choices=progress_choices,default='待拜访')
   
    completemonth=models.PositiveIntegerField(verbose_name='预计落地月份(默认12月,请修改)',choices=completemonth_choices,default=12)
    monthgpgrowth = models.DecimalField(verbose_name='月毛利额增量预估/元',  max_digits=25, decimal_places=2,validators=[MinValueValidator(0.01)], default=0)
    thisyeargpgrowth = models.DecimalField(verbose_name='23年毛利额增量预估/元',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算月毛利额增量', max_digits=25, decimal_places=2, blank=True, null=True)
    thisyeargpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算23年毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)

    target = models.TextField(verbose_name='谈判目标(文字描述,具体金额在下方明细填报)',max_length=255, blank=True, null=True)
    reason = models.TextField(verbose_name='理由',max_length=255, blank=True, null=True)
    
    relation = models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)
    support = models.CharField(verbose_name='所需支持',max_length=255, blank=True, null=True)
    actionplan=models.TextField(verbose_name='行动计划',max_length=255, blank=True, null=True)
    memo = models.TextField(verbose_name='备注',max_length=255, blank=True, null=True)
    advicedirector = models.CharField(verbose_name='倪日磊意见',max_length=255, blank=True, null=True)
    adviceboss = models.CharField(verbose_name='陈海敏意见',max_length=255, blank=True, null=True)
    statushistory=JSONField(verbose_name='历史status',blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)


    class Meta:
        db_table = 'marketing_research_v2\".\"SPDNegotiationStatus'
        verbose_name_plural = '供应商重新谈判状态'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 供应商重新谈判状态删除')
        self.is_active = False
        self.save()


class PZXNegotiationDetail(models.Model):
    brand_choices = (
        ('置换前', '置换前'),
        ('置换后', '置换后'),)
    progressid = models.ForeignKey('PZXNegotiationStatus', models.CASCADE, db_column='progressid',to_field='id',verbose_name= '进度状态')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='价格谈判明细')

    originalsupplier = models.CharField(verbose_name='供应商',help_text=u"请按系统中供应商名称填报",max_length=255, blank=True, null=True) ###
    originalbrand = models.CharField(verbose_name='品牌',help_text=u"请按系统中品牌名称填报",max_length=255, blank=True, null=True)###

    newsupplier = models.CharField(verbose_name='新供应商 ',max_length=255, blank=True, null=True)
    beforeorafterbrandchange = models.CharField(verbose_name='品牌是置换前还是置换后',max_length=255, blank=True, null=True,choices=brand_choices)

    productid =  models.ForeignKey('PZXMenu', models.CASCADE, db_column='productid',to_field='id',verbose_name= '产品信息:名称_规格_单位_采购价_供应商_品牌',blank=True, null=True)###
    code = models.CharField(verbose_name='产品编码U8 ',max_length=255, blank=True, null=True)##
    product = models.CharField(verbose_name='产品名称U8',help_text=u"请按系统名称填报",max_length=255, blank=True, null=True)###
    spec = models.CharField(verbose_name='规格',max_length=255, blank=True, null=True)###
    unit = models.CharField(verbose_name='单位',max_length=255, blank=True, null=True)###
    
    pplperunit = models.PositiveIntegerField(verbose_name='每单位人份数(必填)',help_text=u"举例：单位是盒，规格是60T/盒，则该处填60。液体类产品请大家仔细斟酌后填报",validators=[MinValueValidator(1)],default = 0)
    recentsales = models.DecimalField(verbose_name='半年度开票额 ',help_text=u"半年度采购数量/单位 X 每单位人份数 X LIS收费单价 X LIS结算%", max_digits=25, decimal_places=2, blank=True, null=True)
    recentcost = models.DecimalField(verbose_name='半年度采购额',help_text=u"半年度采购数量/单位 X 采购价/单位", max_digits=25, decimal_places=2, blank=True, null=True)
    recentgp = models.DecimalField(verbose_name='半年度盈亏额',max_digits=25, decimal_places=2, blank=True, null=True)
    recentgpofsupplier = models.DecimalField(verbose_name='半年度供应商盈利额',max_digits=25, decimal_places=2, blank=True, null=True)

    lisfee = models.DecimalField(verbose_name='LIS收费价(必填)',max_digits=25, decimal_places=2,validators=[MinValueValidator(0.01)],default = 0)
    lispercent = models.DecimalField(verbose_name='LIS结算比例(必填,≤1)',max_digits=25, decimal_places=3,validators=[MinValueValidator(0.00),MaxValueValidator(1)],default = 0)
    lissettleprice = models.DecimalField(verbose_name='LIS结算价(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    costperunit = models.DecimalField(verbose_name='采购价/单位(报价)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default = 0) ###
    purchaseqty = models.DecimalField(verbose_name='半年度采购数量/单位',max_digits=25, decimal_places=1,validators=[MinValueValidator(0.1)],default = 0)
    costppl = models.DecimalField(verbose_name='采购价/人份',help_text=u"采购价每单位 / 每单位人份数",max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0)])
    gppercent = models.DecimalField(verbose_name='毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    costfeepercent = models.DecimalField(verbose_name='原采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)    
    
    marketprice = models.DecimalField(verbose_name='市场价/人份(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    marketpricefeepercent = models.DecimalField(verbose_name='市场价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostppl = models.DecimalField(verbose_name='新采购价/人份',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    newcostdroprate = models.DecimalField(verbose_name='新采购价下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newgppercent = models.DecimalField(verbose_name='新毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostfeepercent = models.DecimalField(verbose_name='新采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    targetppl = models.DecimalField(verbose_name='谈判目标/元(必填)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default=0) #供应商重新谈判这里必填
    targetdropdate = models.DecimalField(verbose_name='谈判下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    realmonthlyppl = models.PositiveIntegerField(verbose_name='每月lis开票人份数',default = 0)
    estimatemonthlyppl = models.PositiveIntegerField(verbose_name='预估每月lis开票人份数',default = 0)
    gpgrowthppl = models.DecimalField(verbose_name='毛利额增量/人份',max_digits=25, decimal_places=2, blank=True, null=True)
    estmonthlygpgrowth = models.DecimalField(verbose_name='预估月毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgp = models.DecimalField(verbose_name='月毛利额',max_digits=25, decimal_places=2, blank=True, null=True)

    skuhistory=JSONField(verbose_name='历史sku',blank=True, null=True)
    #skuhistory是为了大菜单更新后，如果销售误点保存，会覆盖原来的采购单价，所以在最开始保存的时候就要把sku丢进去。后期点保存的时候，如果发现有历史sku，说明这条是之前填过的，
    #此时对比原来填的采购价和新菜单上的采购价，如果不一致，就把新采购价补充进“新采购价”中，如果一致则不变
    #如果没有历史sku，就用新菜单上的数据来筛选填报

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDNegotiationDetail'
        verbose_name_plural = '供应商重新谈判明细'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 供应商重新谈判明细删除')
        self.is_active = False
        self.save()


#渠道变更------------------

class PZXChangeChannelStatus(models.Model):
    completemonth_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12,12))
    progress_choices = (
        ('待谈判', '待谈判'),
        ('已谈判等回复', '已谈判等回复'),
        ('新渠道价格已确认', '新渠道价格已确认'),
      )
    overallid = models.ForeignKey('PZXOverall', models.CASCADE, db_column='overallid',to_field='id',verbose_name= '作战计划')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='渠道变更')

    progress=models.CharField(verbose_name='进度(必填)',max_length=25,choices=progress_choices,default='待拜访')
   
    completemonth=models.PositiveIntegerField(verbose_name='预计落地月份(默认12月,请修改)',choices=completemonth_choices,default=12)
    monthgpgrowth = models.DecimalField(verbose_name='月毛利额增量预估/元',  max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default=0)
    thisyeargpgrowth = models.DecimalField(verbose_name='23年毛利额增量预估/元',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算月毛利额增量', max_digits=25, decimal_places=2, blank=True, null=True)
    thisyeargpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算23年毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)

    target = models.TextField(verbose_name='谈判目标(文字描述,具体金额在下方明细填报)',max_length=255, blank=True, null=True)
    reason = models.TextField(verbose_name='理由',max_length=255, blank=True, null=True)
    
    relation = models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)
    support = models.CharField(verbose_name='所需支持',max_length=255, blank=True, null=True)
    actionplan=models.TextField(verbose_name='行动计划',max_length=255, blank=True, null=True)

    memo = models.TextField(verbose_name='备注',max_length=255, blank=True, null=True)
    advicedirector = models.CharField(verbose_name='倪日磊意见',max_length=255, blank=True, null=True)
    adviceboss = models.CharField(verbose_name='陈海敏意见',max_length=255, blank=True, null=True)
    statushistory=JSONField(verbose_name='历史status',blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)


    class Meta:
        db_table = 'marketing_research_v2\".\"SPDChangeChannelStatus'
        verbose_name_plural = '渠道变更状态'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 渠道变更状态删除')
        self.is_active = False
        self.save()


class PZXChangeChannelDetail(models.Model):
    brand_choices = (
        ('置换前', '置换前'),
        ('置换后', '置换后'),)
    progressid = models.ForeignKey('PZXChangeChannelStatus', models.CASCADE, db_column='progressid',to_field='id',verbose_name= '进度状态')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='渠道变更明细')

    originalsupplier = models.CharField(verbose_name='原供应商',help_text=u"请按系统中供应商名称填报",max_length=255, blank=True, null=True)
    originalbrand = models.CharField(verbose_name='品牌',help_text=u"请按系统中品牌名称填报",max_length=255, blank=True, null=True)
    newsupplier = models.CharField(verbose_name='新供应商 ',help_text=u"请按系统中供应商名称填报",max_length=255, blank=True, null=True)
    beforeorafterbrandchange = models.CharField(verbose_name='品牌是置换前还是置换后',max_length=255, blank=True, null=True,choices=brand_choices)
    code = models.CharField(verbose_name='产品编码U8 ',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品名称U8',help_text=u"请按系统名称填报",max_length=255, blank=True, null=True)
    spec = models.CharField(verbose_name='规格',max_length=255, blank=True, null=True)
    unit = models.CharField(verbose_name='单位',max_length=255, blank=True, null=True)
    productid =  models.ForeignKey('PZXMenu', models.CASCADE, db_column='productid',to_field='id',verbose_name= '产品信息:名称_规格_单位_采购价_供应商_品牌',blank=True, null=True)###

    pplperunit = models.PositiveIntegerField(verbose_name='每单位人份数(必填)',help_text=u"举例：单位是盒，规格是60T/盒，则该处填60。液体类产品请大家仔细斟酌后填报",validators=[MinValueValidator(1)],default = 0)
    recentsales = models.DecimalField(verbose_name='半年度开票额 ',help_text=u"半年度采购数量/单位 X 每单位人份数 X LIS收费单价 X LIS结算%", max_digits=25, decimal_places=2, blank=True, null=True)
    recentcost = models.DecimalField(verbose_name='半年度采购额',help_text=u"半年度采购数量/单位 X 采购价/单位", max_digits=25, decimal_places=2, blank=True, null=True)
    recentgp = models.DecimalField(verbose_name='半年度盈亏额',max_digits=25, decimal_places=2, blank=True, null=True)
    recentgpofsupplier = models.DecimalField(verbose_name='半年度供应商盈利额',max_digits=25, decimal_places=2, blank=True, null=True)

    lisfee = models.DecimalField(verbose_name='LIS收费价(必填)',max_digits=25, decimal_places=2,validators=[MinValueValidator(0.01)],default = 0)
    lispercent = models.DecimalField(verbose_name='LIS结算比例(必填,≤1)',max_digits=25, decimal_places=3,validators=[MinValueValidator(0.01),MaxValueValidator(1)],default = 0)
    lissettleprice = models.DecimalField(verbose_name='LIS结算价(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    costperunit = models.DecimalField(verbose_name='原供应商采购价/单位',max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default = 0)

    purchaseqty = models.DecimalField(verbose_name='半年度采购数量/单位',max_digits=25, decimal_places=1,validators=[MinValueValidator(0.1)],default = 0)
    costppl = models.DecimalField(verbose_name='采购价/人份',help_text=u"采购价每单位 / 每单位人份数",max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0)])
    gppercent = models.DecimalField(verbose_name='毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    costfeepercent = models.DecimalField(verbose_name='原采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)    
    
    marketprice = models.DecimalField(verbose_name='市场价/人份(必填)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default = 0)
    marketpricefeepercent = models.DecimalField(verbose_name='市场价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostppl = models.DecimalField(verbose_name='新供应商采购价/人份',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    newcostdroprate = models.DecimalField(verbose_name='新采购价下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newgppercent = models.DecimalField(verbose_name='新毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostfeepercent = models.DecimalField(verbose_name='新采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    targetppl = models.DecimalField(verbose_name='与新供应商谈判目标/元(必填)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    targetdropdate = models.DecimalField(verbose_name='谈判下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    realmonthlyppl = models.PositiveIntegerField(verbose_name='每月lis开票人份数',default = 0)
    estimatemonthlyppl = models.PositiveIntegerField(verbose_name='预估每月lis开票人份数',default = 0)
    gpgrowthppl = models.DecimalField(verbose_name='毛利额增量/人份',max_digits=25, decimal_places=2, blank=True, null=True)
    estmonthlygpgrowth = models.DecimalField(verbose_name='预估月毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgp = models.DecimalField(verbose_name='月毛利额',max_digits=25, decimal_places=2, blank=True, null=True)
    skuhistory=JSONField(verbose_name='历史sku',blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDChangeChannelDetail'
        verbose_name_plural = '渠道变更明细'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 SPD渠道变更明细删除')
        self.is_active = False
        self.save()


#品牌替换-------------------

class PZXChangeBrandStatus(models.Model):
    completemonth_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12,12))
    progress_choices = (
        ('待谈判', '待谈判'),
        ('已谈判等回复', '已谈判等回复'),
        ('新价格已确认', '新价格已确认'),
      )
    overallid = models.ForeignKey('PZXOverall', models.CASCADE, db_column='overallid',to_field='id',verbose_name= '作战计划')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='品牌替换')

    progress=models.CharField(verbose_name='进度(必填)',max_length=25,choices=progress_choices,default='待拜访')
   
    completemonth=models.PositiveIntegerField(verbose_name='预计落地月份(默认12月,请修改)',choices=completemonth_choices,default=12)
    monthgpgrowth = models.DecimalField(verbose_name='月毛利额增量预估/元',  max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default=0)
    thisyeargpgrowth = models.DecimalField(verbose_name='23年毛利额增量预估/元',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算月毛利额增量', max_digits=25, decimal_places=2, blank=True, null=True)
    thisyeargpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算23年毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)

    target = models.TextField(verbose_name='谈判目标(文字描述,具体金额在下方明细填报)',max_length=255, blank=True, null=True)
    reason = models.TextField(verbose_name='理由',max_length=255, blank=True, null=True)
    
    relation = models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)
    support = models.CharField(verbose_name='所需支持',max_length=255, blank=True, null=True)
    actionplan=models.TextField(verbose_name='行动计划',max_length=255, blank=True, null=True)

    memo = models.TextField(verbose_name='备注',max_length=255, blank=True, null=True)
    advicedirector = models.CharField(verbose_name='倪日磊意见',max_length=255, blank=True, null=True)
    adviceboss = models.CharField(verbose_name='陈海敏意见',max_length=255, blank=True, null=True)
    statushistory=JSONField(verbose_name='历史status',blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)


    class Meta:
        db_table = 'marketing_research_v2\".\"SPDChangeBrandStatus'
        verbose_name_plural = '品牌替换状态'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 品牌替换状态删除')
        self.is_active = False
        self.save()

#品牌替换前
class PZXBeforeChangeBrandDetail(models.Model):
    brand_choices = (
        ('置换前', '置换前'),
        ('置换后', '置换后'),)
    progressid = models.ForeignKey('PZXChangeBrandStatus', models.CASCADE, db_column='progressid',to_field='id',verbose_name= '进度状态')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='品牌替换前')
    productid =  models.ForeignKey('PZXMenu', models.CASCADE, db_column='productid',to_field='id',verbose_name= '产品信息:名称_规格_单位_采购价_供应商_品牌',blank=True, null=True)###

    originalsupplier = models.CharField(verbose_name='供应商',help_text=u"请按系统中供应商名称填报",max_length=255, blank=True, null=True)
    originalbrand = models.CharField(verbose_name='品牌',help_text=u"请按系统中品牌名称填报",max_length=255, blank=True, null=True)
    newsupplier = models.CharField(verbose_name='新供应商 ',max_length=255, blank=True, null=True)
    beforeorafterbrandchange = models.CharField(verbose_name='品牌是置换前还是置换后',max_length=255,choices=brand_choices,default='置换前')
    code = models.CharField(verbose_name='产品编码U8 ',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品名称U8',help_text=u"请按系统名称填报",max_length=255, blank=True, null=True)
    spec = models.CharField(verbose_name='规格',max_length=255, blank=True, null=True)
    unit = models.CharField(verbose_name='单位',max_length=255, blank=True, null=True)
    
    pplperunit = models.PositiveIntegerField(verbose_name='每单位人份数(必填)',help_text=u"举例：单位是盒，规格是60T/盒，则该处填60。液体类产品请大家仔细斟酌后填报",validators=[MinValueValidator(1)],default = 0)
    recentsales = models.DecimalField(verbose_name='半年度开票额 ',help_text=u"半年度采购数量/单位 X 每单位人份数 X LIS收费单价 X LIS结算%", max_digits=25, decimal_places=2, blank=True, null=True)
    recentcost = models.DecimalField(verbose_name='半年度采购额',help_text=u"半年度采购数量/单位 X 采购价/单位", max_digits=25, decimal_places=2, blank=True, null=True)
    recentgp = models.DecimalField(verbose_name='半年度盈亏额',max_digits=25, decimal_places=2, blank=True, null=True)
    recentgpofsupplier = models.DecimalField(verbose_name='半年度供应商盈利额',max_digits=25, decimal_places=2, blank=True, null=True)

    lisfee = models.DecimalField(verbose_name='LIS收费价(必填)',max_digits=25, decimal_places=2,validators=[MinValueValidator(0.01)],default = 0)
    lispercent = models.DecimalField(verbose_name='LIS结算比例(必填,≤1)',max_digits=25, decimal_places=3,validators=[MinValueValidator(0.01),MaxValueValidator(1)],default = 0)
    lissettleprice = models.DecimalField(verbose_name='LIS结算价(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    costperunit = models.DecimalField(verbose_name='采购价/单位(报价)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default = 0)
    purchaseqty = models.DecimalField(verbose_name='半年度采购数量/单位',max_digits=25, decimal_places=1,validators=[MinValueValidator(0.1)],default = 0)
    costppl = models.DecimalField(verbose_name='采购价/人份',help_text=u"采购价每单位 / 每单位人份数",max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0)])
    gppercent = models.DecimalField(verbose_name='毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    costfeepercent = models.DecimalField(verbose_name='原采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)    
    
    marketprice = models.DecimalField(verbose_name='市场价/人份(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    marketpricefeepercent = models.DecimalField(verbose_name='市场价占收费比例',max_digits=25, decimal_places=2, blank=True, null=True)
    newcostppl = models.DecimalField(verbose_name='新采购价/人份',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    newcostdroprate = models.DecimalField(verbose_name='新采购价下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newgppercent = models.DecimalField(verbose_name='新毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostfeepercent = models.DecimalField(verbose_name='新采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    targetppl = models.DecimalField(verbose_name='谈判目标/元(必填)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    targetdropdate = models.DecimalField(verbose_name='谈判下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    realmonthlyppl = models.PositiveIntegerField(verbose_name='每月lis开票人份数',default = 0)
    estimatemonthlyppl = models.PositiveIntegerField(verbose_name='预估每月lis开票人份数',default = 0)
    gpgrowthppl = models.DecimalField(verbose_name='毛利额增量/人份',max_digits=25, decimal_places=2, blank=True, null=True)
    estmonthlygpgrowth = models.DecimalField(verbose_name='预估月毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgp = models.DecimalField(verbose_name='月毛利额',max_digits=25, decimal_places=2, blank=True, null=True)
    skuhistory=JSONField(verbose_name='历史sku',blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDBeforeChangeBrandDetail'
        verbose_name_plural = '品牌替换前明细'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 SPD品牌替换前明细删除')
        self.is_active = False
        self.save()


#品牌替换后
class PZXAfterChangeBrandDetail(models.Model):
    brand_choices = (
        ('置换前', '置换前'),
        ('置换后', '置换后'),)
    progressid = models.ForeignKey('PZXChangeBrandStatus', models.CASCADE, db_column='progressid',to_field='id',verbose_name= '进度状态')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='品牌替换后')

    originalsupplier = models.CharField(verbose_name='供应商',help_text=u"请按系统中供应商名称填报",max_length=255, blank=True, null=True)
    originalbrand = models.CharField(verbose_name='品牌',help_text=u"请按系统中品牌名称填报",max_length=255, blank=True, null=True)
    newsupplier = models.CharField(verbose_name='新供应商 ',max_length=255, blank=True, null=True)
    beforeorafterbrandchange = models.CharField(verbose_name='品牌是置换前还是置换后',max_length=255,choices=brand_choices,default='置换后')
    code = models.CharField(verbose_name='产品编码U8 ',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品名称U8',help_text=u"请按系统名称填报",max_length=255, blank=True, null=True)
    spec = models.CharField(verbose_name='规格',max_length=255, blank=True, null=True)
    unit = models.CharField(verbose_name='单位',max_length=255, blank=True, null=True)
    
    pplperunit = models.PositiveIntegerField(verbose_name='每单位人份数(必填)',help_text=u"举例：单位是盒，规格是60T/盒，则该处填60。液体类产品请大家仔细斟酌后填报",validators=[MinValueValidator(1)],default = 0)
    recentsales = models.DecimalField(verbose_name='半年度开票额 ',help_text=u"半年度采购数量/单位 X 每单位人份数 X LIS收费单价 X LIS结算%", max_digits=25, decimal_places=2, blank=True, null=True)
    recentcost = models.DecimalField(verbose_name='半年度采购额',help_text=u"半年度采购数量/单位 X 采购价/单位", max_digits=25, decimal_places=2, blank=True, null=True)
    recentgp = models.DecimalField(verbose_name='半年度盈亏额',max_digits=25, decimal_places=2, blank=True, null=True)
    recentgpofsupplier = models.DecimalField(verbose_name='半年度供应商盈利额',max_digits=25, decimal_places=2, blank=True, null=True)

    lisfee = models.DecimalField(verbose_name='LIS收费价(必填)',max_digits=25, decimal_places=2,validators=[MinValueValidator(0.01)],default = 0)
    lispercent = models.DecimalField(verbose_name='LIS结算比例(必填,≤1)',max_digits=25, decimal_places=3,validators=[MinValueValidator(0.01),MaxValueValidator(1)],default = 0)
    lissettleprice = models.DecimalField(verbose_name='LIS结算价(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    costperunit = models.DecimalField(verbose_name='采购价/单位(报价)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default = 0)
    purchaseqty = models.DecimalField(verbose_name='半年度采购数量/单位',max_digits=25, decimal_places=1,validators=[MinValueValidator(0.1)],default = 0)
    costppl = models.DecimalField(verbose_name='采购价/人份',help_text=u"采购价每单位 / 每单位人份数",max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0)])
    gppercent = models.DecimalField(verbose_name='毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    costfeepercent = models.DecimalField(verbose_name='原采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)    
    
    marketprice = models.DecimalField(verbose_name='市场价/人份(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    marketpricefeepercent = models.DecimalField(verbose_name='市场价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostppl = models.DecimalField(verbose_name='新采购价/人份',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    newcostdroprate = models.DecimalField(verbose_name='新采购价下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newgppercent = models.DecimalField(verbose_name='新毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostfeepercent = models.DecimalField(verbose_name='新采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    targetppl = models.DecimalField(verbose_name='谈判目标/元(必填)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    targetdropdate = models.DecimalField(verbose_name='谈判下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    realmonthlyppl = models.PositiveIntegerField(verbose_name='每月lis开票人份数',default = 0)
    estimatemonthlyppl = models.PositiveIntegerField(verbose_name='预估每月lis开票人份数',default = 0)
    gpgrowthppl = models.DecimalField(verbose_name='毛利额增量/人份',max_digits=25, decimal_places=2, blank=True, null=True)
    estmonthlygpgrowth = models.DecimalField(verbose_name='预估月毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgp = models.DecimalField(verbose_name='月毛利额',max_digits=25, decimal_places=2, blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDAfterChangeBrandDetail'
        verbose_name_plural = '品牌替换后明细'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 SPD品牌替换后明细删除')
        self.is_active = False
        self.save()


#套餐绑定------------

class PZXSetStatus(models.Model):
    completemonth_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12,12))
    progress_choices = (
        ('待谈判', '待谈判'),
        ('已谈判等回复', '已谈判等回复'),
        ('新价格已确认', '新价格已确认'),
      )
    overallid = models.ForeignKey('PZXOverall', models.CASCADE, db_column='overallid',to_field='id',verbose_name= '作战计划')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='套餐绑定')

    progress=models.CharField(verbose_name='进度(必填)',max_length=25,choices=progress_choices,default='待拜访')
   
    completemonth=models.PositiveIntegerField(verbose_name='预计落地月份(默认12月,请修改)',choices=completemonth_choices,default=12)
    monthgpgrowth = models.DecimalField(verbose_name='月毛利额增量预估/元',  max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default=0)
    thisyeargpgrowth = models.DecimalField(verbose_name='23年毛利额增量预估/元',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算月毛利额增量', max_digits=25, decimal_places=2, blank=True, null=True)
    thisyeargpgrowthbydetail = models.DecimalField(verbose_name='根据下方明细计算23年毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)

    target = models.TextField(verbose_name='谈判目标(文字描述,具体金额在下方明细填报)',max_length=255, blank=True, null=True)
    reason = models.TextField(verbose_name='理由',max_length=255, blank=True, null=True)
    
    relation = models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)
    support = models.CharField(verbose_name='所需支持',max_length=255, blank=True, null=True)
    actionplan=models.TextField(verbose_name='行动计划',max_length=255, blank=True, null=True)

    memo = models.TextField(verbose_name='备注',max_length=255, blank=True, null=True)
    advicedirector = models.CharField(verbose_name='倪日磊意见',max_length=255, blank=True, null=True)
    adviceboss = models.CharField(verbose_name='陈海敏意见',max_length=255, blank=True, null=True)
    statushistory=JSONField(verbose_name='历史status',blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)


    class Meta:
        db_table = 'marketing_research_v2\".\"SPDSetStatus'
        verbose_name_plural = '套餐绑定状态'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的套餐绑定状态删除')
        self.is_active = False
        self.save()


class PZXSetDetail(models.Model):
    brand_choices = (
        ('置换前', '置换前'),
        ('置换后', '置换后'),)
    progressid = models.ForeignKey('PZXSetStatus', models.CASCADE, db_column='progressid',to_field='id',verbose_name= '进度状态')
    whygrowth = models.CharField(verbose_name='增量来源',max_length=255,default='套餐绑定明细')

    originalsupplier = models.CharField(verbose_name='供应商',help_text=u"请按系统中供应商名称填报",max_length=255, blank=True, null=True)
    originalbrand = models.CharField(verbose_name='品牌',help_text=u"请按系统中品牌名称填报",max_length=255, blank=True, null=True)
    newsupplier = models.CharField(verbose_name='新供应商 ',max_length=255, blank=True, null=True)
    beforeorafterbrandchange = models.CharField(verbose_name='品牌是置换前还是置换后',max_length=255, blank=True, null=True,choices=brand_choices)
    code = models.CharField(verbose_name='产品编码U8 ',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品名称U8',help_text=u"请按系统名称填报",max_length=255, blank=True, null=True)
    spec = models.CharField(verbose_name='规格',max_length=255, blank=True, null=True)
    unit = models.CharField(verbose_name='单位',max_length=255, blank=True, null=True)
    
    pplperunit = models.PositiveIntegerField(verbose_name='每单位人份数(必填)',help_text=u"举例：单位是盒，规格是60T/盒，则该处填60。液体类产品请大家仔细斟酌后填报",validators=[MinValueValidator(1)],default = 0)
    recentsales = models.DecimalField(verbose_name='半年度开票额 ',help_text=u"半年度采购数量/单位 X 每单位人份数 X LIS收费单价 X LIS结算%", max_digits=25, decimal_places=2, blank=True, null=True)
    recentcost = models.DecimalField(verbose_name='半年度采购额',help_text=u"半年度采购数量/单位 X 采购价/单位", max_digits=25, decimal_places=2, blank=True, null=True)
    recentgp = models.DecimalField(verbose_name='半年度盈亏额',max_digits=25, decimal_places=2, blank=True, null=True)
    recentgpofsupplier = models.DecimalField(verbose_name='半年度供应商盈利额',max_digits=25, decimal_places=2, blank=True, null=True)

    lisfee = models.DecimalField(verbose_name='LIS收费价(必填)',max_digits=25, decimal_places=2,validators=[MinValueValidator(0.01)],default = 0)
    lispercent = models.DecimalField(verbose_name='LIS结算比例(必填,≤1)',max_digits=25, decimal_places=3,validators=[MinValueValidator(0.01),MaxValueValidator(1)],default = 0)
    lissettleprice = models.DecimalField(verbose_name='LIS结算价(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    costperunit = models.DecimalField(verbose_name='采购价/单位(报价)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0.01)],default = 0)
    purchaseqty = models.DecimalField(verbose_name='半年度采购数量/单位',max_digits=25, decimal_places=1,validators=[MinValueValidator(0.1)],default = 0)
    costppl = models.DecimalField(verbose_name='采购价/人份',help_text=u"采购价每单位 / 每单位人份数",max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0)])
    gppercent = models.DecimalField(verbose_name='毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    costfeepercent = models.DecimalField(verbose_name='原采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)    
    
    marketprice = models.DecimalField(verbose_name='市场价/人份(必填)',max_digits=25, decimal_places=2, blank=True, null=True,validators=[MinValueValidator(0.01)],default = 0)
    marketpricefeepercent = models.DecimalField(verbose_name='市场价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostppl = models.DecimalField(verbose_name='新采购价/人份',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    newcostdroprate = models.DecimalField(verbose_name='新采购价下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    newgppercent = models.DecimalField(verbose_name='新毛利率',max_digits=25, decimal_places=4, blank=True, null=True)
    newcostfeepercent = models.DecimalField(verbose_name='新采购价占收费比例',max_digits=25, decimal_places=4, blank=True, null=True)
    targetppl = models.DecimalField(verbose_name='谈判目标/元(必填)',max_digits=25, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    targetdropdate = models.DecimalField(verbose_name='谈判下降比例',max_digits=25, decimal_places=4, blank=True, null=True)
    realmonthlyppl = models.PositiveIntegerField(verbose_name='每月lis开票人份数',default = 0)
    estimatemonthlyppl = models.PositiveIntegerField(verbose_name='预估每月lis开票人份数',default = 0)
    gpgrowthppl = models.DecimalField(verbose_name='毛利额增量/人份',max_digits=25, decimal_places=2, blank=True, null=True)
    estmonthlygpgrowth = models.DecimalField(verbose_name='预估月毛利额增量',max_digits=25, decimal_places=2, blank=True, null=True)
    monthgp = models.DecimalField(verbose_name='月毛利额',max_digits=25, decimal_places=2, blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDSetDetail'
        verbose_name_plural = '套餐绑定明细'
    
    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model中的 SPD套餐绑定明细删除')
        self.is_active = False
        self.save()



#=====================================
class PZXCalculate(models.Model):
    overallid = models.OneToOneField('PZXOverall', models.CASCADE, db_column='overallid',to_field='id',verbose_name= '作战计划')
    estnewgpgrowth = models.DecimalField(verbose_name='新开项目：预估月毛利额增量总计',max_digits=25, decimal_places=2, default=0)
    estnegogpgrowth = models.DecimalField(verbose_name='供应商重新谈判：预估月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    estchannelgpgrowth = models.DecimalField(verbose_name='渠道变更：预估月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    estbrandgpgrowth = models.DecimalField(verbose_name='品牌替换：预估月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    estsetgpgrowth = models.DecimalField(verbose_name='套餐绑定：预估月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    estallgpgrowth = models.DecimalField(verbose_name='所有业务：预估月毛利额增量',max_digits=25, decimal_places=2,  default=0)
    realnewgpgrowth = models.DecimalField(verbose_name='新开项目：实际月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    newgpgrowthpercent = models.DecimalField(verbose_name='新开项目：毛利额增量完成率',max_digits=25, decimal_places=2,  default=0)
    realnegogpgrowth = models.DecimalField(verbose_name='供应商重新谈判：实际月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    negogpgrowthpercent = models.DecimalField(verbose_name='供应商重新谈判：毛利额增量完成率',max_digits=25, decimal_places=2,  default=0)
    realchannelgpgrowth = models.DecimalField(verbose_name='渠道变更：实际月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    channelgpgrowthpercent = models.DecimalField(verbose_name='渠道变更：毛利额增量完成率',max_digits=25, decimal_places=2,  default=0)
    realbrandgpgrowth = models.DecimalField(verbose_name='品牌替换：实际月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    brandgpgrowthpercent = models.DecimalField(verbose_name='品牌替换：毛利额增量完成率',max_digits=25, decimal_places=2,  default=0)
    realsetgpgrowth = models.DecimalField(verbose_name='套餐绑定：实际月毛利额增量总计',max_digits=25, decimal_places=2,  default=0)
    setgpgrowthpercent = models.DecimalField(verbose_name='套餐绑定：毛利额增量完成率',max_digits=25, decimal_places=2,  default=0)
    realallgpgrowth = models.DecimalField(verbose_name='所有业务：实际月毛利额增量',max_digits=25, decimal_places=2,  default=0)
    allgpgrowthpercent = models.DecimalField(verbose_name='所有业务：毛利额增量完成率',max_digits=25, decimal_places=2,  default=0)
    
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDCalculate'
        verbose_name_plural = '作战计划计算表'
    
 
#========
#普中心大菜单给供应商重新谈判的筛选用的
class PZXMenu(models.Model):
    overallid = models.ForeignKey('PZXOverall', models.CASCADE, db_column='overallid',to_field='id',verbose_name= '主表id',default=0)

    customer = models.CharField(verbose_name='客户',max_length=255, default='普中心')
    department = models.CharField(verbose_name='科室',max_length=255, blank=True, null=True)
    semidepartment = models.CharField(verbose_name='使用科室',max_length=255, blank=True, null=True)

    category1 = models.CharField(verbose_name='大类',max_length=255, blank=True, null=True)
    category2 = models.CharField(verbose_name='小类',max_length=255, blank=True, null=True)
    project = models.CharField(verbose_name='项目大类',max_length=255, blank=True, null=True)
        
    code = models.CharField(verbose_name='产品编码U8',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品名称U8',max_length=255, blank=True, null=True)
    spec = models.CharField(verbose_name='规格',max_length=255, blank=True, null=True)
    unit = models.CharField(verbose_name='单位',max_length=255, blank=True, null=True)
    brand = models.CharField(verbose_name='品牌',max_length=255, blank=True, null=True)
    supplier = models.CharField(verbose_name='供应商',max_length=255, blank=True, null=True)
    costperunit = models.DecimalField(verbose_name='采购价/单位',max_digits=25, decimal_places=2,default = 0)
    priceperunit = models.DecimalField(verbose_name='销售价/单位',max_digits=25, decimal_places=2,default = 0)
    purchaseqty = models.DecimalField(verbose_name='1-6月采购数量',max_digits=25, decimal_places=2,default = 0)
    purchasesum = models.DecimalField(verbose_name='1-6月采购金额（订单跟踪）',max_digits=25, decimal_places=2,default = 0)
    theoreticalvalue = models.DecimalField(verbose_name='理论销售金额（根据售价反推）',max_digits=25, decimal_places=2,default = 0)
    theoreticalgp = models.DecimalField(verbose_name='理论毛利润',max_digits=25, decimal_places=2,default = 0)
    theoreticalgppercent = models.DecimalField(verbose_name='理论毛利率',max_digits=25, decimal_places=4,default = 0)

    machinemodel = models.CharField(verbose_name='仪器型号',max_length=255, blank=True, null=True)
    machinebrand = models.CharField(verbose_name='仪器品牌',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDPZXMenu'
        verbose_name_plural = '普中心大菜单作筛选'
    def __str__(self):
        # return ('供应商:{}, 品牌:{}, 产品名称:{}, 规格:{}, 单位:{}'.format(self.supplier,self.brand,self.product,self.spec,self.unit))
        return ('{}__{}__单位:{}__采购价:{}__{}__{}'.format(self.product,self.spec,self.unit,self.costperunit,self.supplier,self.brand))
    


#普中心大菜单给inline展示用的
class PZXMenuforinline(models.Model):
    overallid = models.ForeignKey('PZXOverall', models.CASCADE, db_column='overallid',to_field='id',verbose_name= '主表id',default=1)

    customer = models.CharField(verbose_name='客户',max_length=255, default='普中心')
    department = models.CharField(verbose_name='科室',max_length=255, blank=True, null=True)
    semidepartment = models.CharField(verbose_name='使用科室',max_length=255, blank=True, null=True)

    category1 = models.CharField(verbose_name='大类',max_length=255, blank=True, null=True)
    category2 = models.CharField(verbose_name='小类',max_length=255, blank=True, null=True)
    project = models.CharField(verbose_name='项目大类',max_length=255, blank=True, null=True)
    supplier = models.CharField(verbose_name='供应商',max_length=255, blank=True, null=True)   
    brand = models.CharField(verbose_name='品牌',max_length=255, blank=True, null=True)

    code = models.CharField(verbose_name='产品编码U8',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品名称U8',max_length=255, blank=True, null=True)
    spec = models.CharField(verbose_name='规格',max_length=255, blank=True, null=True)
    unit = models.CharField(verbose_name='单位',max_length=255, blank=True, null=True)
   
    costperunit = models.DecimalField(verbose_name='采购价/单位',max_digits=25, decimal_places=2,default = 0)
    priceperunit = models.DecimalField(verbose_name='销售价/单位',max_digits=25, decimal_places=2,default = 0)
    purchaseqty = models.DecimalField(verbose_name='1-6月采购数量',max_digits=25, decimal_places=2,default = 0)
    purchasesum = models.DecimalField(verbose_name='1-6月采购金额（订单跟踪）',max_digits=25, decimal_places=2,default = 0)
    theoreticalvalue = models.DecimalField(verbose_name='理论销售金额（根据售价反推）',max_digits=25, decimal_places=2,default = 0)
    theoreticalgp = models.DecimalField(verbose_name='理论毛利润',max_digits=25, decimal_places=2,default = 0)
    theoreticalgppercent = models.DecimalField(verbose_name='理论毛利率',max_digits=25, decimal_places=2,default = 0)

    machinemodel = models.CharField(verbose_name='仪器型号',max_length=255, blank=True, null=True)
    machinebrand = models.CharField(verbose_name='仪器品牌',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"SPDPZXMenuforinline'
        verbose_name_plural = '普中心大菜单作展示'



# #projectvalues 项目大类的金额表  
# class ProjectValue(models.Model):
#     projectvalueid=models.OneToOneField('PZXOverall', models.CASCADE, db_column='projectvalueid',to_field='projectvalueid',verbose_name= '项目大类相关金额')

#     purchasesum = models.DecimalField(verbose_name='采购金额',max_digits=25, decimal_places=4,default = 0)
#     purchasesumpercent = models.DecimalField(verbose_name='该项目占总采购额占比',max_digits=25, decimal_places=4,default = 0)

#     theoreticalvalue = models.DecimalField(verbose_name='理论销售金额',max_digits=25, decimal_places=4,default = 0)
#     theoreticalgp = models.DecimalField(verbose_name='理论毛利润',max_digits=25, decimal_places=4,default = 0)
#     theoreticalgppercent = models.DecimalField(verbose_name='理论毛利率',max_digits=25, decimal_places=4,default = 0)

#     createtime = models.DateTimeField(auto_now_add=True)
#     updatetime = models.DateTimeField(auto_now=True)
#     is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

#     class Meta:
#         db_table = 'marketing_research_v2\".\"SPDPZXProjectValue'
#         verbose_name_plural = '普中心项目大类金额'


# #suppliervalues 项目大类下的供应商的金额表   
# class SupplierValue(models.Model):
#     suppliervalueid=models.OneToOneField('PZXOverall', models.CASCADE, db_column='suppliervalueid',to_field='id',verbose_name= '供应商相关金额')

#     purchasesum = models.DecimalField(verbose_name='采购金额',max_digits=25, decimal_places=4,default = 0)
#     purchasesumpercentinproject = models.DecimalField(verbose_name='项目中各供应商采购额占比',max_digits=25, decimal_places=4,default = 0)

#     theoreticalvalue = models.DecimalField(verbose_name='理论销售金额',max_digits=25, decimal_places=4,default = 0)
#     theoreticalgp = models.DecimalField(verbose_name='理论毛利润',max_digits=25, decimal_places=4,default = 0)
#     theoreticalgppercent = models.DecimalField(verbose_name='理论毛利率',max_digits=25, decimal_places=4,default = 0)

#     createtime = models.DateTimeField(auto_now_add=True)
#     updatetime = models.DateTimeField(auto_now=True)
#     is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

#     class Meta:
#         db_table = 'marketing_research_v2\".\"SPDPZXSupplierValue'
#         verbose_name_plural = '普中心项目大类-供应商金额'