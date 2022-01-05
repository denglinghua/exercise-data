# encoding:utf-8

from datetime import timedelta

import pandas as pd

from chart_data import to_chart, month_pace_detail
import charts
from stat_utils import top_n

def regular_pace_run(df:pd.DataFrame):
    slowest_pace = timedelta(minutes=10)
    data = df.query('pace <= @slowest_pace and run_type == "室外跑步"')

    return data

def __avg_pace(row):
    total_time_secs = row['time'].total_seconds()
    total_distance = row['distance']
    avg_pace = timedelta(seconds = int(total_time_secs / total_distance))

    return avg_pace

@to_chart('跑得快的', '平均配速 = 总时间 / 总距离，不包含越野', charts.to_ms_formatter,
    value_func_params= ('avg_pace', lambda x : x.total_seconds()))
def pace(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data[['joy_run_id', 'time', 'distance']]
    data = data.groupby("joy_run_id").agg({'time':'sum','distance':'sum'})
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
    data = data[['joy_run_id', 'cadence', 'distance']]
    data = data.groupby('joy_run_id').agg({'cadence':'mean','distance':'sum'})
    data = data.reset_index()
    data = data.query('distance > 1000')
    data = top_n(data, 'cadence', 10)

    return data

@to_chart('步子跨得大的', '平均步幅', '{c} 米',
    value_func_params= ('stride_len', lambda x : round(x, 2)))
def stride(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data.query('stride_len > 0 and stride_len < 1.8')
    data = data[['joy_run_id', 'stride_len', 'distance']]
    data = data.groupby('joy_run_id').agg({'stride_len':'mean','distance':'sum'})
    data = data.reset_index()  
    data = data.query('distance > 1000')
    data = top_n(data, 'stride_len', 10)

    return data

def __month_pace_sum(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data[['joy_run_id', 'month', 'time', 'distance']]
    data = data.groupby(['joy_run_id', 'month']).agg({'time':'sum','distance':'sum'})
    data = data.reset_index() 
    data['avg_pace'] = data.apply(__avg_pace, axis=1)

    filter_df = data[['joy_run_id', 'month']]
    filter_df = filter_df.groupby('joy_run_id').agg({'month':'nunique'})
    filter_df = filter_df.reset_index()
    filter_df = filter_df.query('month >= 24') #24 months is data sample threshold
    id_list = filter_df['joy_run_id'].to_list()

    data = data.query('joy_run_id == @id_list')

    return data

def __month_pace_std(df:pd.DataFrame):
    data = __month_pace_sum(df)
    data['pace_secs'] = data['avg_pace'].dt.total_seconds()
    data = data[['joy_run_id', 'pace_secs']]
    # std ddof=0
    data = data.groupby('joy_run_id').agg({'pace_secs':['std', 'mean']})
    data = data.reset_index()
    data.columns = ['joy_run_id', 'pace_std', 'pace_mean']
    data['pace_secs'] = data.apply(lambda x : x['pace_std'] / x['pace_mean'], axis=1)
    data = data.nsmallest(10, 'pace_secs', 'all')
    data = data.sort_values('pace_secs', ascending=False)
        
    return data

@to_chart('配速平稳', '配速波动 = 月均配速标准差 / 平均月配速', '{c} %',
    value_func_params= ('pace_secs', lambda x : round(x * 100, 2)))
def month_pace_std(df:pd.DataFrame):
    return __month_pace_std(df)

@to_chart('月平均配速曲线', '', charts.to_ms_formatter, 'line',
    values_func = month_pace_detail, chart_props={'height':'400px', 'y_min':180, 'inverse':False})
def month_pace_even_detail(df:pd.DataFrame):
    data = __month_pace_sum(df)
    top_id_list = __month_pace_std(df)['joy_run_id'].to_list()
    data = data.query('joy_run_id == @top_id_list')
    
    return data

def _agg_pace_by_year(df:pd.DataFrame, start_year, end_year):
    years = list(range(start_year, end_year + 1))
    paces = []
    for y in years:
        data = df.query('year == @y')
        if data.empty:
            paces.append(0)
        else:
            pace = int(data['time'].sum().total_seconds() / data['distance'].sum())
            paces.append(pace)
    
    values = paces
    values.append(df['distance'].sum())
    
    cols = years
    cols.append('distance')
    
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

def __pace_progress(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data[['joy_run_id', 'year', 'time', 'distance']]
    start = data['year'].min()
    end = data['year'].max()
    #start = data.loc[0,'year'] # first line
    #end = data.loc[len(data.index), 'year'] # last line
    data = data.groupby('joy_run_id').apply(_agg_pace_by_year, start, end)
    data = data.reset_index()
    data = data.query('distance > 1000')
    data['pace_diff'] = data.apply(_pace_diff, axis = 1, args = (start, end))
    data = data.query('pace_diff > 0')
    data = top_n(data, 'pace_diff', 10)
    
    return data

@to_chart('越跑越快的', '每年平均配速都有进步，年平均配速增长累计', '{c} 秒',
    value_func_params= ('pace_diff', lambda x : int(x)))
def pace_progress(df:pd.DataFrame):
    return __pace_progress(df)

@to_chart('月平均配速提升曲线', '', charts.to_ms_formatter, 'line',
    values_func = month_pace_detail, chart_props={'height':'600px', 'y_min':180, 'inverse':True})
def month_pace_progress_detail(df:pd.DataFrame):
    data = regular_pace_run(df)
    data = data[['joy_run_id', 'month', 'time', 'distance']]
    data = data.groupby(['joy_run_id', 'month']).agg({'time':'sum','distance':'sum'})
    data = data.reset_index() 
    data['avg_pace'] = data.apply(__avg_pace, axis=1)

    top_id_list = __pace_progress(df)['joy_run_id'].to_list()
    data = data.query('joy_run_id == @top_id_list')
    
    return data