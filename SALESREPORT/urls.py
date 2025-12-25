"""
SALESREPORT URL配置
"""

from django.urls import path, re_path
from SALESREPORT.views import Submit, ProjectAPI, CustomerAPI
from SALESREPORT.funnel_analysis import (
    funnel_analysis_view, funnel_data_api, salesman_performance_api
)

urlpatterns = [
    # 日报提交
    path('reportsubmit', Submit.as_view(), name='report_submit'),

    # API接口
    path('api/projects/', ProjectAPI.as_view(), name='api_projects_list'),
    re_path(r'^api/projects/(?P<project_id>\d+)/$', ProjectAPI.as_view(), name='api_project_detail'),
    path('api/customers/', CustomerAPI.as_view(), name='api_customers_list'),

    # 漏斗分析
    path('funnel/', funnel_analysis_view, name='funnel_analysis'),
    path('api/funnel-data/', funnel_data_api, name='funnel_data_api'),
    path('api/salesman-performance/', salesman_performance_api, name='salesman_performance_api'),
]
