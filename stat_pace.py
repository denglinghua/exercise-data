# encoding:utf-8

from datetime import timedelta
import time

import pandas as pd

from chart_data import to_chart, month_pace_detail
import charts
from stat_utils import print_df, top_n, sort_data_by_id_list

def regular_pace_run(df:pd.DataFrame):
    slowest_pace = timedelta(minutes=10)
    data = df.query('pace <= @slowest_pace and run_type == "室外跑步"')

    return data

def __avg_pace(row):
    total_time_secs = row['time'].total_seconds()
    total_distance = row['distance']
    avg_pace = int(total_time_secs / total_distance)

    return avg_pace

@to_chart('跑得快的', '平均配速 = 总时间 / 总距离，不包含越野', charts.to_ms_formatter,
    value_func_params= ('avg_pace', None))
def pace(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data[['id', 'time', 'distance']]
    data = data.groupby("id").agg({'time':'sum','distance':'sum'})
    data = data.reset_index()  
    data = data.query('distance > 1000')
    # Debug mode, the amount of data is small
    # and there may be empty dataframe causes exception
    if data.empty:
        return data

    data['avg_pace'] = data.apply(__avg_pace, axis=1)
    data = data.nsmallest(10, 'avg_pace', 'all')
    data = data.sort_values('avg_pace', ascending=False)

    return data

@to_chart('步子迈得快的', '平均步频', '{c} 步/分',
    value_func_params= ('cadence', lambda x : int(x)))
def cadence(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data.query('cadence > 0 and cadence < 250')
    data = data[['id', 'cadence', 'distance']]
    data = data.groupby('id').agg({'cadence':'mean','distance':'sum'})
    data = data.reset_index()
    data = data.query('distance > 1000')
    data = top_n(data, 'cadence', 10)

    return data

@to_chart('步子跨得大的', '平均步幅', '{c} 米',
    value_func_params= ('stride', lambda x : round(x, 2)))
def stride(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data.query('stride > 0 and stride < 1.8')
    data = data[['id', 'stride', 'distance']]
    data = data.groupby('id').agg({'stride':'mean','distance':'sum'})
    data = data.reset_index()  
    data = data.query('distance > 1000')
    data = top_n(data, 'stride', 10)

    return data

def __month_pace_sum(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data[['id', 'month', 'time', 'distance']]
    data = data.groupby(['id', 'month']).agg({'time':'sum','distance':'sum'})
    data = data.reset_index() 
    data['avg_pace'] = data.apply(__avg_pace, axis=1)

    return data

def __filter_month_pace_sum(sum_data:pd.DataFrame):
    filter_df = sum_data[['id', 'month']]
    filter_df = filter_df.groupby('id').agg({'month':'nunique'})
    filter_df = filter_df.reset_index()
    filter_df = filter_df.query('month >= 24') #24 months is data sample threshold
    id_list = filter_df['id'].to_list()

    data = sum_data.query('id == @id_list')

    return data

def __month_pace_std(sum_df:pd.DataFrame):
    data = __filter_month_pace_sum(sum_df)
    data = data.groupby('id').agg({'avg_pace':['std', 'mean']})
    data = data.reset_index()
    data.columns = ['id', 'pace_std', 'pace_mean']
    data['avg_pace'] = data.apply(lambda x : x['pace_std'] / x['pace_mean'], axis=1)
    data = data.nsmallest(10, 'avg_pace', 'all')
    data = data.sort_values('avg_pace', ascending=False)
        
    return data

@to_chart('平稳跑者——配速', '配速波动 = 月均配速标准差 / 平均月配速', '{c} %',
    value_func_params= ('avg_pace', lambda x : round(x * 100, 2)))
def month_pace_std(df:pd.DataFrame):  
    data = __month_pace_sum(df)
    return __month_pace_std(data)

@to_chart('平稳跑者——配速', '', charts.to_ms_formatter, 'line',
    values_func = month_pace_detail, chart_props={'height':'400px', 'y_min':240, 'inverse':False})
def month_pace_even_detail(df:pd.DataFrame):
    data = __month_pace_sum(df)
    top_id_list = __month_pace_std(data)['id'].to_list()
    data = data.query('id == @top_id_list')
    data = sort_data_by_id_list(data, top_id_list)
    
    return data

def _agg_pace_by_year(df:pd.DataFrame, start_year, end_year):
    years = list(range(start_year, end_year + 1))
    paces = []
    data = df[['year', 'time', 'distance']]
    data['time'] = data['time'].dt.total_seconds()
    data = data.groupby('year').agg(['sum'])
    data.reset_index()
    if len(years) == len(data.index):
        for y in years:
            paces.append(int(data.loc[y, 'time'] / data.loc[y, 'distance']))
    else:
        # once one year data missed, the row will be dropped
        paces = map(lambda x : 0, years)
    
    values = paces
    cols = years
    
    return pd.Series(values, index=cols)

def _pace_diff(row, start_year, end_year):
    for y in range(start_year, end_year + 1):
        # no run in this year
        if row[y] < 1:
            return 0
    
    total_diff = 0
    for y in range(start_year, end_year):
        # every year pace goes up
        year_diff = row[y] - row[y + 1]
        if year_diff <= 0:
            return -1
        else:
            total_diff = total_diff + year_diff
    
    return total_diff

def __distance_id_list(df:pd.DataFrame):
    data = df[['id', 'distance']]
    data = data.groupby('id').agg({'distance':'sum'})
    data = data.reset_index()
    data = data.query('distance > 1000')
    
    return data['id'].to_list()

def __pace_progress(df:pd.DataFrame):
    data = regular_pace_run(df)
    dis_id_list = __distance_id_list(data)
    data = data[['id', 'year', 'time', 'distance']].query('id==@dis_id_list')
    start = data['year'].min()
    end = data['year'].max()
    #start = data.loc[0,'year'] # first line
    #end = data.loc[len(data.index), 'year'] # last line
    data = data.groupby('id').apply(_agg_pace_by_year, start, end)
    data = data.reset_index()
    data['pace_diff'] = data.apply(_pace_diff, axis = 1, args = (start, end))
    data = data.query('pace_diff > 0')
    data = top_n(data, 'pace_diff', 10)
    
    return data

@to_chart('越跑越快的', '每年平均配速都有进步，年平均配速增长累计', '{c} 秒',
    value_func_params= ('pace_diff', lambda x : int(x)))
def pace_progress(df:pd.DataFrame):
    return __pace_progress(df)

@to_chart('越跑越快的', '', charts.to_ms_formatter, 'line',
    values_func = month_pace_detail, chart_props={'height':'600px', 'y_min':240, 'inverse':True})
def month_pace_progress_detail(df:pd.DataFrame):
    data = __month_pace_sum(df)

    top_id_list = __pace_progress(df)['id'].to_list()
    data = data.query('id == @top_id_list')
    data = sort_data_by_id_list(data, top_id_list)
    
    return data