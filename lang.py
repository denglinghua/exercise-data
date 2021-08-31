# encoding:utf-8
__cur_lang = 0
__lang_dict = {
    # col is short for column
    'col_activity_type':('Activity Type', '活动类型'),
    'col_avg_pace':('Avg Pace', '平均配速'),
    'col_date':('Date', '日期'),
    'col_distance':('Distance', '距离'),
    'col_avg_run_cadence':('Avg Run Cadence', '平均步频'),
    'col_avg_stride_length':('Avg Stride Length', '平均步长'),
    'col_calories':('Calories', '卡路里'),
    'col_time':('Time', '时间'),
    'running':('Running', '跑步'),
    'swimming':('Swimming','游泳'),
    'cycling_keyword':('Cycling','骑行'),
    'cycling':('Cycling','自行车'),
    'hour':('hrs', '小时'),
    'min':('mins', '分'),
    'average_run_pace':('Average Run Pace', '跑多快'),
    'run_pace_unit':('mins/km', '分配'),
    'average_run_cadence':('Average Run Cadence', '步频'),
    'steps_per_min':('steps/min', '步/分'),
    'average_stride_length':('Average Stride Length', '步长'),
    'activity_hours':('Activities by Hour', '那些时辰比较活跃'),
    'activity_h':('H', '时'),
    'activity_weekdays':('Activities by Day of Week', '星期几比较活跃'),
    'days_of_week':(
        ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], 
        ["一","二","三","四","五","六","日"]),
    'activity_months':('Activities by Month', '那些月份比较活跃'),
    'months':(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
        list(map(lambda m : str(m) + "月", range(1, 13)))),
    'running_distance':('Running Distance', '跑多远'),
    'swimming_distance':('Swimming Distance', '游多远'),
    'activities':('Activities', '三项分别做了多少次'),
    'activity_times':('', ''),
    'total_distance':('Total Distance', '三项距离'),
    'km':('km', '公里'),
    'activity_calories':('Activity Calories', '三项热量消耗'),
    'kcal':('C', '千卡'),
    'total_activity_time':('Total Activity Time', '三项耗时'),
}

class Lang(object):
    pass

lang = Lang()

def set_lang(lang_index):
    global __cur_lang
    __cur_lang = lang_index
    for key in __lang_dict:
         setattr(lang, key, __lang_dict[key][__cur_lang])