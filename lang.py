# encoding:utf-8
_lang_dict = {
    # col is short for column
    'data__activity_type':('Activity Type', '活动类型'),
    'data__avg_pace':('Avg Pace', '平均配速'),
    'data__date':('Date', '日期'),
    'data__distance':('Distance', '距离'),
    'data__avg_run_cadence':('Avg Run Cadence', '平均步频'),
    'data__avg_stride_length':('Avg Stride Length', '平均步长'),
    'data__calories':('Calories', '热量消耗'),
    'data__time':('Time', '时间'),
    'data__keyword_running':('Running', '跑步'),
    'data__keyword_swimming':('Swimming','游泳'),
    'data__keyword_cycling':('Cycling','骑'),
    'running':('Running', '跑步'),
    'swimming':('Swimming','游泳'),
    'cycling':('Cycling','自行车'),
    'hour_short':('h', '小时'),
    'min_short':('m', '分'),
    'min_full':('mins', '分钟'),
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
    'cycling_distance':('Cycling Distance', '骑多远'),
    'activities':('Activities', '三项分别做了多少次'),
    'activity_times':('', ''),
    'total_distance':('Total Distance', '三项距离'),
    'km':('km', '公里'),
    'm':('m', '米'),
    'activity_calories':('Activity Calories', '三项热量消耗'),
    'kcal':('C', '千卡'),
    'total_activity_time':('Total Activity Time', '三项耗时'),
    'activity_time':('Activity Time', '运动多久'),
    'activity_time_calendar':('Activity Time Calendar', '运动时间日历'),
    'calendar_name':('en', 'cn'),
    'rest':('REST', '休息')
}

class Lang(object):
    pass

lang = Lang()

def set_lang(data_lang_index, display_lang_index):
    for key in _lang_dict:
        lang_index = data_lang_index if key.startswith('data__') else display_lang_index
        setattr(lang, key, _lang_dict[key][lang_index])