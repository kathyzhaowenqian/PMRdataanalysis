from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse,HttpResponse
from Marketing_Research.models import *
from Marketing_Research.tools.PMRBigScreenAPI.PMRBigScreenModel import *
import numpy as np
import json
from json.encoder import JSONEncoder
from decimal import Decimal

#解决pandas和json格式不兼容的问题
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj,Decimal):
            return float(obj)
        elif isinstance(obj,bytes):
           return str(obj,encoding='utf-8')
        
        else:
            return super(NpEncoder, self).default(obj)

# 继承 View

class WDANALYSIS(View):

    def get(self, request):
        login_user = request.user.chinesename
        view_group_list = ['boss','WDmanager','pmrmanager','pmrdirectsales','allviewonly']
        user_in_group_list = request.user.groups.values('name')

        
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in view_group_list :
                return render(request, 'WDanalysis/index.html')
        if request.user.username=='admin':
            return render(request, 'WDanalysis/index.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')
        

class WDANALYSISDETAIL(View):
	# 定义 get 方法
    def get(self,request):
    
        login_user = request.user.chinesename
        view_group_list = ['boss','WDmanager','pmrmanager','pmrdirectsales','allviewonly']
        user_in_group_list = request.user.groups.values('name')
        print(user_in_group_list)

        Wholeresearchlist_queryset = Wholeresearchlist.objects.all()#从视图中拿出所有
        Wholeresearchlist_df = Wholeresearchlist_queryset.to_dataframe()
        year='2024'
        company='卫顿'
        raw_data=InitData(Wholeresearchlist_df,year,company)

        projectname = request.GET.get('project')
        print(projectname,'ajax')                    
        if projectname !='undefined' and projectname !='所有项目':
            print(projectname)
            raw_data=InitProjectData(Wholeresearchlist_df,year,company,projectname)


        dashboarddata_whole= RunWholeCompany(raw_data)
        dashboarddata_whole['code']=200
        
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in view_group_list :
                return JsonResponse(json.dumps(dashboarddata_whole, cls=NpEncoder,ensure_ascii=False),safe=False,charset='utf-8' )
        if request.user.username=='admin':
            return JsonResponse(json.dumps(dashboarddata_whole, cls=NpEncoder,ensure_ascii=False),safe=False,charset='utf-8' )

        


        # # 返回json 字符串给前端
        # return render(request,'PMRanalysis/index.html',locals())
    
    # 定义 get 方法 
    def post(self,request):
       pass