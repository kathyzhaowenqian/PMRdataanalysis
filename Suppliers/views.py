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
from .models import *

today = date.today()

#定好这个文件的名称
folder_name1 = 'file'
folder_name2 = 'suppliers'
file_name_xey = 'XuErYuan.xlsx'
Upload_File_xey = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_xey)

file_name_nq = 'NanQiao.xlsx'
Upload_File_nq = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_nq)

file_name_pzx = 'PuZhongXin.xlsx'
Upload_File_pzx = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_pzx)

file_name_xinyi = 'XinYi.xlsx'
Upload_File_xinyi = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_xinyi)

file_name_pizhou = 'PiZhou.xlsx'
Upload_File_pizhou = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_pizhou)

file_name_anting = 'AnTing.xlsx'
Upload_File_anting = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_anting)

file_name_qixian = 'QiXian.xlsx'
Upload_File_qixian = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_qixian)

file_name_shenyang = 'ShenYang.xlsx'
Upload_File_shenyang = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_shenyang)

file_name_situan = 'SiTuan.xlsx'
Upload_File_situan = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_situan)

file_name_tinglin = 'Tinglin.xlsx'
Upload_File_tinglin = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_tinglin)

file_name_xidu = 'XiDu.xlsx'
Upload_File_xidu = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_xidu)

file_name_zhixiao = 'ZhiXiao.xlsx'
Upload_File_zhixiao = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_zhixiao)


file_name_nanxiang = 'NanXiang.xlsx'
Upload_File_nanxiang = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_nanxiang)


file_name_siwuwu = 'SiWuWu.xlsx'
Upload_File_siwuwu = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_siwuwu)

file_name_total = 'TOTALprojects.xlsx'
Upload_File_total = os.path.join(os.path.dirname(__file__), folder_name1, folder_name2,file_name_total)




#==============================================================
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
        
        
#==============================================================
# 上传23年数据
class Uploads_NQ_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_NQ):  # 判断文件是否存在
            #     os.remove(Upload_File_NQ)       # 删除文件
            return render(request,'Suppliers/index_nq.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_nq

                rawdata23 = uploaded_file 
                project='南桥'
                table23='NQ23'
                seq23='nq23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='NQ2122'
                table23='NQ23'
                table24='NQ24'
                project='南桥'
                filename=file_name
                Supplier_Rank_table='NQ_Supplier_Rank'
                supplierrank_id_seq_table='nqsupplierrank_id_seq'
                Supplier_Product_Summary_table='NQ_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='nqsupplierproductsummary_id_seq'
                Product_Rank_table='NQ_Product_Rank'
                productrank_id_seq_table='nqproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    
# 上传24年数据
class Uploads_NQ_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_nq

                rawdata24 = uploaded_file 
                project='南桥'
                table24='NQ24'
                seq24='nq24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='NQ2122'
                table23='NQ23'
                table24='NQ24'
                project='南桥'
                filename=file_name
                Supplier_Rank_table='NQ_Supplier_Rank'
                supplierrank_id_seq_table='nqsupplierrank_id_seq'
                Supplier_Product_Summary_table='NQ_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='nqsupplierproductsummary_id_seq'
                Product_Rank_table='NQ_Product_Rank'
                productrank_id_seq_table='nqproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)


                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_NQ(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_nq

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=NanQiao_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')    
        
        

#==============================================================
# 上传23年数据
class Uploads_PZX_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_PZX):  # 判断文件是否存在
            #     os.remove(Upload_File_PZX)       # 删除文件
            return render(request,'Suppliers/index_pzx.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_pzx

                rawdata23 = uploaded_file 
                project='普中心'
                table23='PZX23'
                seq23='pzx23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='PZX2122'
                table23='PZX23'
                table24='PZX24'
                project='普中心'
                filename=file_name
                Supplier_Rank_table='PZX_Supplier_Rank'
                supplierrank_id_seq_table='pzxsupplierrank_id_seq'
                Supplier_Product_Summary_table='PZX_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='pzxsupplierproductsummary_id_seq'
                Product_Rank_table='PZX_Product_Rank'
                productrank_id_seq_table='pzxproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    
# 上传24年数据
class Uploads_PZX_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_pzx

                rawdata24 = uploaded_file 
                project='普中心'
                table24='PZX24'
                seq24='pzx24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='PZX2122'
                table23='PZX23'
                table24='PZX24'
                project='普中心'
                filename=file_name
                Supplier_Rank_table='PZX_Supplier_Rank'
                supplierrank_id_seq_table='pzxsupplierrank_id_seq'
                Supplier_Product_Summary_table='PZX_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='pzxsupplierproductsummary_id_seq'
                Product_Rank_table='PZX_Product_Rank'
                productrank_id_seq_table='pzxproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)


                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})

# 下载
class Downloads_PZX(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_pzx

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=PuZhongXin_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')    



#==============================================================
# 上传23年数据
class Uploads_XINYI_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_XINYI):  # 判断文件是否存在
            #     os.remove(Upload_File_XINYI)       # 删除文件
            return render(request,'Suppliers/index_xinyi.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_xinyi

                rawdata23 = uploaded_file 
                project='新沂'
                table23='XINYI23'
                seq23='xinyi23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='XINYI2122'
                table23='XINYI23'
                table24='XINYI24'
                project='新沂'
                filename=file_name
                Supplier_Rank_table='XINYI_Supplier_Rank'
                supplierrank_id_seq_table='xinyisupplierrank_id_seq'
                Supplier_Product_Summary_table='XINYI_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='xinyisupplierproductsummary_id_seq'
                Product_Rank_table='XINYI_Product_Rank'
                productrank_id_seq_table='xinyiproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_XINYI_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_xinyi

                rawdata24 = uploaded_file 
                project='新沂'
                table24='XINYI24'
                seq24='xinyi24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='XINYI2122'
                table23='XINYI23'
                table24='XINYI24'
                project='新沂'
                filename=file_name
                Supplier_Rank_table='XINYI_Supplier_Rank'
                supplierrank_id_seq_table='xinyisupplierrank_id_seq'
                Supplier_Product_Summary_table='XINYI_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='xinyisupplierproductsummary_id_seq'
                Product_Rank_table='XINYI_Product_Rank'
                productrank_id_seq_table='xinyiproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_XINYI(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_xinyi

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=XinYi_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')    



#==============================================================
# 上传23年数据
class Uploads_PIZHOU_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_PIZHOU):  # 判断文件是否存在
            #     os.remove(Upload_File_PIZHOU)       # 删除文件
            return render(request,'Suppliers/index_pizhou.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_pizhou

                rawdata23 = uploaded_file 
                project='邳州'
                table23='PIZHOU23'
                seq23='pizhou23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='PIZHOU2122'
                table23='PIZHOU23'
                table24='PIZHOU24'
                project='邳州'
                filename=file_name
                Supplier_Rank_table='PIZHOU_Supplier_Rank'
                supplierrank_id_seq_table='pizhousupplierrank_id_seq'
                Supplier_Product_Summary_table='PIZHOU_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='pizhousupplierproductsummary_id_seq'
                Product_Rank_table='PIZHOU_Product_Rank'
                productrank_id_seq_table='pizhouproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_PIZHOU_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_pizhou

                rawdata24 = uploaded_file 
                project='邳州'
                table24='PIZHOU24'
                seq24='pizhou_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='PIZHOU2122'
                table23='PIZHOU23'
                table24='PIZHOU24'
                project='邳州'
                filename=file_name
                Supplier_Rank_table='PIZHOU_Supplier_Rank'
                supplierrank_id_seq_table='pizhousupplierrank_id_seq'
                Supplier_Product_Summary_table='PIZHOU_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='pizhousupplierproductsummary_id_seq'
                Product_Rank_table='PIZHOU_Product_Rank'
                productrank_id_seq_table='pizhouproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_PIZHOU(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_pizhou

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=PiZhou_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  
        

#==============================================================
# 上传23年数据
class Uploads_ANTING_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_ANTING):  # 判断文件是否存在
            #     os.remove(Upload_File_ANTING)       # 删除文件
            return render(request,'Suppliers/index_anting.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_anting

                rawdata23 = uploaded_file 
                project='安亭'
                table23='ANTING23'
                seq23='anting23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='ANTING2122'
                table23='ANTING23'
                table24='ANTING24'
                project='安亭'
                filename=file_name
                Supplier_Rank_table='ANTING_Supplier_Rank'
                supplierrank_id_seq_table='antingsupplierrank_id_seq'
                Supplier_Product_Summary_table='ANTING_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='antingsupplierproductsummary_id_seq'
                Product_Rank_table='ANTING_Product_Rank'
                productrank_id_seq_table='antingproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_ANTING_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_anting

                rawdata24 = uploaded_file 
                project='安亭'
                table24='ANTING24'
                seq24='anting24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='ANTING2122'
                table23='ANTING23'
                table24='ANTING24'
                project='安亭'
                filename=file_name
                Supplier_Rank_table='ANTING_Supplier_Rank'
                supplierrank_id_seq_table='antingsupplierrank_id_seq'
                Supplier_Product_Summary_table='ANTING_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='antingsupplierproductsummary_id_seq'
                Product_Rank_table='ANTING_Product_Rank'
                productrank_id_seq_table='antingproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_ANTING(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_anting

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=AnTing_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  


#==============================================================
# 上传23年数据
class Uploads_NANXIANG_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_NANXIANG):  # 判断文件是否存在
            #     os.remove(Upload_File_NANXIANG)       # 删除文件
            return render(request,'Suppliers/index_nanxiang.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_nanxiang

                rawdata23 = uploaded_file 
                project='南翔'
                table23='NANXIANG23'
                seq23='nanxiang23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='NANXIANG2122'
                table23='NANXIANG23'
                table24='NANXIANG24'
                project='南翔'
                filename=file_name
                Supplier_Rank_table='NANXIANG_Supplier_Rank'
                supplierrank_id_seq_table='nanxiangsupplierrank_id_seq'
                Supplier_Product_Summary_table='NANXIANG_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='nanxiangsupplierproductsummary_id_seq'
                Product_Rank_table='NANXIANG_Product_Rank'
                productrank_id_seq_table='nanxiangproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_NANXIANG_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_nanxiang

                rawdata24 = uploaded_file 
                project='南翔'
                table24='NANXIANG24'
                seq24='nanxiang24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='NANXIANG2122'
                table23='NANXIANG23'
                table24='NANXIANG24'
                project='南翔'
                filename=file_name
                Supplier_Rank_table='NANXIANG_Supplier_Rank'
                supplierrank_id_seq_table='nanxiangsupplierrank_id_seq'
                Supplier_Product_Summary_table='NANXIANG_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='nanxiangsupplierproductsummary_id_seq'
                Product_Rank_table='NANXIANG_Product_Rank'
                productrank_id_seq_table='nanxiangproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_NANXIANG(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_nanxiang

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=NanXiang_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  

#==============================================================
# 上传23年数据
class Uploads_QIXIAN_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_QIXIAN):  # 判断文件是否存在
            #     os.remove(Upload_File_QIXIAN)       # 删除文件
            return render(request,'Suppliers/index_qixian.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_qixian

                rawdata23 = uploaded_file 
                project='齐贤'
                table23='QIXIAN23'
                seq23='qixian23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='QIXIAN2122'
                table23='QIXIAN23'
                table24='QIXIAN24'
                project='齐贤'
                filename=file_name
                Supplier_Rank_table='QIXIAN_Supplier_Rank'
                supplierrank_id_seq_table='qixiansupplierrank_id_seq'
                Supplier_Product_Summary_table='QIXIAN_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='qixiansupplierproductsummary_id_seq'
                Product_Rank_table='QIXIAN_Product_Rank'
                productrank_id_seq_table='qixianproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_QIXIAN_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_qixian

                rawdata24 = uploaded_file 
                project='齐贤'
                table24='QIXIAN24'
                seq24='qixian24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='QIXIAN2122'
                table23='QIXIAN23'
                table24='QIXIAN24'
                project='齐贤'
                filename=file_name
                Supplier_Rank_table='QIXIAN_Supplier_Rank'
                supplierrank_id_seq_table='qixiansupplierrank_id_seq'
                Supplier_Product_Summary_table='QIXIAN_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='qixiansupplierproductsummary_id_seq'
                Product_Rank_table='QIXIAN_Product_Rank'
                productrank_id_seq_table='qixianproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_QIXIAN(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_qixian

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=QiXian_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  
        
#==============================================================
# 上传23年数据
class Uploads_SHENYANG_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_SHENYANG):  # 判断文件是否存在
            #     os.remove(Upload_File_SHENYANG)       # 删除文件
            return render(request,'Suppliers/index_shenyang.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_shenyang

                rawdata23 = uploaded_file 
                project='申养'
                table23='SHENYANG23'
                seq23='shenyang23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='SHENYANG2122'
                table23='SHENYANG23'
                table24='SHENYANG24'
                project='申养'
                filename=file_name
                Supplier_Rank_table='SHENYANG_Supplier_Rank'
                supplierrank_id_seq_table='shenyangsupplierrank_id_seq'
                Supplier_Product_Summary_table='SHENYANG_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='shenyangsupplierproductsummary_id_seq'
                Product_Rank_table='SHENYANG_Product_Rank'
                productrank_id_seq_table='shenyangproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_SHENYANG_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_shenyang

                rawdata24 = uploaded_file 
                project='申养'
                table24='SHENYANG24'
                seq24='shenyang24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='SHENYANG2122'
                table23='SHENYANG23'
                table24='SHENYANG24'
                project='申养'
                filename=file_name
                Supplier_Rank_table='SHENYANG_Supplier_Rank'
                supplierrank_id_seq_table='shenyangsupplierrank_id_seq'
                Supplier_Product_Summary_table='SHENYANG_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='shenyangsupplierproductsummary_id_seq'
                Product_Rank_table='SHENYANG_Product_Rank'
                productrank_id_seq_table='shenyangproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_SHENYANG(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_shenyang

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=ShenYang_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'
                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  
        

#==============================================================
# 上传23年数据
class Uploads_SITUAN_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_SITUAN):  # 判断文件是否存在
            #     os.remove(Upload_File_SITUAN)       # 删除文件
            return render(request,'Suppliers/index_situan.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_situan

                rawdata23 = uploaded_file 
                project='四团'
                table23='SITUAN23'
                seq23='situan23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='SITUAN2122'
                table23='SITUAN23'
                table24='SITUAN24'
                project='四团'
                filename=file_name
                Supplier_Rank_table='SITUAN_Supplier_Rank'
                supplierrank_id_seq_table='situansupplierrank_id_seq'
                Supplier_Product_Summary_table='SITUAN_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='situansupplierproductsummary_id_seq'
                Product_Rank_table='SITUAN_Product_Rank'
                productrank_id_seq_table='situanproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_SITUAN_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_situan

                rawdata24 = uploaded_file 
                project='四团'
                table24='SITUAN24'
                seq24='situan24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='SITUAN2122'
                table23='SITUAN23'
                table24='SITUAN24'
                project='四团'
                filename=file_name
                Supplier_Rank_table='SITUAN_Supplier_Rank'
                supplierrank_id_seq_table='situansupplierrank_id_seq'
                Supplier_Product_Summary_table='SITUAN_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='situansupplierproductsummary_id_seq'
                Product_Rank_table='SITUAN_Product_Rank'
                productrank_id_seq_table='situanproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_SITUAN(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_situan

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=SiTuan_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  
        


#==============================================================
# 上传23年数据
class Uploads_SIWUWU_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_SIWUWU):  # 判断文件是否存在
            #     os.remove(Upload_File_SIWUWU)       # 删除文件
            return render(request,'Suppliers/index_siwuwu.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_siwuwu

                rawdata23 = uploaded_file 
                project='四五五'
                table23='SIWUWU23'
                seq23='siwuwu23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='SIWUWU2122'
                table23='SIWUWU23'
                table24='SIWUWU24'
                project='四五五'
                filename=file_name
                Supplier_Rank_table='SIWUWU_Supplier_Rank'
                supplierrank_id_seq_table='siwuwusupplierrank_id_seq'
                Supplier_Product_Summary_table='SIWUWU_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='siwuwusupplierproductsummary_id_seq'
                Product_Rank_table='SIWUWU_Product_Rank'
                productrank_id_seq_table='siwuwuproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_SIWUWU_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_siwuwu

                rawdata24 = uploaded_file 
                project='四五五'
                table24='SIWUWU24'
                seq24='siwuwu24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='SIWUWU2122'
                table23='SIWUWU23'
                table24='SIWUWU24'
                project='四五五'
                filename=file_name
                Supplier_Rank_table='SIWUWU_Supplier_Rank'
                supplierrank_id_seq_table='siwuwusupplierrank_id_seq'
                Supplier_Product_Summary_table='SIWUWU_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='siwuwusupplierproductsummary_id_seq'
                Product_Rank_table='SIWUWU_Product_Rank'
                productrank_id_seq_table='siwuwuproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_SIWUWU(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_siwuwu

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=SiWuWu_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  
        

#==============================================================
# 上传23年数据
class Uploads_TINGLIN_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_TINGLIN):  # 判断文件是否存在
            #     os.remove(Upload_File_TINGLIN)       # 删除文件
            return render(request,'Suppliers/index_tinglin.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_tinglin

                rawdata23 = uploaded_file 
                project='亭林'
                table23='TINGLIN23'
                seq23='tinglin23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='TINGLIN2122'
                table23='TINGLIN23'
                table24='TINGLIN24'
                project='亭林'
                filename=file_name
                Supplier_Rank_table='TINGLIN_Supplier_Rank'
                supplierrank_id_seq_table='tinglinsupplierrank_id_seq'
                Supplier_Product_Summary_table='TINGLIN_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='tinglinsupplierproductsummary_id_seq'
                Product_Rank_table='TINGLIN_Product_Rank'
                productrank_id_seq_table='tinglinproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_TINGLIN_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_tinglin

                rawdata24 = uploaded_file 
                project='亭林'
                table24='TINGLIN24'
                seq24='tinglin24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='TINGLIN2122'
                table23='TINGLIN23'
                table24='TINGLIN24'
                project='亭林'
                filename=file_name
                Supplier_Rank_table='TINGLIN_Supplier_Rank'
                supplierrank_id_seq_table='tinglinsupplierrank_id_seq'
                Supplier_Product_Summary_table='TINGLIN_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='tinglinsupplierproductsummary_id_seq'
                Product_Rank_table='TINGLIN_Product_Rank'
                productrank_id_seq_table='tinglinproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_TINGLIN(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_tinglin

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=TingLin_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  
        

#==============================================================
# 上传23年数据
class Uploads_XIDU_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_XIDU):  # 判断文件是否存在
            #     os.remove(Upload_File_XIDU)       # 删除文件
            return render(request,'Suppliers/index_xidu.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_xidu

                rawdata23 = uploaded_file 
                project='西渡'
                table23='XIDU23'
                seq23='xidu23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='XIDU2122'
                table23='XIDU23'
                table24='XIDU24'
                project='西渡'
                filename=file_name
                Supplier_Rank_table='XIDU_Supplier_Rank'
                supplierrank_id_seq_table='xidusupplierrank_id_seq'
                Supplier_Product_Summary_table='XIDU_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='xidusupplierproductsummary_id_seq'
                Product_Rank_table='XIDU_Product_Rank'
                productrank_id_seq_table='xiduproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_XIDU_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_xidu

                rawdata24 = uploaded_file 
                project='西渡'
                table24='XIDU24'
                seq24='xidu24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='XIDU2122'
                table23='XIDU23'
                table24='XIDU24'
                project='西渡'
                filename=file_name
                Supplier_Rank_table='XIDU_Supplier_Rank'
                supplierrank_id_seq_table='xidusupplierrank_id_seq'
                Supplier_Product_Summary_table='XIDU_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='xidusupplierproductsummary_id_seq'
                Product_Rank_table='XIDU_Product_Rank'
                productrank_id_seq_table='xiduproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_XIDU(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_xidu

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=XiDu_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  
        

#==============================================================
# 上传23年数据
class Uploads_ZHIXIAO_23(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_ZHIXIAO):  # 判断文件是否存在
            #     os.remove(Upload_File_ZHIXIAO)       # 删除文件
            return render(request,'Suppliers/index_zhixiao.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')


    def post(self,request):
        if  request.FILES.get('uploadfile23') is not None:
            uploaded_file = request.FILES.get('uploadfile23')

        #     # 使用 Pandas 读取 Excel 文件
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_zhixiao

                rawdata23 = uploaded_file 
                project='直销'
                table23='ZHIXIAO23'
                seq23='zhixiao23_id_seq'
                RawSaveToSql(rawdata23,project,table23,seq23)
                print('原始数据已上传')

                table2122='ZHIXIAO2122'
                table23='ZHIXIAO23'
                table24='ZHIXIAO24'
                project='直销'
                filename=file_name
                Supplier_Rank_table='ZHIXIAO_Supplier_Rank'
                supplierrank_id_seq_table='zhixiaosupplierrank_id_seq'
                Supplier_Product_Summary_table='ZHIXIAO_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='zhixiaosupplierproductsummary_id_seq'
                Product_Rank_table='ZHIXIAO_Product_Rank'
                productrank_id_seq_table='zhixiaoproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
        
        return JsonResponse({'success': False, 'msg': '请上传文件'})
    

# 上传24年数据
class Uploads_ZHIXIAO_24(View):
    def post(self,request):
        if  request.FILES.get('uploadfile24') is not None:
            uploaded_file = request.FILES.get('uploadfile24')
            try:
                print('看一下格式excel_file',uploaded_file)
                file_name = Upload_File_zhixiao

                rawdata24 = uploaded_file 
                project='直销'
                table24='ZHIXIAO24'
                seq24='zhixiao24_id_seq'
                RawSaveToSql(rawdata24,project,table24,seq24)
                print('原始数据已上传')

                
                table2122='ZHIXIAO2122'
                table23='ZHIXIAO23'
                table24='ZHIXIAO24'
                project='直销'
                filename=file_name
                Supplier_Rank_table='ZHIXIAO_Supplier_Rank'
                supplierrank_id_seq_table='zhixiaosupplierrank_id_seq'
                Supplier_Product_Summary_table='ZHIXIAO_Supplier_Product_Summary'
                supplierproductsummary_id_seq_table='zhixiaosupplierproductsummary_id_seq'
                Product_Rank_table='ZHIXIAO_Product_Rank'
                productrank_id_seq_table='zhixiaoproductrank_id_seq'
                TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)

                return JsonResponse({'success': True, 'msg': '文件上传成功'})

            except Exception as e:
                return JsonResponse({'success': False, 'msg': '文件错误！错误信息：{}'.format(str(e))})
       
        return JsonResponse({'success': False, 'msg': '请上传文件'})


# 下载
class Downloads_ZHIXIAO(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
            file_path = Upload_File_zhixiao

            if not os.path.exists(file_path):
                return JsonResponse({'code':404,'data': '请先上传文件'})
               
            try:
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=ZhiXiao_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  
        

########################################
# 上传23年数据
class Uploads_TOTAL(View):
    def get(self,request):
        if request.user.username=='admin' or  request.user.username=='syp' :#or  request.user.username=='cxy':               
            # if os.path.exists(Upload_File_ZHIXIAO):  # 判断文件是否存在
            #     os.remove(Upload_File_ZHIXIAO)       # 删除文件
            return render(request,'Suppliers/index_total.html')
        else:
            return HttpResponse('您好，目前您暂无权限访问')

# 下载
class Downloads_TOTAL(View):
    def get(self,request):
        # login_user = request.user.chinesename
        if request.user.username=='admin' or  request.user.username=='syp':# or  request.user.username=='cxy':  
       
            supplierrankcombine_df=Total_Supplier_Rank.objects.all()
            productrankcombine_df=Total_Product_Rank.objects.all()
            supplierrankcombine_df = pd.DataFrame(list(supplierrankcombine_df.values()))
            productrankcombine_df = pd.DataFrame(list(productrankcombine_df.values()))
            supplierrankcombine_df.rename(columns={ 'rank': '排序', 'supplier': '供应商', 'qty21': '21年采购数量', 'qty22': '22年采购数量', 'qty23': '23年采购数量', 'qty24': '24年采购数量', 'totalqty': '采购总数量', 'sum21': '21年采购金额', 'sum22': '22年采购金额', 'sum23': '23年采购金额', 'sum24': '24年采购金额', 'totalsum': '采购总金额' },inplace=True)
            productrankcombine_df.rename(columns={},inplace=True)

                #保存
            result_list = [supplierrankcombine_df,productrankcombine_df]
            sheet_name_list = ['所有项目供应商排行','所有项目存货信息汇总']
            writer = pd.ExcelWriter(Upload_File_total)
            for i in range(len(result_list)):
                result_list[i]=result_list[i].style.set_properties(**{'text-align': 'center'}) ## 使excel表格中的数据居中对齐
                result_list[i].to_excel(writer, sheet_name=sheet_name_list[i],index=False)
                worksheet = writer.sheets[sheet_name_list[i]]
            writer.close()
            print('excel保存成功')
            
            try:
                with open(Upload_File_total, 'rb') as f:
                    response = HttpResponse(f.read())
                    response['Content-Disposition'] = 'attachment; filename=ALL_PROJECTS_{}.xlsx'.format(today)
                    response['Content-Type'] = 'application/vnd.ms-excel'

                    return response              
                    
            except Exception as e:
                return JsonResponse({'code':404,'data': '下载失败：' + str(e)})
        else:
            return HttpResponse('您好，目前您暂无权限访问')  