from django.shortcuts import render
# Create your views here.
from django.views import View
from django.http import JsonResponse,HttpResponse
from PUZHONGXIN.models import *
import numpy as np
import json
from json.encoder import JSONEncoder
from decimal import Decimal
from django.http import JsonResponse

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
        
# Create your views here.
class PZXgantt(View):

    def get(self, request):
        # login_user = request.user.chinesename
        # view_group_list = ['boss','pmronlyview','pmrmanager','pmrdirectsales','allviewonly']
        # user_in_group_list = request.user.groups.values('name')

        
        # for user_in_group_dict in user_in_group_list:
        #     if user_in_group_dict['name'] in view_group_list :
        #         return render(request, 'PMRanalysis/index.html')
            
        # if request.user.username=='admin':
            return render(request, 'PUZHONGXIN/gantt2.html')
        # else:
        #     return HttpResponse('您好，目前您暂无权限访问')
        
    def post(self,request):
        
        username = request.user.username
        NegotiationStatus_queryset = PZXNegotiationStatus.objects.values('statushistory')
        Negotiationdatas = [item['statushistory'] for item in NegotiationStatus_queryset]
        Negotiationsource=[]
        for i in Negotiationdatas:
            eachsource={}
            result = []
            current_item = {}
            
            for item in i:
                datetime=item['time'].split()[0]
                if not current_item:
                    current_item = {'from': datetime, 'to': datetime, 'label': item['status']}
                elif item['status'] == current_item['label']:
                    current_item['to'] = datetime
                else:
                    result.append(current_item)
                    current_item = {'from': datetime, 'to': datetime, 'label': item['status']}

            if current_item:
                result.append(current_item)
            # print(result)
            for j in result:
                if j['label']== '待谈判':
                    j['customClass']="ganttGreen"
                elif j['label']== '已谈判等回复':
                    j['customClass']="ganttBlue"
                elif j['label']== '新价格已确认' :
                    j['customClass']="ganttOrange"
            # for j in result:
            #     if j['label']== '待拜访' or j['label']== '初期了解中' or j['label']== '有意向':
            #         j['customClass']="ganttGreen"
            #     elif j['label']== '申报预算'or j['label']== '审批中' or j['label']== '审批通过':
            #         j['customClass']="ganttBlue"
            #     elif j['label']== '待招标' or j['label']== '招标完成':
            #         j['customClass']="ganttRed"
            #     elif j['label']== '仪器装机启用' or j['label']== '仪器试剂均开票':
            #         j['customClass']="ganttOrange"

            eachsource['name']= i[0]['semidepartment']+"-"+i[0]['project']+"-"+i[0]['supplier']
            eachsource['desc']= "目标:"+i[-1]['completemonth']+"月,预估月毛利增量："+str('{:,.0f}'.format(float(i[-1]['monthgpgrowth'])))
            eachsource['values']=result    
            Negotiationsource.append(eachsource)

        result = {'code':200, 'data':{'Negotiationsource':Negotiationsource}}

        return JsonResponse(json.dumps(result, cls=NpEncoder,ensure_ascii=False),safe=False,charset='utf-8' )
    

#     var ganttData = [
#     {
#         id: 1, name: "hello1", series: [
#             { name: "OK", start: new Date(2023,01,01), end: new Date(2023,01,03) },
#             { name: "NOT OK", start: new Date(2023,01,02), end: new Date(2023,01,05), color: "#f0f0f0" }
#         ]
#     }, 