import psycopg2
import pandas as pd
import os
import xlrd
#pip install msoffcrypto-tool
import io            # 将文件写入到内存中
# from sqlalchemy import create_engine
import numpy as np
from datetime import date,timedelta,datetime
import re

def SHIYUAN(rawdata):
    order_df = pd.read_excel(rawdata, sheet_name = '订单') #要保证订单编号和物料编码联合只出现一次
    order_df['订单编号'] = order_df['订单编号'].astype(str)
    order_df['物料编码'] = order_df['物料编码'].astype(str)

    in_out_df = pd.read_excel(rawdata, sheet_name = '直送入库和康意路出入库明细') 
    in_out_df['订单号'] = in_out_df['订单号'].astype(str)
    in_out_df['商品编码'] = in_out_df['商品编码'].astype(str)
    in_out_df['批号'] = in_out_df['批号'].astype(str)

    consumption_df = pd.read_excel(rawdata, sheet_name = '领用明细') 
    consumption_df['编码'] = consumption_df['编码'].astype(str)
    consumption_df['批号'] = consumption_df['批号'].astype(str)
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
    result_list = [order_all_df,order_df,in_out_df,str_kyl_df,product_batch_kyl_df,product_in_consumption_df,product_batch_in_consumption_df,consumption_df]
    return result_list
