# from Marketing_Research_QT.models import *
# from import_export import fields, resources,widgets
# from import_export.widgets import ForeignKeyWidget
# from django.db.models import Count, Case, When, IntegerField



# class PMRResearchDetailResource(resources.ModelResource):
#     # uniquestring = fields.Field(
#     #     column_name='唯一值',
#     #     attribute='researchlist',
#     #     widget=ForeignKeyWidget(PMRResearchList3, field='uniquestring'))
    
#     class Meta:
#         model = PMRResearchDetail3
#         fields = ('ownbusiness','machinemodel','machineseries')


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
    

#     q1target = fields.Field(
#         column_name='Q1目标',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q1target', separator='|')
#     )

#     q1actualsales = fields.Field(
#         column_name='Q1实际开票',
#         attribute='salestarget3_set',
#         widget= widgets.ManyToManyWidget(SalesTargetResource, field='q1actualsales', separator='|')
#     )

#     machinemodels=fields.Field(
#         column_name='仪器型号',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='machinemodel', separator='|')
#     )
#     machineseries=fields.Field(
#         column_name='仪器序列号',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='machineseries', separator='|')
#     )
#     installdates=fields.Field(
#         column_name='装机时间',
#         attribute='pmrresearchdetail3_set',
#         widget= widgets.ManyToManyWidget(PMRResearchDetailResource, field='installdate', separator='|')
#     )

   
#     class Meta:
#         model = PMRResearchList3
#         fields = ('company','district','hospitalclass','hospitalname','salesman1','salesman2','contactname','contactmobile','q1target','q1actualsales','machinemodels','installdates')

#     def dehydrate_q1target(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q1target) for sales_target in sales_targets])
    
#     def dehydrate_q1actualsales(self, obj):
#         sales_targets = obj.salestarget3_set.filter(year='2023',is_active=True)
#         return '|'.join([str(sales_target.q1actualsales) for sales_target in sales_targets])

