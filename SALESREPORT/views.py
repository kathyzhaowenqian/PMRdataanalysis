from typing import Any
from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import numpy as np
import json
from json.encoder import JSONEncoder
from decimal import Decimal
import pandas as pd
import xlwt
import io
 
import os
from django.http import FileResponse
from .models import *

from datetime import date,timedelta,datetime
from django.utils import timezone
import pytz

china_tz = pytz.timezone('Asia/Shanghai')

# 假设用户字典如下, 这应该是你定义的对应关系
user_company_dict = {
    1:1,25:7,

    # 其他用户数据...
}


def transfer_date(frontend_date):
    date = datetime.strptime(frontend_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    date = date.replace(tzinfo=pytz.UTC)
    date = date.astimezone(china_tz)
    return date

class Submit(View):
    def get(self,request):
        JcReport_view_group_list=['JCReport']
        user_in_group_list = request.user.groups.values('name')

        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in JcReport_view_group_list:
                today = date.today()            
                context={
                    'today':today
                }
                return render(request,'report/report.html',context=context)
        if request.user.username=='admin' or request.user.username=='zwq8zhj':               

            # login_user = request.user.id
            # companyid=user_company_dict[login_user]
            # print(login_user,type(login_user),companyid,type(companyid))
            today = date.today()            
            context={
                'today':today
            }
            return render(request,'report/report.html',context=context)
        else:
            return HttpResponse('您好，目前您暂无权限访问')
        
    def post(self, request):
        login_user = request.user.id
        if login_user:
            companyid=user_company_dict[login_user]
            # print(login_user,type(login_user),companyid,type(companyid))
            data = json.loads(request.body)
            # print(data['date2'],data['date3'],type(data['date2']))


            #  # 将字符串解析为 UTC 时间的 datetime 对象
            # date2 = datetime.strptime(data['date2'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # # 将其设置为 UTC 时区
            # date2 = date2.replace(tzinfo=pytz.UTC)
            # date2 = date2.astimezone(china_tz)

        

            SalesReport.objects.create(
                salesman_id=login_user,
                company_id=companyid,
                date1=transfer_date(data['date1']),
                project=data['project'],
                name=data['name'],
                desc=data['desc'],
                type=data['type'],
                state=data['state'],
                stage=data['stage'],
                date2=transfer_date(data['date2']) if data['date2'] else None,
                date3=transfer_date(data['date3']) if data['date3'] else None,
                operator_id=login_user
            )
             
            return JsonResponse({'status': 'success'}, status=201)
    