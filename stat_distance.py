# encoding:utf-8

import pandas as pd

from chart_data import to_chart, month_distance_detail
import charts
from stat_utils import top_n, sort_data_by_id_list
from stat_pace import regular_pace_run

@to_chart('42KM达人', '>42公里的记录数量', '{c} 次',
    value_func_params= ('distance', None))
def marathon(df:pd.DataFrame):
    data = df[['id', 'distance']].query('distance > 42')
    data = data.groupby("id").count()
    data = data.reset_index()
    data = top_n(data, 'distance', 10)

    return data

@to_chart('抬腿就是半马', '>21公里的记录数量', '{c} 次',
    value_func_params= ('distance', None))
def half_marathon(df:pd.DataFrame):
    data = df[['id', 'distance']].query('distance > 21')
    data = data.groupby("id").count()
    data = data.reset_index()
    data = top_n(data, 'distance', 10)
        
    return data

@to_chart('跑得远的', '累计跑量', '{c} 公里',
    value_func_params= ('distance', lambda x : int(x)))
def distance(df:pd.DataFrame):
    data = df[['id', 'distance']]
    data = data.groupby("id").sum('distance')
    data = data.reset_index()
    data = top_n(data, 'distance', 10)
    
    return data

def _month_distance_sum(df:pd.DataFrame):
    data = df[['id', 'month', 'distance']]
    data = data.groupby(['id', 'month'])['distance'].sum()
    data = data.reset_index()

    return data
    
def _month_distance_std(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = _month_distance_sum(data)
    data = data.groupby('id').agg({'month':'count','distance':['std', 'mean']})
    data = data.reset_index()
    data.columns = ['id', 'month', 'distance_std', 'distance_mean']
    data['distance'] = data.apply(lambda x : x['distance_std'] / x['distance_mean'], axis=1)
    data = top_n(data, 'month', 1)
    data = data.nsmallest(10, 'distance', 'all')
    data = data.sort_values('distance', ascending=False)

    return data

@to_chart('平稳跑者——跑量', '跑量波动 = 月跑量标准差 / 月平均跑量', '{c} %',
    value_func_params= ('distance', lambda x : round(x * 100, 2)))
def month_distance_std(df:pd.DataFrame):
    return _month_distance_std(df)

@to_chart('平稳跑者——跑量', '', '{value}', 'line',
    values_func = month_distance_detail,chart_props={'height':'400px'})
def month_distance_detail(df:pd.DataFrame):
    data = _month_distance_std(df)
    top_id_list = data['id'].to_list()
    data = regular_pace_run(df)
    data = _month_distance_sum(data)
    data = data.query('id == @top_id_list')
    data = sort_data_by_id_list(data, top_id_list)
    
    return data

@to_chart('每次跑量平稳', '跑步距离波动 = 距离标准差 / 平均距离', '{c} %',
    value_func_params= ('distance', lambda x : round(x * 100, 2)))
def distance_std(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data.groupby('id').agg({'distance':['sum', 'std', 'mean']})
    data = data.reset_index()
    data.columns = ['id', 'distance_sum', 'distance_std', 'distance_mean']
    data['distance'] = data.apply(lambda x : x['distance_std'] / x['distance_mean'], axis=1)
    data = data.query('distance_sum > 1000')
    data = data.nsmallest(10, 'distance', 'all')
    data = data.sort_values('distance', ascending=False)
        
    return data