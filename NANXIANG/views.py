from django.shortcuts import render
# Create your views here.
from django.views import View
from django.http import JsonResponse,HttpResponse
from NANXIANG.models import *
import numpy as np
import json
from json.encoder import JSONEncoder
from decimal import Decimal
from django.http import JsonResponse
from datetime import date,timedelta,datetime
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
class NXgantt(View):

    def get(self, request):
        # login_user = request.user.chinesename
        # view_group_list = ['boss','pmronlyview','pmrmanager','pmrdirectsales','allviewonly']
        # user_in_group_list = request.user.groups.values('name')

        
        # for user_in_group_dict in user_in_group_list:
        #     if user_in_group_dict['name'] in view_group_list :
        #         return render(request, 'PMRanalysis/index.html')
            
        # if request.user.username=='admin':
            return render(request, 'NANXIANG/gantt2.html')
        # else:
        #     return HttpResponse('您好，目前您暂无权限访问')
        
    def post(self,request):
        
        username = request.user.username
        NewProjectStatus_queryset = NXNewProjectStatus.objects.values('statushistory').filter(is_active=True)
        NegotiationStatus_queryset = NXNegotiationStatus.objects.values('statushistory').filter(is_active=True)
        ChangeChannelStatus_queryset = NXChangeChannelStatus.objects.values('statushistory').filter(is_active=True)
        ChangeBrandStatus_queryset = NXChangeBrandStatus.objects.values('statushistory').filter(is_active=True)
        SetStatus_queryset = NXSetStatus.objects.values('statushistory').filter(is_active=True)
        NewProjectdatas = [item['statushistory'] for item in NewProjectStatus_queryset]
        Negotiationdatas = [item['statushistory'] for item in NegotiationStatus_queryset]
        ChangeChanneldatas = [item['statushistory'] for item in ChangeChannelStatus_queryset]
        ChangeBranddatas = [item['statushistory'] for item in ChangeBrandStatus_queryset]
        Setdatas = [item['statushistory'] for item in SetStatus_queryset]
        datas=NewProjectdatas+Negotiationdatas+ChangeChanneldatas+ChangeBranddatas+Setdatas

        #根据采购金额和供应商采购金额排序
        datas = sorted(datas, key=lambda x: (float(x[0]['purchasesum']), float(x[0]['supplierpurchasesum'])), reverse=True)
        datasource=[]
        for i in datas: #循环每一行的statushistory，每一行statushistory结构是 [{,,,},{,,,}]
            eachsource={}
            result = []
            current_item = {}
            #结构 { ，，[{},{}]} ，然后最外面套Negotiationsource  就是 [{ ，，[{},{}]},{ ，，[{},{}]}]
            for item in i: #循环[{,,,},{,,,}]中的每个{}
                datetime=item['time'].split()[0]
                if not current_item: #等于给每一个{}配一个current_item
                    current_item = {'from': datetime, 'to': datetime, 'label': item['status']}
                elif item['status'] == current_item['label']: #如果出现了同样的label（就是状态，待拜访之类的）
                    current_item['to'] = datetime #就把时间更新到最新
                else:
                    result.append(current_item) #如果有current_item就append
                    current_item = {'from': datetime, 'to': datetime, 'label': item['status']}

            if current_item:
                result.append(current_item)

            #如果不是最后一个状态，则日期一直往今天延续
            latest_item = max(result, key=lambda x: x['to'])
            if latest_item['label']!='仪器试剂均开票' and latest_item['label']!='新价格已确认' and   latest_item['label']!='新渠道价格已确认' :
                latest_item['to']=str(date.today())

            # print(result)
            for j in result:  #result就是values,循环value[]中的每一个{}
                if j['label']== '待谈判' or  j['label']== '待拜访' or j['label']== '初期了解中' or j['label']== '有意向':
                    j['customClass']="ganttGreen"
                elif j['label']== '已谈判等回复' or j['label']== '申报预算'or j['label']== '审批中' or j['label']== '审批通过':
                    j['customClass']="ganttBlue"
                elif j['label']== '待招标' or j['label']== '招标完成' or j['label']== '仪器装机启用' :
                     j['customClass']="ganttRed"
                elif j['label']== '新价格已确认' or j['label']== '新渠道价格已确认' or j['label']== '仪器试剂均开票' :
                    j['customClass']="ganttOrange"
     
            eachsource['name']= i[0]['semidepartment']+"-"+i[0]['project']+"-"+i[0]['supplier']
            eachsource['desc']= "【"+i[-1]['whygrowth']+"】"+"目标:"+i[-1]['completemonth']+"月,预估月毛利↑："+str('{:,.0f}'.format(float(i[-1]['monthgpgrowth'])))
            eachsource['values']=result    
            datasource.append(eachsource)
           
        result = {'code':200, 'data':{'datasource':datasource}}

        return JsonResponse(json.dumps(result, cls=NpEncoder,ensure_ascii=False),safe=False,charset='utf-8' )
    

    #   //     {
    #         //         name: "more",
    #         //         desc: "",
    #         //         values: [
    #         //         {
    #         //             from: "2021-03-05",
    #         //             to: "2021-03-05",
    #         //             label: "1",
    #         //             customClass: "ganttBlue"
    #         //         },
    #         //         {
    #         //             from: "2021-03-05",
    #         //             to: "2021-03-07",
    #         //             label: "2",
    #         //             customClass: "ganttPurple"
    #         //         },
    #         //         {
    #         //             from: "2021-03-07",
    #         //             to: "2021-03-07",
    #         //             label: "3",
    #         //             customClass: "ganttYellow"
    #         //         },

    #         //         ]