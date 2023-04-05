from django.db import models
from Marketing_Research.models import UserInfo

# Create your models here.
class UserInfojc(UserInfo):
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



class JCResearchList(models.Model):
    jicheng_choices=(
        ('是', '是'),
        ('否', '否'),
        ('未知', '未知'),
    )
    hospital = models.ForeignKey('Hospital', models.CASCADE, db_column='hospital',to_field='id',verbose_name= '医院')
    director=models.CharField(verbose_name='院长姓名',max_length=255,null=True,blank=True)
    sizeofclinicallab=models.CharField(verbose_name='检验科规模',max_length=255,null=True,blank=True)
    jcornot=models.CharField(verbose_name='是否集成',max_length=255,choices=jicheng_choices)
    jccompany=models.CharField(verbose_name='集成配送公司',max_length=255,null=True,blank=True)
    jcstartdate = models.DateField(verbose_name='集成开始时间',blank=True, null=True,help_text=u'例: 2023/02/01')
    jcenddate = models.DateField(verbose_name='集成截止时间',blank=True, null=True,help_text=u'例: 2023/02/01')
    jcmemo=models.CharField(verbose_name='集成备注',max_length=255,null=True,blank=True)
    sizeofsystem=models.CharField(verbose_name='生化免疫流水线规模',max_length=255,null=True,blank=True)
    brand = models.ForeignKey('Brand', models.CASCADE, db_column='brand',to_field='id',verbose_name= '品牌',null=True,blank=True)
    systemstartdate = models.DateField(verbose_name='流水线开始时间',blank=True, null=True,help_text=u'例: 2023/02/01')
    systemenddate = models.DateField(verbose_name='流水线截止时间',blank=True, null=True,help_text=u'例: 2023/02/01')
    systemmemo=models.CharField(verbose_name='流水线备注',max_length=255,null=True,blank=True)
    relation=models.CharField(verbose_name='关系点',max_length=255,null=True,blank=True)
    operator = models.ForeignKey('UserInfojc', models.CASCADE, db_column='operator',to_field='id',related_name='operatorjc',verbose_name= '最后操作人')

    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)

    class Meta:
        db_table = 'marketing_research_v2\".\"JCResearchList'
        verbose_name_plural = '集成调研表'

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        print(self,'我在model.py的删除') 
        self.is_active = False
        self.save()