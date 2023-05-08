  # 展示时间
  # 去年12.1-4.30 Q1        3.31  + 下一个月的最后一天
    # 3.1-7.31 Q2        6.30  + 下一个月的最后一天 
    # 6.1-10.31 Q3       9.30  + 下一个月的最后一天
    # 9.1-下一年.1.31 Q4  12.31  + 下一个月的最后一天
from datetime import date,timedelta,datetime
from calendar import monthrange
# print(str(datetime.now().year-1)[-2:])
# print(datetime.now().month)
def calculate_quarter_start_end_day(quarter,thisyear):

    quarter = quarter
    year = thisyear
    first_month_of_quarter = 3 * quarter - 2
    last_month_of_quarter = 3 * quarter
    date_of_first_day_of_quarter = date(year, first_month_of_quarter, 1)
    date_of_last_day_of_quarter = date(year, last_month_of_quarter, monthrange(year, last_month_of_quarter)[1])#取得该月有多少天，及最后一天的日期
    return date_of_first_day_of_quarter,date_of_last_day_of_quarter


def result_of_Quatar_display(advanced_days,delayed_days):
    # 判断今天是否在
    # first_day_season, last_dat_season
    # 定义 Q1_range的时间，Q2的时间,Q3r的时间，Q4的时间 return
    # 


    today = date(2023, 4, 11)
    # today = datetime.now().date()
    this_year =2023#datetime.now().year

    #PMRresearchlist的list显示：
    list_display = ('hospital_district','hospital_hospitalclass','hospital','colored_project','salesman1_chinesename','salesman2_chinesename',                    
                   'testspermonth','owntestspermonth','salesmode','saleschannel','support','progress','detailcalculate_totalmachinenumber','detailcalculate_ownmachinenumberpercent',)
            
    # list_editable = ('saleschannel','support')

    #这是salestarget中的readonly fields
    readonly_fields = ('q1actualsales','q2actualsales','q3actualsales','q4actualsales','q1finishrate','q2finishrate','q3finishrate','q4finishrate')

    Q1_range = (calculate_quarter_start_end_day(1,this_year)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(1,this_year)[1]+timedelta(days=delayed_days))
    Q2_range = (calculate_quarter_start_end_day(2,this_year)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(2,this_year)[1]+timedelta(days=delayed_days))
    Q3_range = (calculate_quarter_start_end_day(3,this_year)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(3,this_year)[1]+timedelta(days=delayed_days))

    Q4_range = (calculate_quarter_start_end_day(4,this_year)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(4,this_year)[1]+timedelta(days=delayed_days))
    Q4_range_last = (calculate_quarter_start_end_day(4,this_year-1)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(4,this_year-1)[1]+timedelta(days=delayed_days))#去年9.2-明年1.30
   
    Q1_range_next = (calculate_quarter_start_end_day(1,this_year+1)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(1,this_year+1)[1]+timedelta(days=delayed_days))#今年12.2- 明年4.30

    if today >= Q4_range_last[0] and today <= Q4_range_last[1]: #闭区间 去年9.2-1.30  看到去年Q4  今年初能看到去年Q4
        if today.month == 1:
            list_display =  list_display + ('salestarget_{}_q4'.format(str(this_year-1)[-2:]),'completemonth_{}_q4'.format(str(this_year-1)[-2:]),'actualsales_{}_q4'.format(str(this_year-1)[-2:]),'finishrate_{}_q4'.format(str(this_year-1)[-2:]))
        else:
            list_display =  list_display + ('salestarget_{}_q4'.format(str(this_year)[-2:]),'completemonth_{}_q4'.format(str(this_year)[-2:]),'actualsales_{}_q4'.format(str(this_year)[-2:]),'finishrate_{}_q4'.format(str(this_year)[-2:]))

    if today >= Q1_range[0] and today <= Q1_range[1]:           #闭区间 去年12.2-4.30  看到Q1    去年末能看到今年Q1
        if today.month == 12:
            list_display =  list_display + ('salestarget_{}_q1'.format(str(this_year+1)[-2:]),'completemonth_{}_q1'.format(str(this_year+1)[-2:]),'actualsales_{}_q1'.format(str(this_year+1)[-2:]),'finishrate_{}_q1'.format(str(this_year+1)[-2:]))
        else:    
            list_display =  list_display + ('salestarget_{}_q1'.format(str(this_year)[-2:]),'completemonth_{}_q1'.format(str(this_year)[-2:]),'actualsales_{}_q1'.format(str(this_year)[-2:]),'finishrate_{}_q1'.format(str(this_year)[-2:]))
   
    if today >= Q2_range[0] and today <= Q2_range[1]:            #闭区间 3.2-7.30  看到Q2
        list_display =  list_display + ('salestarget_{}_q2'.format(str(this_year)[-2:]),'completemonth_{}_q2'.format(str(this_year)[-2:]),'actualsales_{}_q2'.format(str(this_year)[-2:]),'finishrate_{}_q2'.format(str(this_year)[-2:]))
   
    if today >= Q3_range[0] and today <= Q3_range[1]:            #闭区间 6.2-10.30  看到Q3
        list_display =  list_display + ('salestarget_{}_q3'.format(str(this_year)[-2:]),'completemonth_{}_q3'.format(str(this_year)[-2:]),'actualsales_{}_q3'.format(str(this_year)[-2:]),'finishrate_{}_q3'.format(str(this_year)[-2:]))
    
    if today >= Q4_range[0] and today <= Q4_range[1]:             #闭区间 9.2- 明年1.30  看到Q4 明年初能看到今年Q4 
        if today.month == 1:
            list_display =  list_display + ('salestarget_{}_q4'.format(str(this_year-1)[-2:]),'completemonth_{}_q4'.format(str(this_year-1)[-2:]),'actualsales_{}_q4'.format(str(this_year-1)[-2:]),'finishrate_{}_q4'.format(str(this_year-1)[-2:]))
        else:
            list_display =  list_display + ('salestarget_{}_q4'.format(str(this_year)[-2:]),'completemonth_{}_q4'.format(str(this_year)[-2:]),'actualsales_{}_q4'.format(str(this_year)[-2:]),'finishrate_{}_q4'.format(str(this_year)[-2:]))

    if today >= Q1_range_next[0] and today <= Q1_range_next[1]:   #闭区间 12.2- 明年4.30  看到明年Q1  
        if today.month == 12:
            list_display =  list_display + ('salestarget_{}_q1'.format(str(this_year+1)[-2:]),'completemonth_{}_q1'.format(str(this_year+1)[-2:]),'actualsales_{}_q1'.format(str(this_year+1)[-2:]),'finishrate_{}_q1'.format(str(this_year+1)[-2:]))
        else:    
            list_display =  list_display + ('salestarget_{}_q1'.format(str(this_year)[-2:]),'completemonth_{}_q1'.format(str(this_year)[-2:]),'actualsales_{}_q1'.format(str(this_year)[-2:]),'finishrate_{}_q1'.format(str(this_year)[-2:]))
      

#     # display上的可以编辑的时间段， 不可以超出list display的字段   所以要规定开始日期
#     # 去年12.1-4.30 Q1    1.1开始变灰     Q1可填报：上一年的12.1-12.31 
#     # 3.1-7.31 Q2         4.1开始变灰    Q2 可填报：3.1-3.31 
#     # 6.1-10.31 Q3        7.1开始变灰     Q3  可填报：6.1-6.31
#     # 9.1-下一年.1.31 Q4   10.1开始变灰    Q4 可填报：9.1-9.30
#    #                              Q1  可填报 12.1-12.31
   
#     Q1_editable= (calculate_quarter_start_end_day(1,this_year+1)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(1,this_year+1)[0]) #去年12.1-1.1
#     Q2_editable = (calculate_quarter_start_end_day(2,this_year)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(2,this_year)[0]) #3.1-4.1
#     Q3_editable = (calculate_quarter_start_end_day(3,this_year)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(3,this_year)[0]) #6.1-7.1
#     Q4_editable = (calculate_quarter_start_end_day(4,this_year)[0]-timedelta(days=advanced_days),calculate_quarter_start_end_day(4,this_year)[0]) #9.1-10.1
#     if today >= Q1_editable[0] and today < Q1_editable[1]:      # Q1可填报：上一年的12.1-12.31 
#         list_editable = list_editable + ('targetsalesvalue','Q1completemonth',)

#     if today >= Q2_editable[0] and today < Q2_editable[1]:    #Q2 可填报：3.1-3.31 
#         list_editable = list_editable + ('targetsalesvalue2','Q2completemonth',)

#     if today >= Q3_editable[0] and today < Q3_editable[1]:   #Q3  可填报：6.1-6.31
#         list_editable = list_editable + ('targetsalesvalue3','Q3completemonth',)

#     if today >= Q4_editable[0] and today < Q4_editable[1]:   #Q4 可填报：9.1-9.30
#         list_editable = list_editable + ('targetsalesvalue4','Q4completemonth',)

    # field中 只读的时间段 
    # 去年12.1-4.30 Q1    1.1开始变灰     Q1可填报：上一年的12.1-12.31   Q1变灰：1.1-11.30
    # 3.1-7.31 Q2         4.1开始变灰    Q2 可填报：3.1-3.31            Q2变灰：4.1-12.31
    # 6.1-10.31 Q3        7.1开始变灰     Q3  可填报：6.1-6.31          Q3变灰：7.1-12.31
    # 9.1-下一年.1.31 Q4   10.1开始变灰    Q4 可填报：9.1-9.30           Q4变灰：10.1-次年1.31
   #                              Q1  可填报 12.1-12.31
    Q1_readonly_field = (calculate_quarter_start_end_day(1,this_year)[0],calculate_quarter_start_end_day(1,this_year+1)[0]-timedelta(days=advanced_days))  #Q1变灰：1.1-11.30
    Q2_readonly_field = (calculate_quarter_start_end_day(2,this_year)[0],calculate_quarter_start_end_day(1,this_year+1)[0]) #Q2变灰：4.1-12.31
    Q3_readonly_field = (calculate_quarter_start_end_day(3,this_year)[0],calculate_quarter_start_end_day(1,this_year+1)[0]) #Q3变灰：7.1-12.31
    Q4_readonly_field = (calculate_quarter_start_end_day(4,this_year)[0],calculate_quarter_start_end_day(4,this_year)[1]+timedelta(days=delayed_days)) #Q4变灰：10.1-次年1.31

    if today >= Q1_readonly_field[0] and today < Q1_readonly_field[1]: #Q1变灰：1.1-11.30
        readonly_fields = readonly_fields + ('q1target','q1completemonth',)

    if today >= Q2_readonly_field[0] and today < Q2_readonly_field[1]:#Q2变灰：4.1-12.31
        readonly_fields = readonly_fields + ('q2target','q2completemonth',)

    if today >= Q3_readonly_field[0] and today < Q3_readonly_field[1]:#Q3变灰：7.1-12.31
        readonly_fields = readonly_fields + ('q3target','q3completemonth',)

    if today >= Q4_readonly_field[0] and today < Q4_readonly_field[1]: #Q4变灰：10.1-次年1.31
        readonly_fields = readonly_fields + ('q4target','q4completemonth',)



    speicial_case_date = date(2023,5,31)
    if today <= speicial_case_date:
        return ( # list_display
                    ('hospital_district','hospital_hospitalclass','hospital','colored_project','salesman1_chinesename','salesman2_chinesename',                    
                   'testspermonth','owntestspermonth','salesmode','saleschannel','support','progress','detailcalculate_totalmachinenumber','detailcalculate_ownmachinenumberpercent',
                  'actualsales_23_q1',#'finishrate_23_q1',#  'salestarget_23_q1','completemonth_23_q1',
                   'salestarget_23_q2','completemonth_23_q2','actualsales_23_q2','finishrate_23_q2'),
                    #list_editable
                #   ('saleschannel','support','targetsalesvalue','Q1completemonth','targetsalesvalue2','Q2completemonth'),

                    #readonly_fields
                   ('q1target','q1completemonth','q1actualsales','q2actualsales','q3actualsales','q4actualsales','q1finishrate','q2finishrate','q3finishrate','q4finishrate')
                )





    return list_display,readonly_fields

if __name__ == '__main__':
    print(result_of_Quatar_display(30,30))