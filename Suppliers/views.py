from django.shortcuts import render
from django.views import View
import os
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from Suppliers.tools.CalculateAPI import *
import pandas as pd
from datetime import date
import psycopg2
import pandas as pd
import os
import xlrd
#pip install msoffcrypto-tool
import io            # 将文件写入到内存中
from sqlalchemy import create_engine
import numpy as np
from datetime import date,timedelta,datetime
import re
from sqlalchemy.types import *


today = date.today()

#定好这个文件的名称
folder_name1 = 'file'
folder_name2 = 'suppliers'
file_name_xey = 'XuErYuan.xlsx'
Upload_File_xey = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_xey)



# 上传23年数据
class Uploads_XEY_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_xey):  # 判断文件是否存在
            #     os.remove(Upload_File_xey)       # 删除文件
            return render(request,'Suppliers/index_xey.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_xey

                rawdata23 = uploaded_file 
                project='徐二院'
                table23='XEY23'
                seq23='xey23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='XEY2122'
                table23='XEY23'
                table24='XEY24'
                project='徐二院'
                filename=file_name
                Supplier_Rank_table='XEY_Supplier_Rank'
                supplierrank_id_seq_table='xeysupplierrank_id_seq'
                Supplier_Product_Summary_table='XEY_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='xeysupplierproductsummary_id_seq'
                Product_Rank_table='XEY_Product_Rank'
                productrank_id_seq_table='xeyproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_XEY_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_xey

                rawdata24 = uploaded_file 
                project='徐二院'
                table24='XEY24'
                seq24='xey24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='XEY2122'
                table23='XEY23'
                table24='XEY24'
                project='徐二院'
                filename=file_name
                Supplier_Rank_table='XEY_Supplier_Rank'
                supplierrank_id_seq_table='xeysupplierrank_id_seq'
                Supplier_Product_Summary_table='XEY_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='xeysupplierproductsummary_id_seq'
                Product_Rank_table='XEY_Product_Rank'
                productrank_id_seq_table='xeyproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)


                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})




# 下载
class Downloads_XEY(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_xey

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=XuErYuan_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')    
        
        