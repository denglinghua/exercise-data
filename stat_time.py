# encoding:utf-8

import pandas as pd

from chart_data import to_chart
import charts
from stat_utils import top_n

@to_chart('坚持得最好的', '没有哪一周不跑步的', '', 'word_cloud',
    value_func_params= ('distance', lambda x : int(x)), chart_props={'height':'720px'})
def every_week(df:pd.DataFrame):
    data = df[['joy_run_id', 'week_no', 'distance']]
    data = data.groupby("joy_run_id").agg({'week_no':'nunique','distance':'sum'})
    data = data.reset_index()
    data = top_n(data, 'week_no', 1)
        
    return data

@to_chart('勤奋跑者 - 频率高', '有跑过步的天数', '{c} 天',
    value_func_params= ('days', lambda x : int(x)))
def days(df:pd.DataFrame):
    data = df[['joy_run_id', 'end_time']]
    data['end_date'] = data['end_time'].map(lambda x : x.date())
    data = data[['joy_run_id', 'end_date']]
    data = data.groupby("joy_run_id")['end_date'].nunique()
    data = data.reset_index(name='days')
    data = top_n(data, 'days', 10)

    return data

@to_chart('勤奋跑者 - 时间长', '3年累计跑步时长', charts.to_hms_formatter,
    value_func_params= ('time', lambda x : x.total_seconds()))
def time(df:pd.DataFrame):
    data = df[['joy_run_id', 'time']]
    #data = data.groupby("joy_run_id").sum('time')
    # timedelta can't be summed in this way 'sum()'
    data = data.groupby('joy_run_id').agg({'time': 'sum'})
    data = data.reset_index()
    data = top_n(data, 'time', 10)
    
    return data

@to_chart('晨跑达人', '6:30之前开始跑，字越大，次数越多', '', 'word_cloud',
    value_func_params= ('time', None), chart_props={'height':'600px'})
def morning_run(df:pd.DataFrame):
    the_time = pd.to_datetime(['06:30:00'])[0].time()
    data = df[['joy_run_id', 'end_time', 'time']]
    data['start_date'] = df['end_time'] - df['time']
    data = data[data.start_date.dt.time <= the_time]
    data = data.groupby('joy_run_id').count()
    data = data.reset_index()
    data = top_n(data, 'time', 50)

    return data

@to_chart('夜跑达人', '21:00之后开始跑，字越大，次数越多', '', 'word_cloud',
    value_func_params= ('time', None))
def night_run(df:pd.DataFrame):
    data = df[['joy_run_id', 'end_time', 'time']]
    data['start_date'] = df['end_time'] - df['time']
    data = data[data.start_date.dt.hour > 21]
    data = data.groupby('joy_run_id').count()
    data = data.reset_index()
    data = top_n(data, 'time', 50)

    return data