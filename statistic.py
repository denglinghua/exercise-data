# encoding:utf-8

from datetime import timedelta

import pandas as pd

from chart_data import to_chart, name_value_pair_data
import charts

def __print_df(df, message=''):
    print('\n')
    print(message)
    print(df)
    return df

def __top_n(df, column, n, ascending=True):
    data = df.nlargest(n, column, 'all')
    data = data.sort_values(column, ascending=ascending)
    return data

def test(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance', 'week_no']]
    data = data.query('joy_run_id == 95462930')
    data = data.groupby('week_no').sum('distance')
    __print_df(data, 'qu')


@to_chart(('rank_bar', '全程马拉松', '>42公里的记录数量，统计范围2019-01-01～2021-12-31', '{c} 次'),
    (name_value_pair_data, ('distance', None)))
def marathon(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']].query('distance > 42')
    data = data.groupby("joy_run_id").count()
    data = data.reset_index()
    data = __top_n(data, 'distance', 10)

    return data

@to_chart(('rank_bar', '半马王子', '>21公里的记录数量，统计范围2019-01-01～2021-12-31', '{c} 次'),
    (name_value_pair_data, ('distance', None)))
def half_marathon(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']].query('distance > 21')
    data = data.groupby("joy_run_id").count()
    data = data.reset_index()
    data = __top_n(data, 'distance', 10)
        
    return data

@to_chart(('rank_bar', '跑得远的', '3年累计跑量', '{c} 公里'),
    (name_value_pair_data, ('distance', lambda x : int(x))))
def distance(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']]
    data = data.groupby("joy_run_id").sum('distance')
    data = data.reset_index()
    data = __top_n(data, 'distance', 10)
    
    return data

@to_chart(('word_cloud', '坚持得最好的', '没有哪一周不跑步的', ''),
    (name_value_pair_data, ('distance', lambda x : int(x))))
def every_week(df:pd.DataFrame):
    data = df[['joy_run_id', 'week_no', 'distance']]
    data = data.groupby("joy_run_id").agg({'week_no':'nunique','distance':'sum'})
    data = data.reset_index()
    data = __top_n(data, 'week_no', 1)
        
    return data

def __regular_pace_run(df:pd.DataFrame):
    slowest_pace = timedelta(minutes=10)
    data = df.query('pace <= @slowest_pace and run_type == "室外跑步"')

    #__print_df(data, 'regular run')
    
    return data

def __avg_pace(row):
    total_time_secs = row['time'].total_seconds()
    total_distance = row['distance']
    avg_pace = timedelta(seconds = int(total_time_secs / total_distance))

    return avg_pace

@to_chart(('rank_bar', '跑得快的', '平均配速 = 总时间 / 总距离，不包含越野', charts.to_ms_formatter),
    (name_value_pair_data, ('avg_pace', lambda x : x.total_seconds())))
def pace(df:pd.DataFrame):
    data = __regular_pace_run(df)
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

@to_chart(('rank_bar', '勤奋跑者 - 时间长', '3年累计跑步时长', charts.to_hms_formatter),
    (name_value_pair_data, ('time', lambda x : x.total_seconds())))
def time(df:pd.DataFrame):
    data = df[['joy_run_id', 'time']]
    #data = data.groupby("joy_run_id").sum('time')
    # timedelta can't be summed in this way 'sum()'
    data = data.groupby('joy_run_id').agg({'time': 'sum'})
    data = data.reset_index()
    data = __top_n(data, 'time', 10)
    
    return data

@to_chart(('rank_bar', '勤奋跑者 - 频率高', '有跑过步的天数', '{c} 天'),
    (name_value_pair_data, ('days', lambda x : int(x))))
def days(df:pd.DataFrame):
    data = df[['joy_run_id', 'end_time']]
    data['end_date'] = data['end_time'].transform(lambda x : x.date())
    data = data[['joy_run_id', 'end_date']]
    data = data.groupby("joy_run_id")['end_date'].nunique()
    data = data.reset_index(name='days')
    data = __top_n(data, 'days', 10)

    return data

@to_chart(('rank_bar', '步子迈得快的', '平均步频', '{c} 步/分'),
    (name_value_pair_data, ('cadence', lambda x : int(x))))
def cadence(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data = data.query('cadence > 0 and cadence < 250')
    data = data[['joy_run_id', 'cadence', 'distance']]
    data = data.groupby('joy_run_id').agg({'cadence':'mean','distance':'sum'})
    data = data.reset_index()  
    data = data.query('distance > 1000')
    data = __top_n(data, 'cadence', 10)

    return data

@to_chart(('rank_bar', '步子跨得大的', '平均步幅', '{c} 米'),
    (name_value_pair_data,  ('stride_len', lambda x : round(x, 2))))
def stride(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data = data.query('stride_len > 0 and stride_len < 1.8')
    data = data[['joy_run_id', 'stride_len', 'distance']]
    data = data.groupby('joy_run_id').agg({'stride_len':'mean','distance':'sum'})
    data = data.reset_index()  
    data = data.query('distance > 1000')
    data = __top_n(data, 'stride_len', 10)

    return data

def __month_distance_sum(df:pd.DataFrame):
    data = df[['joy_run_id', 'end_time', 'distance']]
    data['month'] = data['end_time'].dt.to_period('M')
    data = data[['joy_run_id', 'month', 'distance']]  
    data = data.groupby(['joy_run_id', 'month'])['distance'].sum()
    data = data.reset_index()

    return data
    
@to_chart(('rank_bar', '月跑量平稳', '跑量波动 = 月跑量标准差 / 月平均跑量', '{c} %'),
    (name_value_pair_data, ('distance', lambda x : round(x * 100, 2))))
def month_distance_std(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data = __month_distance_sum(data)
    data = data.groupby('joy_run_id').agg({'month':'count','distance':['std', 'mean']})
    data = data.reset_index()
    data.columns = ['joy_run_id', 'month', 'distance_std', 'distance_mean']
    data['distance'] = data.apply(lambda x : x['distance_std'] / x['distance_mean'], axis=1)
    data = __top_n(data, 'month', 1)
    data = data.nsmallest(10, 'distance', 'all')
    data = data.sort_values('distance', ascending=False)

    return data

#@to_chart(('rank_bar', '月跑量变化', '每月跑量', '{c} %'),
#    (name_value_pair_data, ('distance', lambda x : round(x * 100, 2))))
def month_distance_detail(df:pd.DataFrame):
    data = month_distance_std(df)
    top_id_list = data = data['joy_run_id'].to_list()
    data = __regular_pace_run(df)
    data = __month_distance_sum(data)
    data = data.query('joy_run_id == @top_id_list')
    __print_df(data.groupby('joy_run_id'))
    return

@to_chart(('rank_bar', '跑量平稳', '跑步距离波动 = 距离标准差 / 平均距离', '{c} %'),
    (name_value_pair_data, ('distance', lambda x : round(x * 100, 2))))
def distance_std(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data = data.groupby('joy_run_id').agg({'distance':['sum', 'std', 'mean']})
    data = data.reset_index()
    data.columns = ['joy_run_id', 'distance_sum', 'distance_std', 'distance_mean']
    data['distance'] = data.apply(lambda x : x['distance_std'] / x['distance_mean'], axis=1)
    data = data.query('distance_sum > 1000')
    data = data.nsmallest(10, 'distance', 'all')
    data = data.sort_values('distance', ascending=False)
        
    return data

@to_chart(('rank_bar', '配速平稳', '配速波动 = 配速标准差 / 平均配速', '{c} %'),
    (name_value_pair_data, ('pace_secs', lambda x : round(x * 100, 2))))
def pace_std(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data['pace_secs'] = data['pace'].dt.total_seconds()
    # std ddof=0
    data = data.groupby('joy_run_id').agg({'distance':'sum','pace_secs':['std', 'mean']})
    data = data.reset_index()
    data.columns = ['joy_run_id', 'distance', 'pace_std', 'pace_mean']
    data = data.query('distance > 1000')
    data['pace_secs'] = data.apply(lambda x : x['pace_std'] / x['pace_mean'], axis=1)
    data = data.nsmallest(10, 'pace_secs', 'all')
    data = data.sort_values('pace_secs', ascending=False)
        
    return data

def _agg_pace_by_year(df:pd.DataFrame, start_year, end_year):
    years = list(range(start_year, end_year + 1))
    paces = []
    for y in years:
        data = df.query('end_time.dt.year == @y')
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


@to_chart(('rank_bar', '越跑越快的', '每年平均配速都有进步，年平均配速增长累计', '{c} 秒'),
    (name_value_pair_data, ('pace_diff', lambda x : int(x))))
def pace_progress(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data = data[['joy_run_id', 'end_time', 'time', 'distance']]
    start = data['end_time'].min().year
    end = data['end_time'].max().year
    data = data.groupby('joy_run_id').apply(_agg_pace_by_year, start, end)
    data = data.reset_index()
    data = data.query('distance > 1000')
    data['pace_diff'] = data.apply(_pace_diff, axis = 1, args = (start, end))
    data = data.query('pace_diff > 0')
    data = __top_n(data, 'pace_diff', 10)
    
    return data

