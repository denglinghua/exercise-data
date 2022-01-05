# encoding:utf-8

import pandas as pd

from chart_data import to_chart, month_distance_detail
import charts
from stat_utils import top_n
from stat_pace import regular_pace_run

@to_chart('全程马拉松', '>42公里的记录数量，统计范围2019-01-01～2021-12-31', '{c} 次',
    value_func_params= ('distance', None))
def marathon(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']].query('distance > 42')
    data = data.groupby("joy_run_id").count()
    data = data.reset_index()
    data = top_n(data, 'distance', 10)

    return data

@to_chart('半马王子', '>21公里的记录数量，统计范围2019-01-01～2021-12-31', '{c} 次',
    value_func_params= ('distance', None))
def half_marathon(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']].query('distance > 21')
    data = data.groupby("joy_run_id").count()
    data = data.reset_index()
    data = top_n(data, 'distance', 10)
        
    return data

@to_chart('跑得远的', '3年累计跑量', '{c} 公里',
    value_func_params= ('distance', lambda x : int(x)))
def distance(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']]
    data = data.groupby("joy_run_id").sum('distance')
    data = data.reset_index()
    data = top_n(data, 'distance', 10)
    
    return data

def __month_distance_sum(df:pd.DataFrame):
    data = df[['joy_run_id', 'month', 'distance']]
    data = data.groupby(['joy_run_id', 'month'])['distance'].sum()
    data = data.reset_index()

    return data
    
def __month_distance_std(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = __month_distance_sum(data)
    data = data.groupby('joy_run_id').agg({'month':'count','distance':['std', 'mean']})
    data = data.reset_index()
    data.columns = ['joy_run_id', 'month', 'distance_std', 'distance_mean']
    data['distance'] = data.apply(lambda x : x['distance_std'] / x['distance_mean'], axis=1)
    data = top_n(data, 'month', 1)
    data = data.nsmallest(10, 'distance', 'all')
    data = data.sort_values('distance', ascending=False)

    return data

@to_chart('月跑量平稳', '跑量波动 = 月跑量标准差 / 月平均跑量', '{c} %',
    value_func_params= ('distance', lambda x : round(x * 100, 2)))
def month_distance_std(df:pd.DataFrame):
    return __month_distance_std(df)

@to_chart('月跑量曲线', '', '{value}', 'line',
    values_func = month_distance_detail,chart_props={'height':'400px'})
def month_distance_detail(df:pd.DataFrame):
    data = __month_distance_std(df)
    top_id_list = data['joy_run_id'].to_list()
    data = regular_pace_run(df)
    data = __month_distance_sum(data)
    data = data.query('joy_run_id == @top_id_list')
    
    return data

@to_chart('跑量平稳', '跑步距离波动 = 距离标准差 / 平均距离', '{c} %',
    value_func_params= ('distance', lambda x : round(x * 100, 2)))
def distance_std(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data.groupby('joy_run_id').agg({'distance':['sum', 'std', 'mean']})
    data = data.reset_index()
    data.columns = ['joy_run_id', 'distance_sum', 'distance_std', 'distance_mean']
    data['distance'] = data.apply(lambda x : x['distance_std'] / x['distance_mean'], axis=1)
    data = data.query('distance_sum > 1000')
    data = data.nsmallest(10, 'distance', 'all')
    data = data.sort_values('distance', ascending=False)
        
    return data