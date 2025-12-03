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
from SHIYUAN.tools.CalculateAPI import *
import os
from django.http import FileResponse

today = date.today()
# Upload_File_2 = os.path.join(os.path.dirname(__file__), './file/sy', 'ShiYuan.xlsx')
folder_name1 = 'file'
folder_name2 = 'sy'
file_name = 'ShiYuan.xlsx'
Upload_File_2 = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name)


class Upload(View):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.Upload_File = Upload_File_2

    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='zwq8zhj' or  request.user.username=='cxy':               
            # print('os.path.dirname(__file__),',os.path.dirname(__file__))
                
            if os.path.exists(self.Upload_File):  # 判断文件是否存在
                os.remove(self.Upload_File)       # 删除文件

            return render(request,'SY/upload.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')
        '''
    def post(self,request):
        if  request.FILES['excelFile']:
            
            excel_file = request.FILES['excelFile']
            print('看一下格式excel_file',excel_file)
            file_name = self.Upload_File
            # file_name = '/file/sy/ShiYuan.xlsx'
            if os.path.exists(file_name):  # 判断文件是否存在
                os.remove(file_name)       # 删除文件

            sheet_name_list = ['订单统计','订单明细(上传的)','直送入库和康意路出入库明细(上传的)','康意路库存','康意路库存(带批次)','医院端的库存和领用汇总','医院端的库存和领用汇总(带批次)','领用明细(上传的)']
            
            writer = pd.ExcelWriter(file_name)
            result_list=SHIYUAN(excel_file)

            for i in range(len(result_list)):
                result_list[i]=result_list[i].style.set_properties(**{'text-align': 'center'}) ## 使excel表格中的数据居中对齐
                result_list[i].to_excel(writer, sheet_name=sheet_name_list[i],index=False)
                worksheet = writer.sheets[sheet_name_list[i]]
            writer.close()

            return HttpResponseRedirect('/SHIYUAN/downloads')
        return HttpResponse('没有正确上传')'''

    def post(self,request):
        if  request.FILES.get('excel') is not None:
            excel_file = request.FILES.get('excel')
            
            # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',excel_file)
                file_name = self.Upload_File
                # file_name = '/file/sy/ShiYuan.xlsx'
                if os.path.exists(file_name):  # 判断文件是否存在
                    os.remove(file_name)       # 删除文件

                sheet_name_list = ['订单统计','订单明细(上传的)','直送入库和康意路出入库明细(上传的)','康意路库存','康意路库存(带批次)','医院端的库存和领用汇总','医院端的库存和领用汇总(带批次)','领用明细(上传的)']
                
                writer = pd.ExcelWriter(file_name)
                result_list=SHIYUAN(excel_file)

                for i in range(len(result_list)):
                    result_list[i]=result_list[i].style.set_properties(**{'text-align': 'center'}) ## 使excel表格中的数据居中对齐
                    result_list[i].to_excel(writer, sheet_name=sheet_name_list[i],index=False)
                    worksheet = writer.sheets[sheet_name_list[i]]
                writer.close()
                result = {'code':200, 'data':'文件上传成功'}
                return JsonResponse(result)
    
            except Exception as e:
                result = {'code':404, 'data':'文件错误！错误信息：{}'.format(str(e))}
                return JsonResponse(result)
        
        return JsonResponse({'code':404, 'data':'请上传文件'})



class Download(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='zwq8zhj' or  request.user.username=='cxy':  
            file_path = Upload_File_2

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=ShiYuanCalculate.xlsx'
                    response['Content-Type'] = 'application/vnd.ms-excel'
                    # print('response??????',response)

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')    
'''
class Download(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # self.Upload_File = os.path.join(os.path.dirname(__file__), './file/sy', 'ShiYuan.xlsx')
        

    def get(self,request):
        file_path = Upload_File_2
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read())
            
            response['Content-Disposition'] = 'attachment; filename=ShiYuanCalculate.xlsx'
            response['Content-Type'] = 'application/vnd.ms-excel'
            return response'''



class Upload2(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='zwq8zhj' or  request.user.username=='cxy':               

            # # login_user = request.user.chinesename
            # if os.path.exists(Upload_File_2):  # 判断文件是否存在
            #     os.remove(Upload_File_2)       # 删除文件

            return render(request,'SY/index.html')
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

                SHIYUAN(uploaded_file,file_name)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

class Download2(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='zwq8zhj' or  request.user.username=='cxy':  
            file_path = Upload_File_2

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=ShiYuanCalculate.xlsx'
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')    