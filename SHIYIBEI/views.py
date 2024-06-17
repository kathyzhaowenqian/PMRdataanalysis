from typing import Any
from django.shortcuts import render,redirect
# Create your views here.
from django.views import View
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import numpy as np
import json
from json.encoder import JSONEncoder
from decimal import Decimal
from datetime import date,timedelta,datetime
import pandas as pd
import xlwt
import io
from SHIYIBEI.tools.CalculateAPI import *
import os
from django.http import FileResponse
today = date.today()
folder_name1 = 'file'
folder_name2 = 'syb'
file_name = 'ShiYiBei.xlsx'
Upload_File_2 = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name)



class Upload2(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' or  request.user.username=='cxy':               

            # # login_user = request.user.chinesename
            # if os.path.exists(Upload_File_2):  # 判断文件是否存在
            #     os.remove(Upload_File_2)       # 删除文件

            return render(request,'SYB/index.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile') is not None:
            uploaded_file = request.FILES.get('uploadfile')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_2
                # if os.path.exists(file_name):  # 判断文件是否存在
                #     os.remove(file_name)       # 删除文件

                SHIYIBEI(uploaded_file,file_name)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

class Download2(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp' or  request.user.username=='cxy':  
            file_path = Upload_File_2

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=ShiYiBeiCalculate.xlsx'
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')    