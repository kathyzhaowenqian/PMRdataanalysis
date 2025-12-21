import psycopg
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
from django.conf import settings




def RawSaveToSql(rawdata,project,table,seq):
    detail_df = pd.read_excel(rawdata, sheet_name = project, dtype={'发票号':str,'存货编码': str,'税率': str,'规格型号': str,'订单号': str,'入库单号': str}) 
    detail_df=detail_df[['序号','发票类型','发票号','发票日期','供应商','存货编码','存货名称','规格型号','主计量','税率','数量','原币无税单价','原币单价','原币金额','原币税额','原币价税合计','订单号','入库单号','项目名称','品牌','走账方式']]
    detail_df['发票日期'] = pd.to_datetime(detail_df['发票日期'])
    detail_df['数量'] = detail_df['数量'].apply(lambda x: float(str(x).replace(',', '')))
    detail_df['原币无税单价'] = detail_df['原币无税单价'].apply(lambda x: float(str(x).replace(',', '')))
    detail_df['原币金额'] = detail_df['原币金额'].apply(lambda x: float(str(x).replace(',', '')))
    detail_df['原币单价'] = detail_df['原币单价'].apply(lambda x: float(str(x).replace(',', '')))
    detail_df['原币单价']=detail_df['原币单价'].round(2)

    detail_df['原币税额'] = detail_df['原币税额'].apply(lambda x: float(str(x).replace(',', '')))
    detail_df['原币价税合计'] = detail_df['原币价税合计'].apply(lambda x: float(str(x).replace(',', '')))
    detail_df['年份']=detail_df['发票日期'].dt.year
    detail_df['季度']=detail_df['发票日期'].dt.quarter
    detail_df['月份']=detail_df['发票日期'].dt.month
    #23年数据存入数据库
    detail_to_sql_df=detail_df
    # print('detail_to_sql_df',detail_to_sql_df)
    detail_to_sql_df.rename(columns={'序号':'no','发票类型':'invoicetype','发票号':'invoicecode','发票日期':'invoicedate','供应商':'supplier','存货编码':'productcode','存货名称':'productname','规格型号':'spec','主计量':'unit','税率':'taxrate','数量':'quantity','原币无税单价':'pricewithouttax','原币单价':'price','原币金额':'sumwithouttax','原币税额':'tax','原币价税合计':'sum','订单号':'ordercode','入库单号':'entrycode','项目名称':'project','品牌':'brand','走账方式':'paycompany','年份':'year','季度':'quarter','月份':'month'},inplace=True)
    # print('detail_to_sql_df',detail_to_sql_df)
    detail_to_sql_connect = create_engine('postgresql+psycopg://' + settings.PG_DBUSER + ':' + settings.PG_PASSWORD + '@'+settings.PG_HOST + ':'+settings.PG_PORT+'/'+settings.PG_DBNAME)
    print('settings.PG_DBNAME',settings.PG_DBNAME)
    detail_to_sql_connect_conn = detail_to_sql_connect.connect()

    detail_to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLIERS"."{}"'.format(table))   
    detail_to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLIERS"."{}" RESTART WITH 1'.format(seq))
    # detail_to_sql_connect_conn.execute(text('''SELECT setval('"SUPPLIERS"."{}"', 1, true)'''.format(seq)))

    # print(detail_to_sql_connect_conn.execute(text('select * from  "SUPPLIERS"."XEY2122" limit 3')).fetchall())
    # detail_to_sql_connect.dispose()
    # detail_to_sql_connect_conn.close()
    try:
        detail_to_sql_df.to_sql(table, con=detail_to_sql_connect, schema='SUPPLIERS', if_exists='append', index=False)
        print('已上传')
    except Exception as e:
        print('错误：{}'.format(e))

    detail_to_sql_connect.dispose()
    detail_to_sql_connect_conn.close()
    return '上传数据库成功'





def TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table):
    conn = psycopg.connect(
        dbname=settings.PG_DBNAME,
        user=settings.PG_DBUSER,
        password=settings.PG_PASSWORD,
        port=settings.PG_PORT,
        host=settings.PG_HOST
    )
  
    #读取21-22年数据
    detail_21_22_sql ='select * from  "SUPPLIERS"."{}"'.format(table2122)
    detail_21_22_df = pd.read_sql_query(detail_21_22_sql,con=conn)
    detail_21_22_df=detail_21_22_df[['no','invoicetype','invoicecode','invoicedate','supplier','productcode','productname','spec','unit','taxrate','quantity','pricewithouttax','price','sumwithouttax','tax','sum','ordercode','entrycode','project','brand','paycompany','year','quarter','month']]
    detail_21_22_df.rename(columns={'no':'序号','invoicetype':'发票类型','invoicecode':'发票号','invoicedate':'发票日期','supplier':'供应商','productcode':'存货编码','productname':'存货名称','spec':'规格型号','unit':'主计量','taxrate':'税率','quantity':'数量','pricewithouttax':'原币无税单价','price':'原币单价','sumwithouttax':'原币金额','tax':'原币税额','sum':'原币价税合计','ordercode':'订单号','entrycode':'入库单号','project':'项目名称','brand':'品牌','paycompany':'走账方式','year':'年份','quarter':'季度','month':'月份'},inplace=True)
    detail_21_22_df['数量'] = detail_21_22_df['数量'].apply(lambda x: float(str(x).replace(',', '')))
    detail_21_22_df['原币无税单价'] = detail_21_22_df['原币无税单价'].apply(lambda x: float(str(x).replace(',', '')))
    detail_21_22_df['原币金额'] = detail_21_22_df['原币金额'].apply(lambda x: float(str(x).replace(',', '')))
    detail_21_22_df['原币单价'] = detail_21_22_df['原币单价'].apply(lambda x: float(str(x).replace(',', '')))
    detail_21_22_df['原币单价']=detail_21_22_df['原币单价'].round(2)
    detail_21_22_df['原币税额'] = detail_21_22_df['原币税额'].apply(lambda x: float(str(x).replace(',', '')))
    detail_21_22_df['原币价税合计'] = detail_21_22_df['原币价税合计'].apply(lambda x: float(str(x).replace(',', '')))
    
    #读取23年数据
    detail_23_sql ='select * from  "SUPPLIERS"."{}"'.format(table23)
    detail_23_df = pd.read_sql_query(detail_23_sql,con=conn)
    detail_23_df=detail_23_df[['no','invoicetype','invoicecode','invoicedate','supplier','productcode','productname','spec','unit','taxrate','quantity','pricewithouttax','price','sumwithouttax','tax','sum','ordercode','entrycode','project','brand','paycompany','year','quarter','month']]
    detail_23_df.rename(columns={'no':'序号','invoicetype':'发票类型','invoicecode':'发票号','invoicedate':'发票日期','supplier':'供应商','productcode':'存货编码','productname':'存货名称','spec':'规格型号','unit':'主计量','taxrate':'税率','quantity':'数量','pricewithouttax':'原币无税单价','price':'原币单价','sumwithouttax':'原币金额','tax':'原币税额','sum':'原币价税合计','ordercode':'订单号','entrycode':'入库单号','project':'项目名称','brand':'品牌','paycompany':'走账方式','year':'年份','quarter':'季度','month':'月份'},inplace=True)
    detail_23_df['数量'] = detail_23_df['数量'].apply(lambda x: float(str(x).replace(',', '')))
    detail_23_df['原币无税单价'] = detail_23_df['原币无税单价'].apply(lambda x: float(str(x).replace(',', '')))
    detail_23_df['原币金额'] = detail_23_df['原币金额'].apply(lambda x: float(str(x).replace(',', '')))
    detail_23_df['原币单价'] = detail_23_df['原币单价'].apply(lambda x: float(str(x).replace(',', '')))
    detail_23_df['原币单价']=detail_23_df['原币单价'].round(2)
    detail_23_df['原币税额'] = detail_23_df['原币税额'].apply(lambda x: float(str(x).replace(',', '')))
    detail_23_df['原币价税合计'] = detail_23_df['原币价税合计'].apply(lambda x: float(str(x).replace(',', '')))

    #读取24年数据
    detail_24_sql ='select * from  "SUPPLIERS"."{}"'.format(table24)
    detail_24_df = pd.read_sql_query(detail_24_sql,con=conn)
    detail_24_df=detail_24_df[['no','invoicetype','invoicecode','invoicedate','supplier','productcode','productname','spec','unit','taxrate','quantity','pricewithouttax','price','sumwithouttax','tax','sum','ordercode','entrycode','project','brand','paycompany','year','quarter','month']]
    detail_24_df.rename(columns={'no':'序号','invoicetype':'发票类型','invoicecode':'发票号','invoicedate':'发票日期','supplier':'供应商','productcode':'存货编码','productname':'存货名称','spec':'规格型号','unit':'主计量','taxrate':'税率','quantity':'数量','pricewithouttax':'原币无税单价','price':'原币单价','sumwithouttax':'原币金额','tax':'原币税额','sum':'原币价税合计','ordercode':'订单号','entrycode':'入库单号','project':'项目名称','brand':'品牌','paycompany':'走账方式','year':'年份','quarter':'季度','month':'月份'},inplace=True)
    detail_24_df['数量'] = detail_24_df['数量'].apply(lambda x: float(str(x).replace(',', '')))
    detail_24_df['原币无税单价'] = detail_24_df['原币无税单价'].apply(lambda x: float(str(x).replace(',', '')))
    detail_24_df['原币金额'] = detail_24_df['原币金额'].apply(lambda x: float(str(x).replace(',', '')))
    detail_24_df['原币单价'] = detail_24_df['原币单价'].apply(lambda x: float(str(x).replace(',', '')))
    detail_24_df['原币单价']=detail_24_df['原币单价'].round(2)
    detail_24_df['原币税额'] = detail_24_df['原币税额'].apply(lambda x: float(str(x).replace(',', '')))
    detail_24_df['原币价税合计'] = detail_24_df['原币价税合计'].apply(lambda x: float(str(x).replace(',', '')))
    #合并21-24年
    if detail_24_df.empty: #如果没有24年数据
        detail_total_df=pd.concat([detail_21_22_df,detail_23_df], ignore_index=True)
    else:
        detail_total_df=pd.concat([detail_21_22_df,detail_23_df,detail_24_df], ignore_index=True)
    detail_total_df['发票日期'] = pd.to_datetime(detail_total_df['发票日期'])
    
    #供应商列表更新
    supplierlist=detail_total_df['供应商'].unique()
    supplierlist_df = pd.DataFrame({'供应商': supplierlist})
    supplierlist_df.rename(columns={'供应商':'supplier'},inplace=True)
    #先从数据库拿供应商基础信息
    supplier_info_sql ='''select * from "SUPPLIERS"."Supplier_info" where is_active=True and project ={}'''.format("'"+project+"'")  #可以写format
    supplier_info_df = pd.read_sql_query(supplier_info_sql,con=conn)
    supplier_info_df=supplier_info_df.drop_duplicates(subset=['supplier'], keep='first')
    conn.close()
    
    new_suppliers = supplierlist_df[~supplierlist_df['supplier'].isin(supplier_info_df['supplier'])]
    print('new_suppliers',new_suppliers)
    connect =create_engine('postgresql+psycopg://' + settings.PG_DBUSER + ':' + settings.PG_PASSWORD + '@'+settings.PG_HOST + ':'+settings.PG_PORT+'/'+settings.PG_DBNAME)
    if not new_suppliers.empty:
        print('将新的供应商数据插入表2中')
        new_data_to_insert = new_suppliers.copy()
        new_data_to_insert.loc[:,'contact'] = '未填报'  
        new_data_to_insert.loc[:,'payterm'] = '未填报'  
        new_data_to_insert.loc[:,'tax'] = '未填报'
        new_data_to_insert.loc[:,'delivery'] = '未填报'
        new_data_to_insert.loc[:,'project'] = project  
        new_data_to_insert.to_sql('Supplier_info', connect, schema='SUPPLIERS', if_exists='append', index=False)
    else:
        print('供应商基础信息一模一样 无需添加')
    connect.dispose()
    print('数据库中的Supplier_info更新完成')
    
    #供应商排序
    suppliers_pivot_df = detail_total_df.pivot_table(index='供应商', columns='年份', values=['数量','原币价税合计'], aggfunc='sum', fill_value=0)
    suppliers_pivot_df.columns = [f'{col[0]}_{col[1]}' if col[1] else f'{col[0]}' for col in suppliers_pivot_df.columns]
    suppliers_pivot_df=suppliers_pivot_df.reset_index()

    #如果有24年的话，要多两列，在插入数据的时候也可以判断，然后建不同的表
    if '原币价税合计_2024' in suppliers_pivot_df.columns:
        suppliers_pivot_df.rename(columns={ '原币价税合计_2021':'21年采购金额','原币价税合计_2022':'22年采购金额','原币价税合计_2023':'23年采购金额','原币价税合计_2024':'24年采购金额','数量_2021':'21年采购数量','数量_2022':'22年采购数量','数量_2023':'23年采购数量','数量_2024':'24年采购数量'},inplace=True)
        suppliers_pivot_df['采购总数量'] = suppliers_pivot_df['21年采购数量'] + suppliers_pivot_df['22年采购数量']+ suppliers_pivot_df['23年采购数量']+ suppliers_pivot_df['24年采购数量']
        suppliers_pivot_df['采购总金额'] = suppliers_pivot_df['21年采购金额'] + suppliers_pivot_df['22年采购金额']+ suppliers_pivot_df['23年采购金额']+ suppliers_pivot_df['24年采购金额']
        suppliers_pivot_df.sort_values(by=['24年采购金额', '采购总金额'], ascending=[False, False],inplace=True)
        suppliers_pivot_df.reset_index(inplace=True)
        suppliers_pivot_df['排序'] = range(1, len(suppliers_pivot_df)+1)
        suppliers_pivot_df=suppliers_pivot_df[['排序','供应商', '21年采购数量', '22年采购数量', '23年采购数量' ,'24年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','24年采购金额','采购总金额']]

    else:
        suppliers_pivot_df.rename(columns={ '原币价税合计_2021':'21年采购金额','原币价税合计_2022':'22年采购金额','原币价税合计_2023':'23年采购金额','数量_2021':'21年采购数量','数量_2022':'22年采购数量','数量_2023':'23年采购数量'},inplace=True)
        suppliers_pivot_df['采购总数量'] = suppliers_pivot_df['21年采购数量'] + suppliers_pivot_df['22年采购数量']+ suppliers_pivot_df['23年采购数量']
        suppliers_pivot_df['采购总金额'] = suppliers_pivot_df['21年采购金额'] + suppliers_pivot_df['22年采购金额']+ suppliers_pivot_df['23年采购金额']
        suppliers_pivot_df.sort_values(by=['23年采购金额', '采购总金额'], ascending=[False, False],inplace=True)
        suppliers_pivot_df.reset_index(inplace=True)
        suppliers_pivot_df['排序'] = range(1, len(suppliers_pivot_df)+1)
        suppliers_pivot_df=suppliers_pivot_df[['排序','供应商', '21年采购数量', '22年采购数量', '23年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','采购总金额']]

    #存货汇总
    productprice_df = detail_total_df.sort_values(by=['发票日期', '原币单价'], ascending=[False, True]).groupby(['存货编码', '存货名称', '规格型号','主计量','供应商','品牌']).head(1)
    productprice_df=productprice_df.reset_index(drop=True)
    # productprice_df = detail_total_df.groupby(['存货编码', '存货名称', '供应商','规格型号','主计量','品牌']).apply(lambda x: x.loc[x['发票日期'].idxmax()])[['存货编码', '存货名称', '供应商','规格型号','主计量','品牌','发票日期', '原币单价']].reset_index(drop=True)
    product_pivot_df = detail_total_df.pivot_table(index=['存货编码', '存货名称', '供应商','规格型号','主计量','品牌'], columns='年份', values=['数量','原币价税合计'], aggfunc='sum', fill_value=0)
    product_pivot_df.columns = ['_'.join(map(str, col)) for col in product_pivot_df.columns.values]
    product_pivot_df = product_pivot_df.reset_index()

    if '原币价税合计_2024' in product_pivot_df.columns:
        product_pivot_df.rename(columns={ '原币价税合计_2021':'21年采购金额','原币价税合计_2022':'22年采购金额','原币价税合计_2023':'23年采购金额','原币价税合计_2024':'24年采购金额','数量_2021':'21年采购数量','数量_2022':'22年采购数量','数量_2023':'23年采购数量','数量_2024':'24年采购数量'},inplace=True)
        product_pivot_df['采购总数量'] = product_pivot_df['21年采购数量'] + product_pivot_df['22年采购数量']+ product_pivot_df['23年采购数量']+ product_pivot_df['24年采购数量']
        product_pivot_df['采购总金额'] = product_pivot_df['21年采购金额'] + product_pivot_df['22年采购金额']+ product_pivot_df['23年采购金额']+ product_pivot_df['24年采购金额']
        product_pivot_df.sort_values(by=['24年采购金额', '采购总金额','供应商'], ascending=[False, False,False],inplace=True)
        product_pivot_df.reset_index(inplace=True)
        product_pivot_df['排序'] = range(1, len(product_pivot_df)+1)
        product_pivot_df=product_pivot_df[['排序','存货编码','存货名称','供应商','规格型号','主计量','品牌','21年采购数量', '22年采购数量', '23年采购数量' ,'24年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','24年采购金额','采购总金额']]

    else:
        product_pivot_df.rename(columns={'原币价税合计_2021':'21年采购金额','原币价税合计_2022':'22年采购金额','原币价税合计_2023':'23年采购金额','数量_2021':'21年采购数量','数量_2022':'22年采购数量','数量_2023':'23年采购数量'},inplace=True)
        product_pivot_df['采购总数量'] = product_pivot_df['21年采购数量'] + product_pivot_df['22年采购数量']+ product_pivot_df['23年采购数量']
        product_pivot_df['采购总金额'] = product_pivot_df['21年采购金额'] + product_pivot_df['22年采购金额']+ product_pivot_df['23年采购金额']
        product_pivot_df.sort_values(by=['23年采购金额', '采购总金额','供应商'], ascending=[False, False,False],inplace=True)
        product_pivot_df.reset_index(inplace=True)
        product_pivot_df['排序'] = range(1, len(product_pivot_df)+1)
        product_pivot_df=product_pivot_df[['排序','存货编码','存货名称','供应商','规格型号','主计量','品牌', '21年采购数量', '22年采购数量', '23年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','采购总金额']]

    product_rank=product_pivot_df.merge(productprice_df,how='left',on=['存货编码', '存货名称', '供应商','规格型号','主计量','品牌'])
    product_rank.rename(columns={ '发票日期':'最近发票日期','原币单价':'单价','主计量':'单位'},inplace=True)
    product_rank

    if '24年采购金额' in product_rank.columns:
        product_rank=product_rank[['排序','存货编码','存货名称','规格型号','单位','供应商','品牌','最近发票日期','单价', '21年采购数量', '22年采购数量', '23年采购数量','24年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','24年采购金额','采购总金额']]
    else:
        product_rank=product_rank[['排序','存货编码','存货名称','规格型号','单位','供应商','品牌', '最近发票日期','单价','21年采购数量', '22年采购数量', '23年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','采购总金额']]

    #供应商销量汇总表
    productpricedetail_df= detail_total_df.groupby(['存货编码', '存货名称', '供应商','规格型号','主计量','品牌','原币单价']).agg({'发票日期': 'max'}).reset_index()
    product_price_pivot_df = detail_total_df.pivot_table(index=[ '供应商','存货编码', '存货名称','规格型号','主计量','品牌','原币单价'], columns='年份', values=['数量','原币价税合计'], aggfunc='sum', fill_value=0)
    product_price_pivot_df.columns = ['_'.join(map(str, col)) for col in product_price_pivot_df.columns.values]
    product_price_pivot_df = product_price_pivot_df.reset_index()

    if '原币价税合计_2024' in product_price_pivot_df.columns:
        product_price_pivot_df.rename(columns={ '原币价税合计_2021':'21年采购金额','原币价税合计_2022':'22年采购金额','原币价税合计_2023':'23年采购金额','原币价税合计_2024':'24年采购金额','数量_2021':'21年采购数量','数量_2022':'22年采购数量','数量_2023':'23年采购数量','数量_2024':'24年采购数量'},inplace=True)
        product_price_pivot_df['采购总数量'] = product_price_pivot_df['21年采购数量'] + product_price_pivot_df['22年采购数量']+ product_price_pivot_df['23年采购数量']+ product_price_pivot_df['24年采购数量']
        product_price_pivot_df['采购总金额'] = product_price_pivot_df['21年采购金额'] + product_price_pivot_df['22年采购金额']+ product_price_pivot_df['23年采购金额']+ product_price_pivot_df['24年采购金额']
    else:
        product_price_pivot_df.rename(columns={'原币价税合计_2021':'21年采购金额','原币价税合计_2022':'22年采购金额','原币价税合计_2023':'23年采购金额','数量_2021':'21年采购数量','数量_2022':'22年采购数量','数量_2023':'23年采购数量'},inplace=True)
        product_price_pivot_df['采购总数量'] = product_price_pivot_df['21年采购数量'] + product_price_pivot_df['22年采购数量']+ product_price_pivot_df['23年采购数量']
        product_price_pivot_df['采购总金额'] = product_price_pivot_df['21年采购金额'] + product_price_pivot_df['22年采购金额']+ product_price_pivot_df['23年采购金额']
    
    supplier_product_summary_df=product_price_pivot_df.merge(productpricedetail_df,how='left',on=['存货编码', '存货名称', '供应商','规格型号','主计量','品牌','原币单价'])
    supplier_product_summary_df.rename(columns={ '发票日期':'最近发票日期','原币单价':'单价','主计量':'单位'},inplace=True)

    if '24年采购金额' in supplier_product_summary_df.columns:
        supplier_product_summary_df.sort_values(by=['供应商', '存货编码','最近发票日期'], ascending=[True, True,False],inplace=True)
        supplier_product_summary_df.reset_index(inplace=True)
        supplier_product_summary_df['排序'] = range(1, len(supplier_product_summary_df)+1)
        supplier_product_summary_df=supplier_product_summary_df.merge(supplier_info_df[['supplier','contact','payterm','tax','delivery']],how='left',left_on='供应商',right_on='supplier')
        supplier_product_summary_df=supplier_product_summary_df[['供应商','contact','payterm','tax','delivery','存货编码','存货名称','规格型号','单位','品牌','最近发票日期','单价', '21年采购数量', '22年采购数量', '23年采购数量','24年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','24年采购金额','采购总金额']]
    else:
        supplier_product_summary_df.sort_values(by=['供应商', '存货编码','最近发票日期'], ascending=[True, True,False],inplace=True)
        supplier_product_summary_df.reset_index(inplace=True)
        supplier_product_summary_df['排序'] = range(1, len(supplier_product_summary_df)+1)
        supplier_product_summary_df=supplier_product_summary_df.merge(supplier_info_df[['supplier','contact','payterm','tax','delivery']],how='left',left_on='供应商',right_on='supplier')
        supplier_product_summary_df=supplier_product_summary_df[['供应商','contact','payterm','tax','delivery','存货编码','存货名称','规格型号','单位','品牌','最近发票日期','单价', '21年采购数量', '22年采购数量', '23年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','采购总金额']]

    supplier_product_summary_df.rename(columns={'contact':'联系方式','payterm':'账期','tax':'税率','delivery':'配送方式'},inplace=True)
    supplier_product_summary_df=supplier_product_summary_df.merge(suppliers_pivot_df[['排序','供应商']],how='left',on='供应商')
    supplier_product_summary_df.rename(columns={'排序':'供应商排序'},inplace=True)
    supplier_product_summary_df.sort_values(by=['供应商排序', '存货编码','最近发票日期'], ascending=[True, True,False],inplace=True)
    supplier_product_summary_df['排序'] = range(1, len(supplier_product_summary_df)+1)
    
    if '24年采购金额' in supplier_product_summary_df.columns:
        supplier_product_summary_df=supplier_product_summary_df[['排序','供应商排序','供应商','联系方式','账期','税率','配送方式','存货编码','存货名称','规格型号','单位','品牌','最近发票日期','单价', '21年采购数量', '22年采购数量', '23年采购数量','24年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','24年采购金额','采购总金额']]
    else:
        supplier_product_summary_df=supplier_product_summary_df[['排序','供应商排序','供应商','联系方式','账期','税率','配送方式','存货编码','存货名称','规格型号','单位','品牌','最近发票日期','单价', '21年采购数量', '22年采购数量', '23年采购数量','采购总数量','21年采购金额','22年采购金额','23年采购金额','采购总金额']]

    #保存
    result_list = [suppliers_pivot_df,supplier_product_summary_df,product_rank]
    sheet_name_list = ['供应商排行','供应商销量汇总','存货信息汇总']
    writer = pd.ExcelWriter(filename)
    for i in range(len(result_list)):
        result_list[i]=result_list[i].style.set_properties(**{'text-align': 'center'}) ## 使excel表格中的数据居中对齐
        result_list[i].to_excel(writer, sheet_name=sheet_name_list[i],index=False)
        worksheet = writer.sheets[sheet_name_list[i]]
    #     worksheet.set_column('A:B',16) ## 设置excel表格列宽为16
    writer.close()
    print('excel保存成功')
    
    #保存数据库
    suppliers_to_sql= suppliers_pivot_df
    suppliers_to_sql['project']=project
    suppliers_to_sql['id']=suppliers_to_sql['排序']

    supplier_product_summary_to_sql=supplier_product_summary_df
    supplier_product_summary_to_sql['project']=project
    supplier_product_summary_to_sql['id']=supplier_product_summary_to_sql['排序']

    product_rank_to_sql=product_rank
    product_rank_to_sql['project']=project
    product_rank_to_sql['id']=product_rank_to_sql['排序']

    if '24年采购金额' in suppliers_to_sql.columns:
        suppliers_to_sql.rename(columns={'排序':'rank','供应商':'supplier','21年采购数量':'qty21','22年采购数量':'qty22','23年采购数量':'qty23','24年采购数量':'qty24','采购总数量':'totalqty','21年采购金额':'sum21','22年采购金额':'sum22','23年采购金额':'sum23','24年采购金额':'sum24','采购总金额':'totalsum'},inplace=True)
        supplier_product_summary_to_sql.rename(columns={'排序':'rank','供应商排序':'supplierrank','供应商':'supplier','联系方式':'contact','账期':'payterm','税率':'tax','配送方式':'delivery','存货编码':'productcode','存货名称':'productname','规格型号':'spec','单位':'unit','品牌':'brand','最近发票日期':'recentdate','单价':'price','21年采购数量':'qty21','22年采购数量':'qty22','23年采购数量':'qty23','24年采购数量':'qty24','采购总数量':'totalqty','21年采购金额':'sum21','22年采购金额':'sum22','23年采购金额':'sum23','24年采购金额':'sum24','采购总金额':'totalsum'},inplace=True)
        product_rank_to_sql.rename(columns={'排序':'rank','存货编码':'productcode','存货名称':'productname','规格型号':'spec','单位':'unit','供应商':'supplier','品牌':'brand','最近发票日期':'recentdate','单价':'price', '21年采购数量':'qty21','22年采购数量':'qty22','23年采购数量':'qty23','24年采购数量':'qty24','采购总数量':'totalqty','21年采购金额':'sum21','22年采购金额':'sum22','23年采购金额':'sum23','24年采购金额':'sum24','采购总金额':'totalsum'},inplace=True)
    else:
        suppliers_to_sql.rename(columns={'排序':'rank','供应商':'supplier','21年采购数量':'qty21','22年采购数量':'qty22','23年采购数量':'qty23','采购总数量':'totalqty','21年采购金额':'sum21','22年采购金额':'sum22','23年采购金额':'sum23','采购总金额':'totalsum'},inplace=True)
        supplier_product_summary_to_sql.rename(columns={'排序':'rank','供应商排序':'supplierrank','供应商':'supplier','联系方式':'contact','账期':'payterm','税率':'tax','配送方式':'delivery','存货编码':'productcode','存货名称':'productname','规格型号':'spec','单位':'unit','品牌':'brand','最近发票日期':'recentdate','单价':'price','21年采购数量':'qty21','22年采购数量':'qty22','23年采购数量':'qty23','采购总数量':'totalqty','21年采购金额':'sum21','22年采购金额':'sum22','23年采购金额':'sum23','采购总金额':'totalsum'},inplace=True)
        product_rank_to_sql.rename(columns={'排序':'rank','存货编码':'productcode','存货名称':'productname','规格型号':'spec','单位':'unit','供应商':'supplier','品牌':'brand','最近发票日期':'recentdate','单价':'price', '21年采购数量':'qty21','22年采购数量':'qty22','23年采购数量':'qty23','采购总数量':'totalqty','21年采购金额':'sum21','22年采购金额':'sum22','23年采购金额':'sum23','采购总金额':'totalsum'},inplace=True)

    to_sql_connect = create_engine('postgresql+psycopg://' + settings.PG_DBUSER + ':' + settings.PG_PASSWORD + '@'+settings.PG_HOST + ':'+settings.PG_PORT+'/'+settings.PG_DBNAME)
    to_sql_connect_conn = to_sql_connect.connect()
    print('数据库链接成功')
    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLIERS"."{}" CASCADE'.format(Supplier_Rank_table))
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLIERS"."{}" RESTART WITH 1'.format(supplierrank_id_seq_table))

    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLIERS"."{}"'.format(Supplier_Product_Summary_table))
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLIERS"."{}" RESTART WITH 1'.format(supplierproductsummary_id_seq_table))

    to_sql_connect_conn.execute('TRUNCATE TABLE "SUPPLIERS"."{}"'.format(Product_Rank_table))
    to_sql_connect_conn.execute('ALTER SEQUENCE "SUPPLIERS"."{}" RESTART WITH 1'.format(productrank_id_seq_table))
    
    suppliers_to_sql.to_sql(Supplier_Rank_table, con=to_sql_connect, schema='SUPPLIERS', if_exists='append', index=False)
    supplier_product_summary_to_sql.to_sql(Supplier_Product_Summary_table, con=to_sql_connect, schema='SUPPLIERS', if_exists='append', index=False)
    product_rank_to_sql.to_sql(Product_Rank_table, con=to_sql_connect, schema='SUPPLIERS', if_exists='append', index=False)

    to_sql_connect.dispose()
    to_sql_connect_conn.close()
    print('所有表格成功上传数据库，关闭链接')
    return 'success'



if __name__=='__main__':
    rawdata23 = 'C:\\Users\\赵文茜\\Desktop\\徐二院测试24年.xlsx'  
    project='徐二院'
    table23='XEY24'
    seq23='xey24_id_seq'
    RawSaveToSql(rawdata23,project,table23,seq23)
    print('原始数据已上传')

                    
    table2122='XEY2122'
    table23='XEY23'
    table24='XEY24'
    project='徐二院'
    filename=r'C:\\Users\\赵文茜\\Desktop\\供应商信息_徐二院.xlsx'
    Supplier_Rank_table='XEY_Supplier_Rank'
    supplierrank_id_seq_table='xeysupplierrank_id_seq'
    Supplier_Product_Summary_table='XEY_Supplier_Product_Summary'
    supplierproductsummary_id_seq_table='xeysupplierproductsummary_id_seq'
    Product_Rank_table='XEY_Product_Rank'
    productrank_id_seq_table='xeyproductrank_id_seq'
    TransformData(table2122,table23,table24,project,filename,Supplier_Rank_table,supplierrank_id_seq_table,Supplier_Product_Summary_table,supplierproductsummary_id_seq_table,Product_Rank_table,productrank_id_seq_table)


