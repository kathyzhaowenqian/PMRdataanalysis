
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.forms import Textarea
from Marketing_Research.models import UserInfo
from multiselectfield import MultiSelectField



def get_company_default_value():
    return Company.objects.get(id=1).company



class UserInfoPMRKA(UserInfo):
    
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





class SalesmanPositionPMRKA(models.Model):
    # id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('UserInfoPMRKA', models.CASCADE, db_column='user',to_field='id') #settings.AUTH_USER_MODEL
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_company_default_value)
    position = models.CharField(verbose_name='岗位',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        managed=False
        db_table = 'marketing_research_v2\".\"SalesmanPosition'
        verbose_name_plural = '员工职位列表'





class PMRResearchListPMRKA(models.Model):
    
    # id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey('Company', models.CASCADE, db_column='company',to_field='id',verbose_name= '公司',default=get_company_default_value)
    hospital = models.ForeignKey('Hospital', models.CASCADE, db_column='hospital',to_field='id',verbose_name= '医院')
    salesman = models.ForeignKey('UserInfoPMRKA', models.CASCADE, db_column='salesman',to_field='id',related_name='salesmanPMRKA',verbose_name= '填报人')
    brand=models.TextField(verbose_name='涉及品牌',max_length=500, blank=True, null=True)
    
    machinenumber = models.PositiveIntegerField(verbose_name='仪器数量',default = 0)
    ownmachinenumber = models.PositiveIntegerField(verbose_name='我司仪器数量',default = 0)
    ownmachinenumberpercent = models.DecimalField(verbose_name='我司仪器数占比',max_digits=25, decimal_places=2, blank=True, null=True)

    testspermonth = models.PositiveIntegerField(verbose_name='月测试数',default = 0)
    owntestspermonth = models.PositiveIntegerField(verbose_name='我司月测试数',default = 0)
    owntestspermonthpercent = models.DecimalField(verbose_name='我司测试数占比',max_digits=25, decimal_places=2, blank=True, null=True)

    salestotal = models.DecimalField(verbose_name='年开票额',max_digits=25, decimal_places=2, default = 0)
    ownsalestotal = models.DecimalField(verbose_name='我司年开票额',max_digits=25, decimal_places=2, blank=True, null=True)
    ownsalestotalpercent = models.DecimalField(verbose_name='我司开票占比',max_digits=25, decimal_places=2, blank=True, null=True)

    department = models.TextField(verbose_name='科室',max_length=255, blank=True, null=True)
    product=models.TextField(verbose_name='产品',max_length=255, blank=True, null=True)
    supplier = models.TextField(verbose_name='供应商',max_length=255, blank=True, null=True)
    relation=models.TextField(verbose_name='关系点',max_length=255, blank=True, null=True)
    newold = models.CharField(verbose_name='业务类型',max_length=255, blank=True, null=True)

    operator = models.ForeignKey('UserInfoPMRKA', models.CASCADE, db_column='operator',to_field='id',related_name='operatorPMRKA',verbose_name= '最后操作人')
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"KA_PMRResearchList'
        verbose_name_plural = '市场调研列表'
    
    # def __str__(self):
    #     return self.hospital

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model.py的删除') 
        self.is_active = False
        self.save()
        #可以把相关联得 Objects 也一起伪删除
        PMRResearchDetailPMRKA.objects.filter(researchlist=self).update(is_active=False)




class PMRResearchDetailPMRKA(models.Model):
    ownbusiness_choices = (
        (True, '是'),
        (False, '否'),)
    researchlist = models.ForeignKey('PMRResearchListPMRKA', models.CASCADE, db_column='researchlist',to_field='id',verbose_name= '调研列表')
    brand = models.ForeignKey('Brand', models.CASCADE, db_column='brand',to_field='id',verbose_name= '品牌',null=True)
    ownbusiness=models.BooleanField(verbose_name='是否我司业务',null=False, default = False,choices=ownbusiness_choices)

    department = models.CharField(verbose_name='科室',max_length=255, blank=True, null=True)
    product = models.CharField(verbose_name='产品',max_length=255, blank=True, null=True)

    machinemodel = models.CharField(verbose_name='仪器型号',max_length=255, blank=True, null=True)
    machinenumber = models.PositiveIntegerField(verbose_name='仪器数量',default = 1)
    installdate = models.DateField(verbose_name='装机日期',blank=True, null=True,help_text=u'例: 2023/09/01')
    expiration=models.CharField(verbose_name='装机时间',max_length=255, blank=True, null=True)
    
    testsperday = models.PositiveIntegerField(verbose_name='日测试数',default = 0)
    salestotal = models.DecimalField(verbose_name='年开票额',max_digits=25, decimal_places=2, default = 0)

    supplier = models.CharField(verbose_name='供应商',max_length=255, blank=True, null=True)
    relation=models.CharField(verbose_name='关系点',max_length=255, blank=True, null=True)
    adminmemo=models.TextField(verbose_name='备注',max_length=500, blank=True, null=True)

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"KA_PMRResearchDetail'
        verbose_name_plural = '市场调研详情表'

    def delete(self, using=None, keep_parents=False):
        #即使在inline中也是假删除
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model删除')
        self.is_active = False
        self.save()



# class DetailCalculatePMRKA(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     researchlist = models.OneToOneField('PMRResearchListPMRKA', models.CASCADE, db_column='researchlist',to_field='id',verbose_name= '调研列表')
#     totalmachinenumber = models.PositiveIntegerField(verbose_name='仪器总数',default = 0)
#     ownmachinenumber = models.PositiveIntegerField(verbose_name='我司仪器总数',default = 0)
#     ownmachinepercent = models.DecimalField(verbose_name='我司仪器数占比',max_digits=25, decimal_places=2, blank=True, null=True)
#     newold=models.CharField(verbose_name='业务类型',max_length=255, blank=True, null=True)
#     totalsumpermonth = models.DecimalField(verbose_name='22年我司月均销售额总计',max_digits=25, decimal_places=2, blank=True, null=True,default = 0)

#     detailedprojectcombine=models.CharField(verbose_name='项目细分集合',max_length=255, blank=True, null=True)
#     ownbusinesscombine=models.CharField(verbose_name='是否我司业务集合',max_length=255, blank=True, null=True)
#     brandscombine=models.CharField(verbose_name='品牌集合',max_length=255, blank=True, null=True)
#     machinemodelcombine=models.CharField(verbose_name='仪器型号集合',max_length=255, blank=True, null=True)
#     machineseriescombine=models.CharField(verbose_name='序列号集合',max_length=255, blank=True, null=True)
#     installdatescombine = models.CharField(verbose_name='装机时间集合',max_length=255, blank=True, null=True)
#     competitionrelationcombine = models.CharField(verbose_name='竞品关系点集合',max_length=255, blank=True, null=True)
#     machinenumbercombine = models.CharField(verbose_name='仪器数量集合',max_length=255, blank=True, null=True)

#     createtime = models.DateTimeField(auto_now_add=True)
#     updatetime = models.DateTimeField(auto_now=True)
#     is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

#     class Meta:
#         db_table = 'marketing_research_v2\".\"KA_PMRDetailCalculate'
#         verbose_name_plural = '项目统计结果表'






