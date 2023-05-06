# from Marketing_Research_QT.models import *
# from import_export import fields, resources,widgets
# from import_export.widgets import ForeignKeyWidget
# from django.db.models import Count, Case, When, IntegerField
# from django.db.models import Q
# from datetime import datetime
# from import_export.formats import base_formats
# from django.utils.encoding import smart_str


# class CustomBooleanWidget(widgets.BooleanWidget):
#     def __init__(self, true_value='是', false_value='否', *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.true_value = true_value
#         self.false_value = false_value
#     def render(self, value, obj=None):
#         if value is None:
#             return ''
#         return self.true_value if value else self.false_value
    
# class PMRResearchDetailResource(resources.ModelResource):
#     company = fields.Field(
#         column_name='公司',
#         attribute='researchlist',
#         widget=ForeignKeyWidget(PMRResearchList3, field='company'))
    
#     district = fields.Field(
#         column_name='地区',
#         attribute='researchlist__hospital__district',
#     )
#     hospitalclass = fields.Field(
#         column_name='医院级别',
#         attribute='researchlist__hospital__hospitalclass',
#     )
#     hospitalname = fields.Field(
#         column_name='医院名称',
#         attribute='researchlist__hospital__hospitalname',
#     )
    
#     salesman1 = fields.Field(
#         column_name='第一负责人',
#         attribute='researchlist__salesman1__chinesename',
#     )
#     salesman2 = fields.Field(
#         column_name='第二负责人',
#         attribute='researchlist__salesman2__chinesename',
#     )
#     project = fields.Field(
#         column_name='项目',
#         attribute='researchlist__project__project',
#     )
#     detailedproject = fields.Field(attribute='detailedproject', column_name='细分项目')

#     ownbusiness = fields.Field(
#         attribute='ownbusiness',
#         column_name='是否我司业务',
#         widget=CustomBooleanWidget()
#     )

#     brand = fields.Field(
#         column_name='品牌',
#         attribute='brand',
#         widget=ForeignKeyWidget(Brand, field='brand'))
    
#     machinemodel = fields.Field(attribute='machinemodel', column_name='仪器型号')
#     machineseries = fields.Field(attribute='machineseries', column_name='序列号')
#     machinenumber = fields.Field(attribute='machinenumber', column_name='仪器数量')
#     installdate = fields.Field(attribute='installdate', column_name='装机时间')
#     expiration = fields.Field(attribute='expiration', column_name='装机时效')
#     testprice = fields.Field(attribute='testprice', column_name='单价')
#     endsupplier = fields.Field(attribute='endsupplier', column_name='终端开票商')

#     competitionrelation = fields.Field(
#         column_name='竞品关系点',
#         attribute='competitionrelation',
#         widget=ForeignKeyWidget(CompetitionRelation, field='competitionrelation'))
    
#     class Meta:
#         model = PMRResearchDetail3
#         fields = ('company','district','hospitalclass','hospitalname','salesman1','salesman2','project','detailedproject','ownbusiness','brand','machinemodel','machineseries','machinenumber','installdate','expiration','testprice','endsupplier','competitionrelation')






# class SalesTargetResource(resources.ModelResource):
#     class Meta:
#         model = SalesTarget3


# class PMRResearchListResource(resources.ModelResource):

#     company = fields.Field(
#         column_name='公司',
#         attribute='company',
#         widget=ForeignKeyWidget(Company, field='company'))
    
#     district = fields.Field(
#         column_name='地区',
#         attribute='hospital',
#         widget=ForeignKeyWidget(Hospital, field='district'))

#     hospitalclass = fields.Field(
#         column_name='医院级别',
#         attribute='hospital',
#         widget=ForeignKeyWidget(Hospital, field='hospitalclass'))
    
#     hospitalname = fields.Field(
#         column_name='医院名称',
#         attribute='hospital',
#         widget=ForeignKeyWidget(Hospital, field='hospitalname'))
        
#     salesman1 = fields.Field(
#         column_name='第一负责人',
#         attribute='salesman1',
#         widget=ForeignKeyWidget(UserInfo3, field='chinesename'))
   
#     salesman2 = fields.Field(
#         column_name='第二负责人',
#         attribute='salesman2',
#         widget=ForeignKeyWidget(UserInfo3, field='chinesename'))
    
#     contactname = fields.Field(attribute='contactname', column_name='联系人')
#     contactmobile = fields.Field(attribute='contactmobile', column_name='联系电话')
#     salesmode = fields.Field(attribute='salesmode', column_name='销售模式')

#     testspermonth = fields.Field(attribute='tetspermonth', column_name='月总测试数')
#     owntestspermonth = fields.Field(attribute='owntestspermonth', column_name='我司月测试数')
#     saleschannel = fields.Field(attribute='saleschannel', column_name='销售路径')
#     support = fields.Field(attribute='support', column_name='所需支持')
#     adminmemo = fields.Field(attribute='memo', column_name='备注')


#     q1actualsales = fields.Field(
#         column_name='Q1实际开票',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q1actualsales', separator='|')
#     )

#     q2target = fields.Field(
#         column_name='Q2目标',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q2target', separator='|')
#     )
#     q2completemonth = fields.Field(
#         column_name='Q2目标完成月',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q2completemonth', separator='|')
#     )
#     q2actualsales = fields.Field(
#         column_name='Q2实际开票',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q2actualsales', separator='|')
#     )

#     q2finishrate = fields.Field(
#         column_name='Q2完成率',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q2finishrate', separator='|')
#     )

#     q3target = fields.Field(
#         column_name='Q3目标',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q3target', separator='|')
#     )
#     q3completemonth = fields.Field(
#         column_name='Q3目标完成月',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q3completemonth', separator='|')
#     )
#     q3actualsales = fields.Field(
#         column_name='Q3实际开票',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q3actualsales', separator='|')
#     )

#     q3finishrate = fields.Field(
#         column_name='Q3完成率',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q3finishrate', separator='|')
#     )

#     q4target = fields.Field(
#         column_name='Q4目标',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q4target', separator='|')
#     )
#     q4completemonth = fields.Field(
#         column_name='Q4目标完成月',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q4completemonth', separator='|')
#     )
#     q4actualsales = fields.Field(
#         column_name='Q4实际开票',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q4actualsales', separator='|')
#     )

#     q4finishrate = fields.Field(
#         column_name='Q4完成率',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q4finishrate', separator='|')
#     )


#     totalmachinenumber = fields.Field(
#         column_name='仪器总数',
#         attribute='detailcalculate3__totalmachinenumber',
#     )
#     ownmachinenumber = fields.Field(
#         column_name='我司仪器数',
#         attribute='detailcalculate3__ownmachinenumber',
#     )
#     ownmachinepercent= fields.Field(
#         column_name='我司仪器占比',
#         attribute='detailcalculate3__ownmachinepercent',
#     )
#     newold= fields.Field(
#         column_name='业务类型',
#         attribute='detailcalculate3__newold',
#     )
#     totalsumpermonth= fields.Field(
#         column_name='22年月均开票额',
#         attribute='detailcalculate3__totalsumpermonth',
#     )

#     detailedprojects=fields.Field(
#         column_name='细分项目',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='detailedproject', separator='|')
#     )
#     ownbusinesses=fields.Field(
#         column_name='是否我司业务',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='ownbusiness', separator='|')
#     )
#     brands=fields.Field(
#         column_name='品牌',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='brand', separator='|')
#     )

#     machinenumbers=fields.Field(
#         column_name='仪器数量',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='machinenumber', separator='|')
#     )
#     machinemodels=fields.Field(
#         column_name='仪器型号',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='machinemodel', separator='|')
#     )

#     machineserieses=fields.Field(
#         column_name='仪器序列号',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='machineseries', separator='|')
#     )
#     installdates=fields.Field(
#         column_name='装机时间',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='installdate', separator='|')
#     )

#     competitionrelations=fields.Field(
#         column_name='竞品关系点',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='competitionrelation', separator='|')
#     )
   
#     class Meta:
#         model = PMRResearchList3
#         fields = ('company','district','hospitalclass','hospitalname','salesman1','salesman2',
#                   'contactname','contactmobile','salesmode','testspermonth','owntestspermonth',
#                   'saleschannel','support','adminmemo',
#                   'q1actualsales','q2target','q2completemonth','q2actualsales','q2finishrate',
#                   'q3target','q3completemonth','q3actualsales','q3finishrate',
#                   'q4target','q4completemonth','q4actualsales','q4finishrate',
#                   'totalmachinenumber','ownmachinenumber','ownmachinepercent',
#                   'newold','totalsumpermonth',
#                   'detailedprojects','ownbusinesses','brands','machinenumbers',
#                   'machinemodels','machineserieses','installdates','competitionrelations')



    
#     def dehydrate_q1actualsales(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q1actualsales) for sales_target in sales_targets])
    
#     def dehydrate_q2actualsales(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q2actualsales) for sales_target in sales_targets])
    
#     def dehydrate_q3actualsales(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q3actualsales) for sales_target in sales_targets])
    
#     def dehydrate_q4actualsales(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q4actualsales) for sales_target in sales_targets])
            
#     def dehydrate_q2target(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q2target) for sales_target in sales_targets])
    
#     def dehydrate_q3target(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q3target) for sales_target in sales_targets])
    
#     def dehydrate_q4target(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q4target) for sales_target in sales_targets])
    
#     def dehydrate_q1completemonth(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q1completemonth) for sales_target in sales_targets])
    
#     def dehydrate_q2completemonth(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q2completemonth) for sales_target in sales_targets])
    
#     def dehydrate_q3completemonth(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q3completemonth) for sales_target in sales_targets])
    
#     def dehydrate_q4completemonth(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q4completemonth) for sales_target in sales_targets])
    
#     def dehydrate_q1finishrate(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q1finishrate) for sales_target in sales_targets])
    
#     def dehydrate_q2finishrate(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q2finishrate) for sales_target in sales_targets])
    
#     def dehydrate_q3finishrate(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q3finishrate) for sales_target in sales_targets])
    
#     def dehydrate_q4finishrate(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q4finishrate) for sales_target in sales_targets])
            
#     def dehydrate_detailedprojects(self, obj):
#         datas = obj.pmrresearchdetail3_set.filter(Q(is_active=True)&~Q(machinenumber=0))
#         return '|'.join([str(i.detailedproject) for i in datas])
    
#     def dehydrate_ownbusinesses(self, obj):
#         datas = obj.pmrresearchdetail3_set.filter(Q(is_active=True)&~Q(machinenumber=0))
#         return '|'.join([str(i.ownbusiness) for i in datas])
    
        
#     def dehydrate_brands(self, obj):
#         datas = obj.pmrresearchdetail3_set.filter(Q(is_active=True)&~Q(machinenumber=0))
#         return '|'.join([str(i.brand) for i in datas])
    
#     def dehydrate_machinenumbers(self, obj):
#         datas = obj.pmrresearchdetail3_set.filter(Q(is_active=True)&~Q(machinenumber=0))
#         return '|'.join([str(i.machinenumber) for i in datas])
    
#     def dehydrate_machinemodels(self, obj):
#         datas = obj.pmrresearchdetail3_set.filter(Q(is_active=True)&~Q(machinenumber=0))
#         return '|'.join([str(i.machinemodel) for i in datas])

#     def dehydrate_machineserieses(self, obj):
#         datas = obj.pmrresearchdetail3_set.filter(Q(is_active=True)&~Q(machinenumber=0))
#         return '|'.join([str(i.machineseries) for i in datas])

#     def dehydrate_installdates(self, obj):
#         datas = obj.pmrresearchdetail3_set.filter(Q(is_active=True)&~Q(machinenumber=0))
#         return '|'.join([str(i.installdate) for i in datas])
    
#     def dehydrate_competitionrelations(self, obj):
#         datas = obj.pmrresearchdetail3_set.filter(Q(is_active=True)&~Q(machinenumber=0))
#         return '|'.join([str(i.competitionrelation) for i in datas])
    
