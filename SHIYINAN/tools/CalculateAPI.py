import psycopg2
import pandas as pd
import os
import xlrd
import io            # 将文件写入到内存中
import numpy as np
from datetime import date,timedelta,datetime
import re
from sqlalchemy import create_engine
from sqlalchemy.types import *
from django.conf import settings

def SHIYINAN(rawdata,filename):
    order_df = pd.read_excel(rawdata, sheet_name = '订单') #要保证订单编号和物料编码联合只出现一次
    order_df['订单编号'] = order_df['订单编号'].astype(str)
    order_df['物料编码'] = order_df['物料编码'].astype(str)
    order_df['数量'] = order_df['数量'].apply(lambda x: float(str(x).replace(',', '')))
    order_df=order_df[["订单日期","使用科室","订单编号","货号","物料编码","智检编码","名称","规格","品牌","单位","供应商","进价","销价","数量","备注"]]

    in_out_df = pd.read_excel(rawdata, sheet_name = '直送入库和康意路出入库明细') 
    in_out_df['订单号'] = in_out_df['订单号'].astype(str)
    in_out_df['商品编码'] = in_out_df['商品编码'].astype(str)
    in_out_df['批号'] = in_out_df['批号'].astype(str)
    in_out_df['数量'] = in_out_df['数量'].apply(lambda x: float(str(x).replace(',', '')))
    in_out_df=in_out_df[["订货抬头", "入库日期", "订单号", "科室", "商品编码", "商品名称", "规格", "单位", "品牌", "供应商", "采购单价", "税价总金额", "数量", "批号", "有效期至", "备注", "备注2"]]

    consumption_df = pd.read_excel(rawdata, sheet_name = '领用明细') 
    consumption_df['编码'] = consumption_df['编码'].astype(str)
    consumption_df['批号'] = consumption_df['批号'].astype(str)
    consumption_df['数量'] = consumption_df['数量'].apply(lambda x: float(str(x).replace(',', '')))
    consumption_df=consumption_df[["日期", "科室", "编码", "产品名称", "规格", "单位", "厂商", "批号", "有效期", "数量", "是否签回", "送货人"]]
 

    #订单统计
    order_groupby_df=order_df.groupby(['订单编号','物料编码'])['数量'].sum().reset_index()
    order_unique_df=order_df[['订单日期','使用科室','订单编号','货号','物料编码','智检编码','名称','规格','品牌','单位','供应商','进价','销价','备注']]
    order_unique_df =order_unique_df.drop_duplicates(subset=['订单编号','物料编码'], keep='first')
    order_merge_df = pd.merge(order_unique_df,order_groupby_df, on=['订单编号','物料编码'], how='left')
    order_merge_df.rename(columns={ '数量':'订单总数量'},inplace=True)
    kyl_in_out_df=in_out_df[in_out_df['备注']=='康意路入库']
    unique_kyl_in_out_df=kyl_in_out_df.groupby(['订单号','商品编码'])['数量'].sum().reset_index()
    unique_kyl_in_out_df.rename(columns={ '数量':'康意路入库总数量'},inplace=True)
    all_kyl_in_out_df= kyl_in_out_df.groupby(['订单号','商品编码']).agg({'数量': lambda x: '/'.join(map(str, x)), '入库日期': lambda x: '/'.join(map(str, x))}).reset_index()
    all_kyl_in_out_df.rename(columns={ '数量':'康意路数量明细','入库日期':'康意路入库日期明细'},inplace=True)
    kyl_df=pd.merge(unique_kyl_in_out_df,all_kyl_in_out_df,  how="left",  left_on=['订单号','商品编码'],right_on=['订单号','商品编码'])
    order_kyl_df=pd.merge(order_merge_df,kyl_df,  how="left",  left_on=['订单编号','物料编码'],right_on=['订单号','商品编码'])
    order_kyl_df.drop(labels=['订单号','商品编码'],axis=1, inplace = True)
    zs_in_out_df=in_out_df[in_out_df['备注']=='直送']
    unique_zs_in_out_df=zs_in_out_df.groupby(['订单号','商品编码'])['数量'].sum().reset_index()
    unique_zs_in_out_df.rename(columns={ '数量':'直送入库总数量'},inplace=True)
    all_zs_in_out_df= zs_in_out_df.groupby(['订单号','商品编码']).agg({'数量': lambda x: '/'.join(map(str, x)), '入库日期': lambda x: '/'.join(map(str, x))}).reset_index()
    all_zs_in_out_df.rename(columns={ '数量':'直送数量明细','入库日期':'直送日期明细'},inplace=True)
    zs_df=pd.merge(unique_zs_in_out_df,all_zs_in_out_df,  how="left",  left_on=['订单号','商品编码'],right_on=['订单号','商品编码'])
    order_all_df=pd.merge(order_kyl_df,zs_df,  how="left",  left_on=['订单编号','物料编码'],right_on=['订单号','商品编码'])
    order_all_df.drop(labels=['订单号','商品编码'],axis=1, inplace = True)
    order_all_df['康意路入库总数量']=order_all_df['康意路入库总数量'].fillna(0)
    order_all_df['直送入库总数量']=order_all_df['直送入库总数量'].fillna(0)
    order_all_df['合计入库']=order_all_df['康意路入库总数量']+order_all_df['直送入库总数量']
    order_all_df['欠货数量']=order_all_df['订单总数量']-order_all_df['合计入库']
    #康意路库存明细带批号
    product_batch_kyl_in_df=kyl_in_out_df.groupby(['商品编码','批号'])['数量'].sum().reset_index()
    product_batch_kyl_out_df=in_out_df[in_out_df['备注']=='康意路出库'].groupby(['商品编码','批号'])['数量'].sum().reset_index()
    product_batch_kyl_in_out_df=pd.merge(product_batch_kyl_in_df,product_batch_kyl_out_df,  how="left",  left_on=['商品编码','批号'],right_on=['商品编码','批号'])
    product_batch_kyl_in_out_df.rename(columns={ '数量_x':'入库数量','数量_y':'出库数量'},inplace=True)
    product_batch_kyl_in_out_df['入库数量']=product_batch_kyl_in_out_df['入库数量'].fillna(0)
    product_batch_kyl_in_out_df['出库数量']=product_batch_kyl_in_out_df['出库数量'].fillna(0)
    product_batch_kyl_in_out_df['剩余库存']=product_batch_kyl_in_out_df['入库数量']-product_batch_kyl_in_out_df['出库数量']
    cut_kyl_in_out_df=kyl_in_out_df[['商品编码','批号','商品名称']]
    product_batch_kyl_df = pd.merge(product_batch_kyl_in_out_df,cut_kyl_in_out_df.drop_duplicates(subset=['商品编码','批号'], keep='first'), on=['商品编码','批号'], how='left')
    product_batch_kyl_df=product_batch_kyl_df[['商品编码','批号','商品名称','入库数量','出库数量','剩余库存']]
    #康意路库存明细
    product_kyl_in_df=kyl_in_out_df.groupby('商品编码')['数量'].sum().reset_index()
    product_kyl_out_df=in_out_df[in_out_df['备注']=='康意路出库'].groupby('商品编码')['数量'].sum().reset_index()
    product_kyl_in_out_df=pd.merge(product_kyl_in_df,product_kyl_out_df,  how="left",  left_on=['商品编码'],right_on=['商品编码'])
    product_kyl_in_out_df.rename(columns={ '数量_x':'入库数量','数量_y':'出库数量'},inplace=True)
    product_kyl_in_out_df['入库数量']=product_kyl_in_out_df['入库数量'].fillna(0)
    product_kyl_in_out_df['出库数量']=product_kyl_in_out_df['出库数量'].fillna(0)
    product_kyl_in_out_df['剩余库存']=product_kyl_in_out_df['入库数量']-product_kyl_in_out_df['出库数量']
    product_kyl_in_out_df.rename(columns={ '入库数量':'入库总数量','出库数量':'出库总数量'},inplace=True)
    str_kyl_in_df= kyl_in_out_df.groupby(['商品编码']).agg({'数量': lambda x: '/'.join(map(str, x)), '入库日期': lambda x: '/'.join(map(str, x)),'批号': lambda x: '/'.join(map(str, x))}).reset_index()
    str_kyl_in_df.rename(columns={ '数量':'入库数量明细','入库日期':'入库日期明细','批号':'入库批号明细'},inplace=True)
    str_kyl_out_df= in_out_df[in_out_df['备注']=='康意路出库'].groupby(['商品编码']).agg({'数量': lambda x: '/'.join(map(str, x)), '入库日期': lambda x: '/'.join(map(str, x)),'批号': lambda x: '/'.join(map(str, x))}).reset_index()
    str_kyl_out_df.rename(columns={ '数量':'出库数量明细','入库日期':'出库日期明细','批号':'出库批号明细'},inplace=True)
    str_kyl_df = pd.merge(product_kyl_in_out_df,str_kyl_in_df, on='商品编码', how='left')
    str_kyl_df= pd.merge(str_kyl_df,str_kyl_out_df, on='商品编码', how='left')
    cut_kyl_in_out_df2=kyl_in_out_df[['商品编码','商品名称']]
    str_kyl_df = pd.merge(str_kyl_df,cut_kyl_in_out_df2.drop_duplicates(subset='商品编码', keep='first'), on='商品编码', how='left')
    str_kyl_df=str_kyl_df[['商品编码','商品名称','入库总数量','入库数量明细','入库日期明细','入库批号明细','出库总数量','出库数量明细','出库日期明细','出库批号明细','剩余库存']]

    #医院端的库存和领用汇总(带批次)
    total_in_df=in_out_df[in_out_df['备注']!='康意路出库']
    sumup_total_in_df=total_in_df[['商品编码','批号','商品名称','规格','单位','品牌','供应商','科室','有效期至']]
    sumup_total_in_df=sumup_total_in_df.drop_duplicates(subset=['商品编码','批号'], keep='first')
    product_batch_kyl_out_df.rename(columns={ '数量':'康意路来货总数量'},inplace=True)
    product_batch_kyl_out_detail_df= in_out_df[in_out_df['备注']=='康意路出库'].groupby(['商品编码','批号']).agg({'数量': lambda x: '/'.join(map(str, x)), '入库日期': lambda x: '/'.join(map(str, x)), '订单号': lambda x: '/'.join(map(str, x))}).reset_index()
    product_batch_kyl_out_detail_df.rename(columns={ '数量':'康意路来货数量明细','入库日期':'康意路来货日期明细','订单号':'康意路来货订单号明细'},inplace=True)
    product_batch_kyl_out_detail_df=pd.merge(product_batch_kyl_out_df,product_batch_kyl_out_detail_df,  how="left",  left_on=['商品编码','批号'],right_on=['商品编码','批号'])
    product_batch_zs_out_total_df=zs_in_out_df.groupby(['商品编码','批号'])['数量'].sum().reset_index()
    product_batch_zs_out_total_df.rename(columns={ '数量':'直送入库总数量'},inplace=True)
    product_batch_zs_out_detail_df= zs_in_out_df.groupby(['商品编码','批号']).agg({'数量': lambda x: '/'.join(map(str, x)), '入库日期': lambda x: '/'.join(map(str, x)), '订单号': lambda x: '/'.join(map(str, x))}).reset_index()
    product_batch_zs_out_detail_df.rename(columns={ '数量':'直送数量明细','入库日期':'直送日期明细','订单号':'直送订单号明细'},inplace=True)
    product_batch_zs_out_all_df=pd.merge(product_batch_zs_out_total_df,product_batch_zs_out_detail_df,  how="left",  left_on=['商品编码','批号'],right_on=['商品编码','批号'])
    product_batch_total_df=pd.merge(sumup_total_in_df,product_batch_zs_out_all_df,  how="left",  left_on=['商品编码','批号'],right_on=['商品编码','批号'])
    product_batch_total_df=pd.merge(product_batch_total_df,product_batch_kyl_out_detail_df,  how="left",  left_on=['商品编码','批号'],right_on=['商品编码','批号'])
    product_batch_total_df['康意路来货总数量']=product_batch_total_df['康意路来货总数量'].fillna(0)
    product_batch_total_df['直送入库总数量']=product_batch_total_df['直送入库总数量'].fillna(0)
    product_batch_total_df['总库存']=product_batch_total_df['直送入库总数量']+product_batch_total_df['康意路来货总数量']
    product_batch_consumption_df=consumption_df.groupby(['编码','批号'])['数量'].sum().reset_index()
    product_batch_consumption_df.rename(columns={ '数量':'领用数量','编码':'商品编码'},inplace=True)
    product_batch_consumption_df['领用数量']=product_batch_consumption_df['领用数量'].fillna(0)
    product_batch_in_consumption_df=pd.merge(product_batch_total_df,product_batch_consumption_df,  how="left",  left_on=['商品编码','批号'],right_on=['商品编码','批号'])
    product_batch_in_consumption_df['领用数量']=product_batch_in_consumption_df['领用数量'].fillna(0)
    product_batch_in_consumption_df['剩余库存']=product_batch_in_consumption_df['总库存']-product_batch_in_consumption_df['领用数量']

    #医院端的库存和领用汇总
    sumup_total_in_df2=total_in_df[['商品编码','商品名称','规格','单位','品牌','供应商','科室']]
    sumup_total_in_df2=sumup_total_in_df2.drop_duplicates(subset=['商品编码'], keep='first')
    product_kyl_out_df.rename(columns={ '数量':'康意路来货总数量'},inplace=True)
    product_kyl_out_detail_df= in_out_df[in_out_df['备注']=='康意路出库'].groupby(['商品编码']).agg({'数量': lambda x: '/'.join(map(str, x)), '入库日期': lambda x: '/'.join(map(str, x)), '订单号': lambda x: '/'.join(map(str, x)),'批号': lambda x: '/'.join(map(str, x)),'有效期至': lambda x: '/'.join(map(str, x))}).reset_index()
    product_kyl_out_detail_df.rename(columns={ '数量':'康意路来货数量明细','入库日期':'康意路来货日期明细','订单号':'康意路来货订单号明细','批号':'康意路来货批号明细','有效期至':'康意路来货效期明细'},inplace=True)
    product_kyl_out_detail_df=pd.merge(product_kyl_out_df,product_kyl_out_detail_df,  how="left",  left_on=['商品编码'],right_on=['商品编码'])
    product_zs_total_df=zs_in_out_df.groupby(['商品编码'])['数量'].sum().reset_index()
    product_zs_total_df.rename(columns={ '数量':'直送入库总数量'},inplace=True)
    product_zs_total_detail_df= zs_in_out_df.groupby(['商品编码']).agg({'数量': lambda x: '/'.join(map(str, x)), '入库日期': lambda x: '/'.join(map(str, x)), '订单号': lambda x: '/'.join(map(str, x)),'批号': lambda x: '/'.join(map(str, x)),'有效期至': lambda x: '/'.join(map(str, x))}).reset_index()
    product_zs_total_detail_df.rename(columns={ '数量':'直送数量明细','入库日期':'直送日期明细','订单号':'直送订单号明细','批号':'直送批号明细','有效期至':'直送效期明细'},inplace=True)
    product_zs_total_all_df=pd.merge(product_zs_total_df,product_zs_total_detail_df,  how="left",  left_on=['商品编码'],right_on=['商品编码'])
    product_zs_combine1_df=pd.merge(sumup_total_in_df2,product_zs_total_all_df,  how="left",  left_on=['商品编码'],right_on=['商品编码'])
    product_zs_combine1_df=pd.merge(product_zs_combine1_df,product_kyl_out_detail_df,  how="left",  left_on=['商品编码'],right_on=['商品编码'])
    product_zs_combine1_df['康意路来货总数量']=product_zs_combine1_df['康意路来货总数量'].fillna(0)
    product_zs_combine1_df['直送入库总数量']=product_zs_combine1_df['直送入库总数量'].fillna(0)
    product_zs_combine1_df['总库存']=product_zs_combine1_df['直送入库总数量']+product_zs_combine1_df['康意路来货总数量']
    product_consumption_df=consumption_df.groupby(['编码'])['数量'].sum().reset_index()
    product_consumption_df.rename(columns={ '数量':'领用数量'},inplace=True)
    product_consumption_df['领用数量']=product_consumption_df['领用数量'].fillna(0)
    product_consumption_detail_df= consumption_df.groupby(['编码']).agg({'数量': lambda x: '/'.join(map(str, x)), '批号': lambda x: '/'.join(map(str, x))}).reset_index()
    product_consumption_all_df=pd.merge(product_consumption_df,product_consumption_detail_df,  how="left",  left_on=['编码'],right_on=['编码'])
    product_consumption_all_df.rename(columns={ '编码':'商品编码','数量':'领用数量明细','批号':'领用批号明细'},inplace=True)
    product_in_consumption_df=pd.merge(product_zs_combine1_df,product_consumption_all_df,  how="left",  left_on=['商品编码'],right_on=['商品编码'])
    product_in_consumption_df['领用数量']=product_in_consumption_df['领用数量'].fillna(0)
    product_in_consumption_df['剩余库存']=product_in_consumption_df['总库存']-product_in_consumption_df['领用数量']
    #合并
    # return result_list
                    #####################商品编码	商品名称	规格	单位	品牌	供应商	科室	直送入库总数量	直送数量明细	直送日期明细	直送订单号明细	直送批号明细	直送效期明细	康意路来货总数量	康意路来货数量明细	康意路来货日期明细	康意路来货订单号明细	康意路来货批号明细	康意路来货效期明细	总库存	领用数量	领用数量明细	领用批号明细	剩余库存
    product_in_consumption_df=product_in_consumption_df[['商品编码','商品名称','规格','单位','品牌','供应商','科室','直送入库总数量','康意路来货总数量','总库存','领用数量','剩余库存']]

    # #商品编码	批号	商品名称	规格	单位	品牌	供应商	科室	有效期至	直送入库总数量	直送数量明细	直送日期明细	直送订单号明细	康意路来货总数量	康意路来货数量明细	康意路来货日期明细	康意路来货订单号明细	总库存	领用数量	剩余库存
    product_batch_in_consumption_df =  product_batch_in_consumption_df[['商品编码','批号','商品名称','规格','单位','品牌','供应商','科室','有效期至','直送入库总数量','康意路来货总数量','总库存','领用数量','剩余库存']]

    str_kyl_df=str_kyl_df[['商品编码','商品名称','入库总数量','出库总数量','剩余库存']]
    #######################   
    # 
    #         
   #保存excel
    result_list = [order_all_df,order_df,in_out_df,str_kyl_df,product_batch_kyl_df,product_in_consumption_df,product_batch_in_consumption_df,consumption_df]
    sheet_name_list = ['订单统计','订单明细(上传的)','直送入库和康意路出入库明细(上传的)','康意路库存','康意路库存(带批次)','医院端的库存和领用汇总','医院端的库存和领用汇总(带批次)','领用明细(上传的)']
    writer = pd.ExcelWriter(filename)
    for i in range(len(result_list)):
        result_list[i]=result_list[i].style.set_properties(**{'text-align': 'center'}) ## 使excel表格中的数据居中对齐
        result_list[i].to_excel(writer, sheet_name=sheet_name_list[i],index=False)
        worksheet = writer.sheets[sheet_name_list[i]]
    writer.close()
    print('excel保存成功')
    

    #保存数据存入数据库
    #订单统计
    order_all_to_sql_df=order_all_df
    order_all_to_sql_df.rename(columns={'订单日期':'orderdate','使用科室':'department','订单编号':'ordercode','货号':'itemcode','物料编码':'productcode','智检编码':'zhijiancode','名称':'productname','规格':'spec','品牌':'brand','单位':'unit','供应商':'supplier','进价':'purchaseprice','销价':'sellprice','备注':'comment','订单总数量':'ttlquantity','康意路入库总数量':'kylquantity','康意路数量明细':'kylqtydetail','康意路入库日期明细':'kyldatedetail','直送入库总数量':'directquantity','直送数量明细':'directqtydetail','直送日期明细':'directdatedetail','合计入库':'ttlinqty','欠货数量':'quantityowed'},inplace=True)
    #订单明细(上传的)
    order_to_sql_df=order_df
    order_to_sql_df.rename(columns={'订单日期':'orderdate','使用科室':'department','订单编号':'ordercode','货号':'itemcode','物料编码':'productcode','智检编码':'zhijiancode','名称':'productname','规格':'spec','品牌':'brand','单位':'unit','供应商':'supplier','进价':'purchaseprice','销价':'sellprice','数量':'quantity','备注':'comment'},inplace=True)
    #直送入库和康意路出入库明细(上传的)
    in_out_to_sql_df=in_out_df
    in_out_to_sql_df.rename(columns={'订货抬头':'ordertitle','入库日期':'indate','订单号':'ordercode','科室':'department','商品编码':'productcode','商品名称':'productname','规格':'spec','单位':'unit','品牌':'brand','供应商':'supplier','采购单价':'purchaseprice','税价总金额':'sum','数量':'quantity','批号':'batchcode','有效期至':'expiredate','备注':'comment','备注2':'comment2'},inplace=True)

    ##########################
    #康意路库存
    str_kyl_to_sql_df=str_kyl_df
    # str_kyl_to_sql_df.rename(columns={'商品编码':'productcode','商品名称':'productname','入库总数量':'inquantity','入库数量明细':'inqtydetail','入库日期明细':'indatedetail','入库批号明细':'inbatchdetail','出库总数量':'outquantity','出库数量明细':'outqtydetail','出库日期明细':'outdatedetail','出库批号明细':'outbatchdetail','剩余库存':'leftqty'},inplace=True)
    str_kyl_to_sql_df.rename(columns={'商品编码':'productcode','商品名称':'productname','入库总数量':'inquantity','出库总数量':'outquantity','剩余库存':'leftqty'},inplace=True)
   ############################


    #康意路库存(带批次)
    product_batch_kyl_to_sql_df=product_batch_kyl_df
    product_batch_kyl_to_sql_df.rename(columns={'商品编码':'productcode','批号':'batchcode','商品名称':'productname','入库数量':'inquantity','出库数量':'outquantity','剩余库存':'leftqty'},inplace=True)
    
    
    ################################
    #医院端的库存和领用汇总
    product_in_consumption_to_sql_df=product_in_consumption_df
    # product_in_consumption_to_sql_df.rename(columns={'商品编码':'productcode','商品名称':'productname','规格':'spec','单位':'unit','品牌':'brand','供应商':'supplier','科室':'department','直送入库总数量':'directinqty','直送数量明细':'directinqtydetail','直送日期明细':'directindatedetail','直送订单号明细':'directinorderdetail','直送批号明细':'directinbatchdetail','直送效期明细':'directinexpdetail','康意路来货总数量':'kylqty','康意路来货数量明细':'kylqtydetail','康意路来货日期明细':'kyldatedetail','康意路来货订单号明细':'kylorderdetail','康意路来货批号明细':'kylbatchdetail','康意路来货效期明细':'kylexpdetail','总库存':'ttlqty','领用数量':'takeoutqty','领用数量明细':'takeoutqtydetail','领用批号明细':'takeoutbatchdetail','剩余库存':'leftqty'},inplace=True)
    product_in_consumption_to_sql_df.rename(columns={'商品编码':'productcode','商品名称':'productname','规格':'spec','单位':'unit','品牌':'brand','供应商':'supplier','科室':'department','直送入库总数量':'directinqty','康意路来货总数量':'kylqty','总库存':'ttlqty','领用数量':'takeoutqty','剩余库存':'leftqty'},inplace=True)

    
    #医院端的库存和领用汇总(带批次)
    product_batch_in_consumption_to_sql_df=product_batch_in_consumption_df
    # product_batch_in_consumption_to_sql_df.rename(columns={'商品编码':'productcode','批号':'batchcode','商品名称':'productname','规格':'spec','单位':'unit','品牌':'brand','供应商':'supplier','科室':'department','有效期至':'expiredate','直送入库总数量':'directinqty','直送数量明细':'directinqtydetail','直送日期明细':'directindatedetail','直送订单号明细':'directinorderdetail','康意路来货总数量':'kylqty','康意路来货数量明细':'kylqtydetail','康意路来货日期明细':'kyldatedetail','康意路来货订单号明细':'kylorderdetail','总库存':'ttlqty','领用数量':'takeoutqty','剩余库存':'leftqty'},inplace=True)
    product_batch_in_consumption_to_sql_df.rename(columns={'商品编码':'productcode','批号':'batchcode','商品名称':'productname','规格':'spec','单位':'unit','品牌':'brand','供应商':'supplier','科室':'department','有效期至':'expiredate','直送入库总数量':'directinqty','康意路来货总数量':'kylqty','总库存':'ttlqty','领用数量':'takeoutqty','剩余库存':'leftqty'},inplace=True)
    ################################


    
    
    #领用明细(上传的)
    consumption_to_sql_df=consumption_df
    consumption_to_sql_df.rename(columns={'日期':'date','科室':'department','编码':'productcode','产品名称':'productname','规格':'spec','单位':'unit','厂商':'brand','批号':'batchcode','有效期':'expiredate','数量':'quantity','是否签回':'signback','送货人':'deliverperson'}, inplace=True)
 
    #【【【【【【【【【【【【链接数据库！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    to_sql_connect = create_engine('postgresql+psycopg2://' + settings.PG_DBUSER + ':' + settings.PG_PASSWORD + '@'+settings.PG_HOST + ':'+settings.PG_PORT+'/'+settings.PG_DBNAME)
    # to_sql_connect = create_engine('postgresql+psycopg2://' + 'postgres' + ':' + 'Kathy83305136' + '@139.224.61.6' + ':'+'5432'+'/'+'postgres')

    # print('settings.PG_DBNAME',settings.PG_DBNAME)
    to_sql_connect_conn = to_sql_connect.connect()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``

    #订单统计
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLYCHAIN"."SHIYINAN_order_calculate"')   
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLYCHAIN"."shiyinanordercalculate_id_seq" RESTART WITH 1')
    #订单明细(上传的)
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLYCHAIN"."SHIYINAN_order_detail"')   
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLYCHAIN"."shiyinanorderdetail_id_seq" RESTART WITH 1')
    #直送入库和康意路出入库明细(上传的)
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLYCHAIN"."SHIYINAN_in_out_detail"')   
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLYCHAIN"."shiyinaninoutdetail_id_seq" RESTART WITH 1')
    #康意路库存
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLYCHAIN"."SHIYINAN_kyl_stock"')   
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLYCHAIN"."shiyinankylstock_id_seq" RESTART WITH 1')
    #康意路库存(带批次)
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLYCHAIN"."SHIYINAN_kyl_stock_batch"')   
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLYCHAIN"."shiyinankylstockbatch_id_seq" RESTART WITH 1')
    #医院端的库存和领用汇总
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLYCHAIN"."SHIYINAN_hospital_in_out"')   
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLYCHAIN"."shiyinanhospitalinout_id_seq" RESTART WITH 1')
    #医院端的库存和领用汇总(带批次)
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLYCHAIN"."SHIYINAN_hospital_in_out_batch"')   
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLYCHAIN"."shiyinanhospitalinoutbatch_id_seq" RESTART WITH 1')
    #领用明细(上传的)
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLYCHAIN"."SHIYINAN_comsumption_detail"')   
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLYCHAIN"."shiyinanconsumptiondetail_id_seq" RESTART WITH 1')

    try:
        order_all_to_sql_df.to_sql("SHIYINAN_order_calculate", con=to_sql_connect, schema='SUPPLYCHAIN', if_exists='append', index=False)
        order_to_sql_df.to_sql("SHIYINAN_order_detail", con=to_sql_connect, schema='SUPPLYCHAIN', if_exists='append', index=False)
        in_out_to_sql_df.to_sql("SHIYINAN_in_out_detail", con=to_sql_connect, schema='SUPPLYCHAIN', if_exists='append', index=False)
        str_kyl_to_sql_df.to_sql("SHIYINAN_kyl_stock", con=to_sql_connect, schema='SUPPLYCHAIN', if_exists='append', index=False)
        product_batch_kyl_to_sql_df.to_sql("SHIYINAN_kyl_stock_batch", con=to_sql_connect, schema='SUPPLYCHAIN', if_exists='append', index=False)
        product_in_consumption_to_sql_df.to_sql("SHIYINAN_hospital_in_out", con=to_sql_connect, schema='SUPPLYCHAIN', if_exists='append', index=False)
        product_batch_in_consumption_to_sql_df.to_sql("SHIYINAN_hospital_in_out_batch", con=to_sql_connect, schema='SUPPLYCHAIN', if_exists='append', index=False)
        consumption_to_sql_df.to_sql("SHIYINAN_comsumption_detail", con=to_sql_connect, schema='SUPPLYCHAIN', if_exists='append', index=False)
        print('已上传')

    except Exception as e:
        print('错误：{}'.format(e))

    to_sql_connect.dispose()
    to_sql_connect_conn.close()
    print('所有表格成功上传数据库，关闭链接')
    return 'success'





if __name__=='__main__':
    rawdata = 'C:\\Users\\赵文茜\\Desktop\\testshiyinan.xlsx'  
    filename= 'C:\\Users\\赵文茜\\Desktop\\testshiyinan_result.xlsx'  
    SHIYINAN(rawdata,filename)
    print('原始数据已上传')

  