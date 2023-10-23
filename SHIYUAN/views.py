from typing import Any
from django.shortcuts import render,redirect
# Create your views here.
from django.views import View
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from PUZHONGXIN.models import *
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
class Upload(View):
    def get(self,request):
        # if os.path.exists('十院明细.xlsx'):  # 判断文件是否存在
        #     os.remove('十院明细.xlsx')       # 删除文件
        # if os.path.exists('ShiYuan.xlsx'):  # 判断文件是否存在
        #     os.remove('ShiYuan.xlsx')       # 删除文件
        return render(request,'SY/upload.html')
    
    def post(self,request):
        if  request.FILES['excelFile']:

            excel_file = request.FILES['excelFile']
            print('看一下格式excel_file',excel_file)
            # order_data = pd.read_excel(excel_file, sheet_name='订单')
            # # 处理数据调整逻辑
            # # ...
            # # 存储调整后的数据到新的Excel文件
            # new_excel_file = 'ShiYuan.xlsx'
            # order_data.to_excel(new_excel_file, index=False)
            file_name = 'ShiYuan.xlsx'
            if os.path.exists(file_name):  # 判断文件是否存在
                os.remove(file_name)       # 删除文件
            sheet_name_list = ['订单统计','订单明细(上传的)','直送入库和康意路出入库明细(上传的)','康意路库存','康意路库存(带批次)','医院端的库存和领用汇总','医院端的库存和领用汇总(带批次)','领用明细(上传的)']
            writer = pd.ExcelWriter(file_name)
            result_list=SHIYUAN(excel_file)

            for i in range(len(result_list)):
                result_list[i]=result_list[i].style.set_properties(**{'text-align': 'center'}) ## 使excel表格中的数据居中对齐
                result_list[i].to_excel(writer, sheet_name=sheet_name_list[i],index=False)
                worksheet = writer.sheets[sheet_name_list[i]]
            #     worksheet.set_column('A:B',16) ## 设置excel表格列宽为16
            writer.close()

            return HttpResponseRedirect('/SHIYUAN/downloads')
        return HttpResponse('没有正确上传')



class Download(View):
    def get(self,request):
        file_path = 'ShiYuan.xlsx'
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read())
            
            response['Content-Disposition'] = 'attachment; filename=ShiYuan.xlsx'
            response['Content-Type'] = 'application/vnd.ms-excel'
            return response