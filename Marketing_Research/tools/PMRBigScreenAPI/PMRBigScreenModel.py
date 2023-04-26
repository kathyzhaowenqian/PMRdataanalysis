# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def InitData(data,year,companyname):
    company_research_df=data[(data['company']==companyname) & (data['year']==year)]
    return company_research_df

def InitProjectData(data,year,companyname,project):
    company_research_df=data[(data['company']==companyname) & (data['year']==year)& (data['project']==project)]
    return company_research_df

#普美瑞直销业务重点项目数量
def ProjectCount(data):
    project_count=data['project'].nunique()
    return project_count

#覆盖医院数量
def HospitalCount(data):
    hospitalname_count=data['hospitalname'].nunique()
    return hospitalname_count

#已有我司仪器的医院数量 不分项目
def HospitalnameWithOwnmachineCount(data):
    hospitalname_withownmachine_count=data[data['newold']=='已有业务(含我司仪器)']['hospitalname'].nunique()
    return hospitalname_withownmachine_count 

#今年已开票医院数量(初始值是0)
def HospitalnameWithValueCount(data):
    hospitalname_withvalue_count=data[(data['q1actualsales']!=0)|(data['q2actualsales']!=0)|(data['q3actualsales']!=0)|(data['q4actualsales']!=0)]['hospitalname'].nunique()
    return hospitalname_withvalue_count 

#总测试数，
def TestspermonthCount(data):
    testspermonth_count=data.drop_duplicates('id')['testspermonth'].sum()
    return testspermonth_count

#我司的测试数，
def OWNtestspermonthCount(data):
    owntestspermonth_count=data.drop_duplicates('id')['owntestspermonth'].sum()
    return owntestspermonth_count 

#所覆盖医院截至目前开票总额，
def SalesValueTotal(data):
    salesvaluetotal=data.drop_duplicates('id')['q1actualsales'].sum()+data.drop_duplicates('id')['q2actualsales'].sum()+data.drop_duplicates('id')['q3actualsales'].sum()+data.drop_duplicates('id')['q4actualsales'].sum()
    return salesvaluetotal
#所覆盖医院Q1开票总额，
def Q1SalesValueTotal(data):
    q1salesvaluetotal=data.drop_duplicates('id')['q1actualsales'].sum()
    return q1salesvaluetotal

#所覆盖医院Q2开票总额，
def Q2SalesValueTotal(data):
    q2salesvaluetotal=data.drop_duplicates('id')['q2actualsales'].sum()
    return q2salesvaluetotal 

#所覆盖医院Q3开票总额，
def Q3SalesValueTotal(data):
    q3salesvaluetotal=data.drop_duplicates('id')['q3actualsales'].sum()
    return q3salesvaluetotal 

#所覆盖医院Q4开票总额，
def Q4SalesValueTotal(data):
    q4salesvaluetotal=data.drop_duplicates('id')['q4actualsales'].sum()
    return q4salesvaluetotal 
#市场总仪器数
def OWNNumberCount(data):
    ownmachine_df=data.drop_duplicates('id')['ownmachinenumber'].sum()
    return ownmachine_df

#我司仪器数
def TotalMachineNumberCount(data):
    totalmachine_df=data.drop_duplicates('id')['totalmachinenumber'].sum()
    return totalmachine_df

#各地区分配的医院数量
def HospitalnameDistrictCount(data):
    hospitalname_district_df=data.groupby('district').agg({'hospitalname': pd.Series.nunique})
    hospitalname_district_df.sort_values(by='hospitalname',inplace=True,ascending=False)
    hospitalname_district_df=hospitalname_district_df.reset_index()
    return hospitalname_district_df

#各销售分配的医院数量
def SalesmanHospitalCount(data):
    salesman1_hospitalnumber_df=data.groupby('salesman1').agg({'hospitalname': pd.Series.nunique})
    salesman1_hospitalnumber_df.sort_values(by='hospitalname',ascending=False,inplace=True)
    salesman1_hospitalnumber_df=salesman1_hospitalnumber_df.reset_index()
    return salesman1_hospitalnumber_df

#各销售有效填报的医院项目率 有效填报了仪器，品牌不为空 数量不为0
def SalesmanFillEffectiveness(data):
    salesman1_needtofill_df=data.groupby('salesman1').agg({'id': pd.Series.nunique}).reset_index()   
    salesman1_effective_df=data[(~data['brand'].isnull()) & (data['machinenumber']!=0)].groupby('salesman1').agg({'id': pd.Series.nunique}).reset_index()
    salesman1_effective_df=pd.merge(salesman1_needtofill_df,salesman1_effective_df,how ='left',on='salesman1')
    salesman1_effective_df.rename(columns={'id_x':'needtofill','id_y':'effectivefill'},inplace=True)
    salesman1_effective_df.replace([np.inf,np.nan],0,inplace=True)
    salesman1_effective_df['effectiveness']=(salesman1_effective_df['effectivefill']/salesman1_effective_df['needtofill']).round(2)
    salesman1_effective_df.sort_values(by='effectiveness',ascending=False, inplace=True)
    salesman1_effective_df=salesman1_effective_df[['salesman1','effectivefill','needtofill','effectiveness']]
    salesman1_effective_df=salesman1_effective_df.reset_index()
    salesman1_effective_df.drop(columns='index',inplace=True)
    return salesman1_effective_df

#医院今年截至今日，开票额总排行  ，具体要有医院名称、金额和销售名称
def HospitalSalesRank(data):
    saleshospitalrank_df=data.drop_duplicates('id') #把同一医院同一项目但是有多个仪器的情况排除掉，只保留一行
    saleshospitalrank_df=saleshospitalrank_df.groupby(['hospitalname','salesman1']).agg({'q1actualsales':sum,'q2actualsales':sum,'q3actualsales':sum,'q4actualsales':sum})
    saleshospitalrank_df['thisyear_totalactualsales']=saleshospitalrank_df['q1actualsales']+saleshospitalrank_df['q2actualsales']+saleshospitalrank_df['q3actualsales']+saleshospitalrank_df['q4actualsales']
    saleshospitalrank_df=saleshospitalrank_df.sort_values(by='thisyear_totalactualsales',ascending=False).reset_index()
    saleshospitalrank_dfsum=saleshospitalrank_df['thisyear_totalactualsales'].sum()
    if saleshospitalrank_dfsum==0:
        saleshospitalrank_df['%']=0
    else:
        saleshospitalrank_df['%']=(saleshospitalrank_df['thisyear_totalactualsales']/saleshospitalrank_dfsum)
    saleshospitalrank_df=saleshospitalrank_df.reset_index()
    saleshospitalrank_df['index']=saleshospitalrank_df['index']+1
    saleshospitalrank_df.rename(columns={'index':'rank'},inplace=True)
    return saleshospitalrank_df

# #各人员的目标完成情况【进度条】
# def SalesmanComplete(data):
#     salesman1complete_df=data.drop_duplicates('id').groupby('salesman1').agg({'q1target':sum,'q1actualsales':sum,'q2target':sum,'q2actualsales':sum,'q3target':sum,'q3actualsales':sum,'q4target':sum,'q4actualsales':sum})
#     salesman1complete_df['totaltarget']=salesman1complete_df['q1target']+salesman1complete_df['q2target']+salesman1complete_df['q3target']+salesman1complete_df['q4target']
#     salesman1complete_df['totalactualsales']=salesman1complete_df['q1actualsales']+salesman1complete_df['q2actualsales']+salesman1complete_df['q3actualsales']+salesman1complete_df['q4actualsales']
#     salesman1complete_df=salesman1complete_df.sort_values(by='totalactualsales',ascending=False).reset_index()
#     salesman1complete_df['q1finishrate']=salesman1complete_df['q1actualsales']/salesman1complete_df['q1target']
#     salesman1complete_df['q2finishrate']=salesman1complete_df['q2actualsales']/salesman1complete_df['q2target']
#     salesman1complete_df['q3finishrate']=salesman1complete_df['q3actualsales']/salesman1complete_df['q3target']
#     salesman1complete_df['q4finishrate']=salesman1complete_df['q4actualsales']/salesman1complete_df['q4target']
#     salesman1complete_df.replace([np.inf,np.nan],'0',inplace=True)
#     salesman1complete_df=salesman1complete_df[['salesman1','q1target','q1actualsales','q1finishrate','q2target','q2actualsales','q2finishrate','q3target','q3actualsales','q3finishrate','q4target','q4actualsales','q4finishrate','totaltarget','totalactualsales']]
#     return salesman1complete_df
def if_zero(target,actual):
    if target==0:
        return 0   
    else:
        return actual/target
    
def SalesmanCompleteWithTarget(data):
    q1_salesman1complete_df=data[(data['q1target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id').groupby('salesman1').agg({'q1target':sum,'q1actualsales':sum})
    q2_salesman1complete_df=data[(data['q2target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id').groupby('salesman1').agg({'q2target':sum,'q2actualsales':sum})
    q3_salesman1complete_df=data[(data['q3target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id').groupby('salesman1').agg({'q3target':sum,'q3actualsales':sum})
    q4_salesman1complete_df=data[(data['q4target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id').groupby('salesman1').agg({'q4target':sum,'q4actualsales':sum})
    salesmanlist=data.drop_duplicates('id').groupby('salesman1')['hospitalname'].count().to_frame().reset_index()
    combine_salesman1complete_df=pd.merge(salesmanlist,q1_salesman1complete_df,how='left',on='salesman1')
    combine_salesman1complete_df.drop(['hospitalname'],axis=1,inplace=True)
    combine_salesman1complete_df=pd.merge(combine_salesman1complete_df,q2_salesman1complete_df,how='outer',on='salesman1')
    combine_salesman1complete_df=pd.merge(combine_salesman1complete_df,q3_salesman1complete_df,how='outer',on='salesman1')
    combine_salesman1complete_df=pd.merge(combine_salesman1complete_df,q4_salesman1complete_df,how='outer',on='salesman1')
    combine_salesman1complete_df.replace([np.inf,np.nan],0,inplace=True)
    combine_salesman1complete_df['totaltarget']=combine_salesman1complete_df['q1target']+combine_salesman1complete_df['q2target']+combine_salesman1complete_df['q3target']+combine_salesman1complete_df['q4target']
    combine_salesman1complete_df['totalactualsales']=combine_salesman1complete_df['q1actualsales']+combine_salesman1complete_df['q2actualsales']+combine_salesman1complete_df['q3actualsales']+combine_salesman1complete_df['q4actualsales']

    combine_salesman1complete_df['q1finishrate']=combine_salesman1complete_df.apply(lambda x:if_zero(x['q1target'],x['q1actualsales']), axis = 1)
    combine_salesman1complete_df['q2finishrate']=combine_salesman1complete_df.apply(lambda x:if_zero(x['q2target'],x['q2actualsales']), axis = 1)
    combine_salesman1complete_df['q3finishrate']=combine_salesman1complete_df.apply(lambda x:if_zero(x['q3target'],x['q3actualsales']), axis = 1)
    combine_salesman1complete_df['q4finishrate']=combine_salesman1complete_df.apply(lambda x:if_zero(x['q4target'],x['q4actualsales']), axis = 1)
    combine_salesman1complete_df['totalfinishrate']=combine_salesman1complete_df.apply(lambda x:if_zero(x['totaltarget'],x['totalactualsales']), axis = 1)
    combine_salesman1complete_df=combine_salesman1complete_df.sort_values(by='totalfinishrate',ascending=False).reset_index()
    combine_salesman1complete_df=combine_salesman1complete_df[['salesman1','q1target','q1actualsales','q1finishrate','q2target','q2actualsales','q2finishrate','q3target','q3actualsales','q3finishrate','q4target','q4actualsales','q4finishrate','totaltarget','totalactualsales','totalfinishrate']]
    return combine_salesman1complete_df


#Q1 各人员 有目标的数据的完成情况
def q1SalesmanCompleteWithTarget(data):
    q1_salesman1complete_df=data[(data['q1target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id').groupby('salesman1').agg({'q1target':sum,'q1actualsales':sum})
    salesmanlist=data.drop_duplicates('id').groupby('salesman1')['hospitalname'].count().to_frame().reset_index()
    q1combine_salesman1complete_df=pd.merge(salesmanlist,q1_salesman1complete_df,how='left',on='salesman1')
    q1combine_salesman1complete_df.drop(['hospitalname'],axis=1,inplace=True)
    q1combine_salesman1complete_df.replace([np.inf,np.nan],0,inplace=True)
    q1combine_salesman1complete_df['q1finishrate']=q1combine_salesman1complete_df.apply(lambda x:if_zero(x['q1target'],x['q1actualsales']), axis = 1)
    q1combine_salesman1complete_df.sort_values(by='q1finishrate',ascending=False,inplace=True)
    q1combine_salesman1complete_df=q1combine_salesman1complete_df.reset_index()
    q1combine_salesman1complete_df.drop(['index'],inplace=True,axis=1)
    return q1combine_salesman1complete_df


def q2SalesmanCompleteWithTarget(data):
    q2_salesman1complete_df=data[(data['q2target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id').groupby('salesman1').agg({'q2target':sum,'q2actualsales':sum})
    salesmanlist=data.drop_duplicates('id').groupby('salesman1')['hospitalname'].count().to_frame().reset_index()
    q2combine_salesman1complete_df=pd.merge(salesmanlist,q2_salesman1complete_df,how='left',on='salesman1')
    q2combine_salesman1complete_df.drop(['hospitalname'],axis=1,inplace=True)
    q2combine_salesman1complete_df.replace([np.inf,np.nan],0,inplace=True)
    q2combine_salesman1complete_df['q2finishrate']=q2combine_salesman1complete_df.apply(lambda x:if_zero(x['q2target'],x['q2actualsales']), axis = 1)
    q2combine_salesman1complete_df.sort_values(by='q2finishrate',ascending=False,inplace=True)
    q2combine_salesman1complete_df=q2combine_salesman1complete_df.reset_index()
    q2combine_salesman1complete_df.drop(['index'],inplace=True,axis=1)
    return q2combine_salesman1complete_df


def q3SalesmanCompleteWithTarget(data):
    q3_salesman1complete_df=data[(data['q3target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id').groupby('salesman1').agg({'q3target':sum,'q3actualsales':sum})
    salesmanlist=data.drop_duplicates('id').groupby('salesman1')['hospitalname'].count().to_frame().reset_index()
    q3combine_salesman1complete_df=pd.merge(salesmanlist,q3_salesman1complete_df,how='left',on='salesman1')
    q3combine_salesman1complete_df.drop(['hospitalname'],axis=1,inplace=True)
    q3combine_salesman1complete_df.replace([np.inf,np.nan],0,inplace=True)
    q3combine_salesman1complete_df['q3finishrate']=q3combine_salesman1complete_df.apply(lambda x:if_zero(x['q3target'],x['q3actualsales']), axis = 1)
    q3combine_salesman1complete_df.sort_values(by='q3finishrate',ascending=False,inplace=True)
    q3combine_salesman1complete_df=q3combine_salesman1complete_df.reset_index()
    q3combine_salesman1complete_df.drop(['index'],inplace=True,axis=1)
    return q3combine_salesman1complete_df



def q4SalesmanCompleteWithTarget(data):
    q4_salesman1complete_df=data[(data['q4target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id').groupby('salesman1').agg({'q4target':sum,'q4actualsales':sum})
    salesmanlist=data.drop_duplicates('id').groupby('salesman1')['hospitalname'].count().to_frame().reset_index()
    q4combine_salesman1complete_df=pd.merge(salesmanlist,q4_salesman1complete_df,how='left',on='salesman1')
    q4combine_salesman1complete_df.drop(['hospitalname'],axis=1,inplace=True)
    q4combine_salesman1complete_df.replace([np.inf,np.nan],0,inplace=True)
    q4combine_salesman1complete_df['q4finishrate']=q4combine_salesman1complete_df.apply(lambda x:if_zero(x['q4target'],x['q4actualsales']), axis = 1)
    q4combine_salesman1complete_df.sort_values(by='q4finishrate',ascending=False,inplace=True)
    q4combine_salesman1complete_df=q4combine_salesman1complete_df.reset_index()
    q4combine_salesman1complete_df.drop(['index'],inplace=True,axis=1)
    return q4combine_salesman1complete_df

#q2 总体目标额
def Q2targettotal(data):
    Q2target=data[(data['q2target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id')['q2target'].sum()
    return Q2target

#q2 含目标额的实际开票额
def Q2actualtotal(data):
    Q2actual=data[(data['q2target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id')['q2actualsales'].sum()
    return Q2actual

#q3 总体目标额
def Q3targettotal(data):
    Q3target=data[(data['q3target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id')['q3target'].sum()
    return Q3target

#q3 含目标额的实际开票额
def Q3actualtotal(data):
    Q3actual=data[(data['q3target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id')['q3actualsales'].sum()
    return Q3actual

#q4 总体目标额
def Q4targettotal(data):
    Q4target=data[(data['q4target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id')['q4target'].sum()
    return Q4target


#q4 含目标额的实际开票额
def Q4actualtotal(data):
    Q4actual=data[(data['q4target']!=0) & (data['totalsumpermonth']==0)].drop_duplicates('id')['q4actualsales'].sum()
    return Q4actual



#各项目的我司仪器数/总仪器数 【数字展示，CRP: 20/80、】
def ProjectMachine(data):
    projectmachine_df=data.drop_duplicates('id').groupby('project').agg({'ownmachinenumber':sum,'totalmachinenumber':sum}).reset_index()
    return projectmachine_df


#竞品关系点：竞品关系点 【饼状图】
def CompetitionRelationCompare(data):
    competitionrelationtotal_df=data[data['machinenumber']!= 0].groupby('competitionrelation')['machinenumber'].sum().to_frame().reset_index()
    competitionrelationwithseries_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull())].groupby('competitionrelation')['machinenumber'].count().to_frame().reset_index()
    competitionrelationwithseriesunique_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull())].drop_duplicates('machineseries').groupby('competitionrelation')['machinenumber'].count().to_frame().reset_index()
    competitionrelationrank_df=pd.merge(competitionrelationtotal_df,competitionrelationwithseries_df,on='competitionrelation',how='outer')
    competitionrelationrank_df=pd.merge(competitionrelationrank_df,competitionrelationwithseriesunique_df,on='competitionrelation',how='outer').fillna(0)
    competitionrelationrank_df['realmachinenumber']=competitionrelationrank_df['machinenumber_x']-competitionrelationrank_df['machinenumber_y']+competitionrelationrank_df['machinenumber']
    competitionrelationrank_df.drop(['machinenumber_x','machinenumber_y','machinenumber'],axis=1,inplace=True)
    competitionrelationrank_df.sort_values(by='realmachinenumber',ascending=False,inplace=True)
    competitionrelationrank_df.reset_index(inplace=True)
    competitionrelationrank_df.drop(['index'],axis=1,inplace=True)
    return competitionrelationrank_df



#我司业务仪器中，（ownbusiness为是，仪器数量不为0），我们直供的占比
def DirectsaleOwnbusiness(data):
    #我司仪器总数
    ownmachine_df=data.drop_duplicates('id')['ownmachinenumber'].sum()
    #我司直供仪器数
    pmrtotal_df=data[(data['ownbusiness']== '是') & (data['machinenumber']!= 0) & (data['endsupplier'].str.contains('普美瑞'))]['machinenumber'].sum()
    #我司直供仪器数含有序列号的仪器
    pmrwithseries_df=data[(data['ownbusiness']== '是') & (data['machinenumber']!= 0) & (data['endsupplier'].str.contains('普美瑞')) & (~data['machineseries'].isnull())]['machinenumber'].count()
    #我司直供仪器数含有序列号的仪器,用序列号去重
    pmrwithseriesunique_df=data[(data['ownbusiness']== '是') & (data['machinenumber']!= 0) & (data['endsupplier'].str.contains('普美瑞')) & (~data['machineseries'].isnull())].drop_duplicates('machineseries')['machinenumber'].count()
    #最终我司直供仪器数
    pmrdirectownmachine=pmrtotal_df-pmrwithseries_df+pmrwithseriesunique_df
    #占比
    if ownmachine_df==0:
        pmrdirectownmachinerate=0
    else:
        pmrdirectownmachinerate=pmrdirectownmachine/ownmachine_df
    return pmrdirectownmachinerate


#品牌仪器数量排名：
def BrandMachineNumber(data):
    brandtotal_df=data[(data['machinenumber']!= 0)].groupby('brand')['machinenumber'].sum().to_frame().reset_index()
    brandwithseries_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull())].groupby('brand')['machinenumber'].count().to_frame().reset_index()
    brandwithseriesunique_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull())].drop_duplicates('machineseries').groupby('brand')['machinenumber'].count().to_frame().reset_index()
    brandrank_df=pd.merge(brandtotal_df,brandwithseries_df,on='brand',how='outer')
    brandrank_df=pd.merge(brandrank_df,brandwithseriesunique_df,on='brand',how='outer').fillna(0)
    brandrank_df['realmachinenumber']=brandrank_df['machinenumber_x']-brandrank_df['machinenumber_y']+brandrank_df['machinenumber']
    brandrank_df.drop(['machinenumber_x','machinenumber_y','machinenumber'],axis=1,inplace=True)
    brandrank_df.sort_values(by='realmachinenumber',ascending=False,inplace=True)
    brandrank_df.reset_index(inplace=True)
    brandrank_df.drop(['index'],axis=1,inplace=True)
    brandrank_dfsum=brandrank_df['realmachinenumber'].sum()
    if brandrank_dfsum==0:
        brandrank_df['%']=0
    else:
        brandrank_df['%']=(brandrank_df['realmachinenumber']/brandrank_dfsum)
    brandrank_df=brandrank_df.reset_index()
    brandrank_df['index']=brandrank_df['index']+1
    brandrank_df.rename(columns={'index':'rank'},inplace=True)
    return brandrank_df


#常规维护的仪器数量： 装机时间5年内，本公司的业务
def NormalMaintainMachineNumber(data):
    normalmaintainance_machinenumber_total_df=data[(data['machinenumber']!= 0) & (data['ownbusiness']== '是') &  (data['expiration']== '5年内')]['machinenumber'].sum()
    normalmaintainance_machinenumber_series_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull()) & (data['ownbusiness']== '是') &  (data['expiration']== '5年内')]['machinenumber'].count()
    normalmaintainance_machinenumber_seriesunique_df=data[ (data['machinenumber']!= 0) & (~data['machineseries'].isnull()) & (data['ownbusiness']== '是') &  (data['expiration']== '5年内')].drop_duplicates('machineseries')['machinenumber'].count()
    normalmaintainance_machinenumber_df=normalmaintainance_machinenumber_total_df-normalmaintainance_machinenumber_series_df+normalmaintainance_machinenumber_seriesunique_df
    return normalmaintainance_machinenumber_df


#重点跟进维护的仪器数量：装机时间5年外, 本公司业务
def MainMaintainMachineNumber(data):
    mainmaintainance_machinenumber_total_df=data[(data['machinenumber']!= 0) & (data['ownbusiness']== '是') &  (data['expiration']== '已超5年')]['machinenumber'].sum()
    mainmaintainance_machinenumber_series_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull()) & (data['ownbusiness']== '是') &  (data['expiration']== '已超5年')]['machinenumber'].count()
    mainmaintainance_machinenumber_seriesunique_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull()) & (data['ownbusiness']== '是') &  (data['expiration']== '已超5年')].drop_duplicates('machineseries')['machinenumber'].count()
    mainmaintainance_machinenumber_df=mainmaintainance_machinenumber_total_df-mainmaintainance_machinenumber_series_df+mainmaintainance_machinenumber_seriesunique_df
    return mainmaintainance_machinenumber_df


#需要关注的仪器数量: 装机时间5年内，非公司业务
def ConcernMachineNumber(data):
    concern_machinenumber_total_df=data[(data['machinenumber']!= 0) & (data['ownbusiness']== '否') &  (data['expiration']== '5年内')]['machinenumber'].sum()
    concern_machinenumber_series_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull()) & (data['ownbusiness']== '否') &  (data['expiration']== '5年内')]['machinenumber'].count()
    concern_machinenumber_seriesunique_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull()) & (data['ownbusiness']== '否') &  (data['expiration']== '5年内')].drop_duplicates('machineseries')['machinenumber'].count()
    concern_machinenumber_df=concern_machinenumber_total_df-concern_machinenumber_series_df+concern_machinenumber_seriesunique_df
    return concern_machinenumber_df


#> 重点开拓的仪器数量: 装机时间5年外，非公司业务
def MainDevelopMachineNumber(data):
    maindevelop_machinenumber_total_df=data[(data['machinenumber']!= 0) & (data['ownbusiness']== '否') &  (data['expiration']== '已超5年')]['machinenumber'].sum()
    maindevelop_machinenumber_series_df=data[ (data['machinenumber']!= 0) & (~data['machineseries'].isnull()) & (data['ownbusiness']== '否') &  (data['expiration']== '已超5年')]['machinenumber'].count()
    maindevelop_machinenumber_seriesunique_df=data[ (data['machinenumber']!= 0) & (~data['machineseries'].isnull()) & (data['ownbusiness']== '否') &  (data['expiration']== '已超5年')].drop_duplicates('machineseries')['machinenumber'].count()
    maindevelop_machinenumber=maindevelop_machinenumber_total_df-maindevelop_machinenumber_series_df+maindevelop_machinenumber_seriesunique_df
    return maindevelop_machinenumber



#> 装机时间未知的仪器数量: 不含装机时间
def NoInstalldateMachineNumber(data):
    noinstalldate_machinenumber_total_df=data[(data['machinenumber']!= 0) & (data['expiration']== '--')]['machinenumber'].sum()
    noinstalldate_machinenumber_series_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull()) &  (data['expiration']== '--')]['machinenumber'].count()
    noinstalldate_machinenumber_seriesunique_df=data[(data['machinenumber']!= 0) & (~data['machineseries'].isnull()) &  (data['expiration']== '--')].drop_duplicates('machineseries')['machinenumber'].count()
    noinstalldate_machinenumber=noinstalldate_machinenumber_total_df-noinstalldate_machinenumber_series_df+noinstalldate_machinenumber_seriesunique_df
    return noinstalldate_machinenumber




def RunWholeCompany(data):
    result={}
    result['data']={}    
    
    #普美瑞直销业务重点项目数量   
    result['data']['ProjectCount']=ProjectCount(data)
    
    #覆盖医院数量
    result['data']['HospitalCount']=HospitalCount(data)
    
    #已有我司仪器的医院数量 不分项目
    result['data']['HospitalnameWithOwnmachineCount']=HospitalnameWithOwnmachineCount(data)
    
    #今年已开票医院数量(初始值是0)
    result['data']['HospitalnameWithValueCount']=HospitalnameWithValueCount(data)
    
    #总测试数，
    result['data']['TestspermonthCount']=TestspermonthCount(data)
    
    #我司的测试数，
    result['data']['OWNtestspermonthCount']=OWNtestspermonthCount(data)
    
    #所有医院截至目前开票总额
    result['data']['SalesValueTotal']=SalesValueTotal(data)
    #所覆盖医院Q1开票总额，
    result['data']['Q1SalesValueTotal']=Q1SalesValueTotal(data)
    #所覆盖医院Q2开票总额，
    result['data']['Q2SalesValueTotal']=Q2SalesValueTotal(data)
    #所覆盖医院Q3开票总额，
    result['data']['Q3SalesValueTotal']=Q3SalesValueTotal(data)
    #所覆盖医院Q4开票总额，
    result['data']['Q4SalesValueTotal']=Q4SalesValueTotal(data)
    #市场总仪器数
    result['data']['TotalMachineNumberCount']=TotalMachineNumberCount(data)

    #我司仪器数
    result['data']['OWNNumberCount']=OWNNumberCount(data)

    #各地区分配的医院数量
    result['data']['HospitalnameDistrictCount']=[] 
    for i in HospitalnameDistrictCount(data).index.tolist():
        element = {}
        element['id'] = i
        element['district'] = HospitalnameDistrictCount(data).iloc[i,0]
        element['hospitalname'] =  HospitalnameDistrictCount(data).iloc[i,1]   
        result['data']['HospitalnameDistrictCount'].append(element)
        
    #各销售分配的医院数量
    result['data']['SalesmanHospitalCount']=[] 
    for i in SalesmanHospitalCount(data).index.tolist():
        element = {}
        element['id'] = i
        element['salesman1'] = SalesmanHospitalCount(data).iloc[i,0]
        element['hospitalname'] =  SalesmanHospitalCount(data).iloc[i,1]   
        result['data']['SalesmanHospitalCount'].append(element) 
        
    #各销售有效填报的医院项目率 有效填报了仪器，品牌不为空 数量不为0
    result['data']['SalesmanFillEffectiveness']=[] 
    for i in SalesmanFillEffectiveness(data).index.tolist():
        element = {}
        element['id'] = i
        element['salesman1'] = SalesmanFillEffectiveness(data).iloc[i,0]
        element['effectivefill'] =  SalesmanFillEffectiveness(data).iloc[i,1]   
        element['needtofill'] = SalesmanFillEffectiveness(data).iloc[i,2]
        element['effectiveness'] =  SalesmanFillEffectiveness(data).iloc[i,3] 
        result['data']['SalesmanFillEffectiveness'].append(element) 
    
    
    #医院今年截至今日，开票额总排行  ，具体要有医院名称、金额和销售名称
    result['data']['HospitalSalesRank']=[] 
    for i in HospitalSalesRank(data).index.tolist()[0:50]:
        element = {}
        element['id'] = i
        element['rank'] = HospitalSalesRank(data).iloc[i,0]
        element['hospitalname'] = HospitalSalesRank(data).iloc[i,1]
        element['salesman1'] =  HospitalSalesRank(data).iloc[i,2]   
        element['q1actualsales'] =  HospitalSalesRank(data).iloc[i,3] 
        element['q2actualsales'] =  HospitalSalesRank(data).iloc[i,4] 
        element['q3actualsales'] =  HospitalSalesRank(data).iloc[i,5] 
        element['q4actualsales'] =  HospitalSalesRank(data).iloc[i,6] 
        element['thisyear_totalactualsales'] =  HospitalSalesRank(data).iloc[i,7] 
        element['%'] =  HospitalSalesRank(data).iloc[i,8] 
        result['data']['HospitalSalesRank'].append(element)
    
    
#     #各人员的目标完成情况【进度条】    
#     result['data']['SalesmanComplete']=[] 
#     for i in SalesmanComplete(data).index.tolist():
#         element = {}
#         element['id'] = i
#         element['salesman1'] = SalesmanComplete(data).iloc[i,0]
#         element['q1target'] =  SalesmanComplete(data).iloc[i,1]   
#         element['q1actualsales'] =  SalesmanComplete(data).iloc[i,2] 
#         element['q1finishrate'] =  SalesmanComplete(data).iloc[i,3] 
#         element['q2target'] =  SalesmanComplete(data).iloc[i,4] 
#         element['q2actualsales'] =  SalesmanComplete(data).iloc[i,5] 
#         element['q2finishrate'] =  SalesmanComplete(data).iloc[i,6] 
#         element['q3target'] =  SalesmanComplete(data).iloc[i,7] 
#         element['q3actualsales'] =  SalesmanComplete(data).iloc[i,8] 
#         element['q3finishrate'] =  SalesmanComplete(data).iloc[i,9] 
#         element['q4target'] =  SalesmanComplete(data).iloc[i,10] 
#         element['q4actualsales'] =  SalesmanComplete(data).iloc[i,11] 
#         element['q4finishrate'] =  SalesmanComplete(data).iloc[i,12] 
#         element['totaltarget'] =  SalesmanComplete(data).iloc[i,13]  
#         element['totalactualsales'] =  SalesmanComplete(data).iloc[i,14]  

#         result['data']['SalesmanComplete'].append(element)
    
    #各人员 有目标的数据的完成情况
    result['data']['SalesmanCompleteWithTarget']=[] 
    for i in SalesmanCompleteWithTarget(data).index.tolist():
        element = {}
        element['id'] = i
        element['salesman1'] = SalesmanCompleteWithTarget(data).iloc[i,0]
        element['q1target'] =  SalesmanCompleteWithTarget(data).iloc[i,1]   
        element['q1actualsales'] =  SalesmanCompleteWithTarget(data).iloc[i,2] 
        element['q1finishrate'] =  SalesmanCompleteWithTarget(data).iloc[i,3] 
        element['q2target'] =  SalesmanCompleteWithTarget(data).iloc[i,4] 
        element['q2actualsales'] =  SalesmanCompleteWithTarget(data).iloc[i,5] 
        element['q2finishrate'] =  SalesmanCompleteWithTarget(data).iloc[i,6] 
        element['q3target'] =  SalesmanCompleteWithTarget(data).iloc[i,7] 
        element['q3actualsales'] =  SalesmanCompleteWithTarget(data).iloc[i,8] 
        element['q3finishrate'] =  SalesmanCompleteWithTarget(data).iloc[i,9] 
        element['q4target'] =  SalesmanCompleteWithTarget(data).iloc[i,10] 
        element['q4actualsales'] =  SalesmanCompleteWithTarget(data).iloc[i,11] 
        element['q4finishrate'] =  SalesmanCompleteWithTarget(data).iloc[i,12] 
        element['totaltarget'] =  SalesmanCompleteWithTarget(data).iloc[i,13] 
        element['totalactualsales'] =  SalesmanCompleteWithTarget(data).iloc[i,14] 
        element['totalfinishrate'] =  SalesmanCompleteWithTarget(data).iloc[i,15] 
        result['data']['SalesmanCompleteWithTarget'].append(element)
    

    #q1 各人员 有目标的数据的完成情况
    result['data']['q1SalesmanCompleteWithTarget']=[] 
    for i in q1SalesmanCompleteWithTarget(data).index.tolist():
        element = {}
        element['id'] = i
        element['salesman1'] = q1SalesmanCompleteWithTarget(data).iloc[i,0]
        element['q1target'] =  q1SalesmanCompleteWithTarget(data).iloc[i,1]   
        element['q1actualsales'] =  q1SalesmanCompleteWithTarget(data).iloc[i,2] 
        element['q1finishrate'] =  q1SalesmanCompleteWithTarget(data).iloc[i,3] 
        result['data']['q1SalesmanCompleteWithTarget'].append(element)  
    
    #q2 各人员 有目标的数据的完成情况
    result['data']['q2SalesmanCompleteWithTarget']=[] 
    for i in q2SalesmanCompleteWithTarget(data).index.tolist():
        element = {}
        element['id'] = i
        element['salesman1'] = q2SalesmanCompleteWithTarget(data).iloc[i,0]
        element['q2target'] =  q2SalesmanCompleteWithTarget(data).iloc[i,1]   
        element['q2actualsales'] =  q2SalesmanCompleteWithTarget(data).iloc[i,2] 
        element['q2finishrate'] =  q2SalesmanCompleteWithTarget(data).iloc[i,3] 
        result['data']['q2SalesmanCompleteWithTarget'].append(element)    
        
    #q3 各人员 有目标的数据的完成情况
    result['data']['q3SalesmanCompleteWithTarget']=[] 
    for i in q3SalesmanCompleteWithTarget(data).index.tolist():
        element = {}
        element['id'] = i
        element['salesman1'] = q3SalesmanCompleteWithTarget(data).iloc[i,0]
        element['q3target'] =  q3SalesmanCompleteWithTarget(data).iloc[i,1]   
        element['q3actualsales'] =  q3SalesmanCompleteWithTarget(data).iloc[i,2] 
        element['q3finishrate'] =  q3SalesmanCompleteWithTarget(data).iloc[i,3] 
        result['data']['q3SalesmanCompleteWithTarget'].append(element)
        
    #q4 各人员 有目标的数据的完成情况
    result['data']['q4SalesmanCompleteWithTarget']=[] 
    for i in q4SalesmanCompleteWithTarget(data).index.tolist():
        element = {}
        element['id'] = i
        element['salesman1'] = q4SalesmanCompleteWithTarget(data).iloc[i,0]
        element['q4target'] =  q4SalesmanCompleteWithTarget(data).iloc[i,1]   
        element['q4actualsales'] =  q4SalesmanCompleteWithTarget(data).iloc[i,2] 
        element['q4finishrate'] =  q4SalesmanCompleteWithTarget(data).iloc[i,3] 
        result['data']['q4SalesmanCompleteWithTarget'].append(element)

   # q2 总体目标额
    result['data']['Q2targettotal']=Q2targettotal(data)
    #q2 含目标额的实际开票额
    result['data']['Q2actualtotal']=Q2actualtotal(data)
    
    #q3 总体目标额
    result['data']['Q3targettotal']=Q3targettotal(data)
    #q3 含目标额的实际开票额
    result['data']['Q3actualtotal']=Q3actualtotal(data)
    
    #q4 总体目标额
    result['data']['Q4targettotal']=Q4targettotal(data)
    #q4 含目标额的实际开票额
    result['data']['Q4actualtotal']=Q4actualtotal(data)

    #各项目的我司仪器数/总仪器数 【数字展示，CRP: 20/80、】
    result['data']['ProjectMachine']=[] 
    for i in ProjectMachine(data).index.tolist()[0:10]:
        element = {}
        element['id'] = i
        element['project'] = ProjectMachine(data).iloc[i,0]
        element['ownmachinenumber'] =  ProjectMachine(data).iloc[i,1]   
        element['totalmachinenumber'] =  ProjectMachine(data).iloc[i,2] 
        result['data']['ProjectMachine'].append(element)
    
    
    #竞品关系点：竞品关系点 【饼状图】
    result['data']['CompetitionRelationCompare']=[] 
    for i in CompetitionRelationCompare(data).index.tolist():
        element = {}
        element['id'] = i
        element['competitionrelation'] = CompetitionRelationCompare(data).iloc[i,0]
        element['realmachinenumber'] =  CompetitionRelationCompare(data).iloc[i,1]   
        result['data']['CompetitionRelationCompare'].append(element)
    
    #我司业务仪器中，（ownbusiness为是，仪器数量不为0），我们直供的占比
    result['data']['DirectsaleOwnbusiness']=DirectsaleOwnbusiness(data)
    
    #品牌仪器数量排名： 六大项目各自的品牌仪器数量排行 【排行榜】
    result['data']['BrandMachineNumber']=[]    
    for i in BrandMachineNumber(data).index.tolist():
        element = {}
        element['id'] = i
        element['rank'] = BrandMachineNumber(data).iloc[i,0]
        element['brand'] = BrandMachineNumber(data).iloc[i,1]
        element['realmachinenumber'] =  BrandMachineNumber(data).iloc[i,2]  
        element['%'] =  BrandMachineNumber(data).iloc[i,3]  
        result['data']['BrandMachineNumber'].append(element)
    
    #常规维护的仪器数量： 装机时间5年内，本公司的业务
    result['data']['NormalMaintainMachineNumber']=NormalMaintainMachineNumber(data)
    #重点跟进维护的仪器数量：装机时间5年外, 本公司业务
    result['data']['MainMaintainMachineNumber']=MainMaintainMachineNumber(data)
    #需要关注的仪器数量: 装机时间5年内，非公司业务
    result['data']['ConcernMachineNumber']=ConcernMachineNumber(data)
    #> 重点开拓的仪器数量: 装机时间5年外，非公司业务
    result['data']['MainDevelopMachineNumber']=MainDevelopMachineNumber(data)

    #> 装机时间未知的仪器数量: 不含装机时间
    result['data']['NoInstalldateMachineNumber']=NoInstalldateMachineNumber(data)   
        
    return result

#+++++++++++++++++++各个项目下++++++++++++++++++++++++++
