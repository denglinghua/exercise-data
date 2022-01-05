# encoding:utf-8

from datetime import timedelta

import pandas as pd

from chart_data import to_chart, name_value_pair_data, month_pace_detail, month_distance_detail
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


@to_chart('全程马拉松', '>42公里的记录数量，统计范围2019-01-01～2021-12-31', '{c} 次',
    value_func_params= ('distance', None))
def marathon(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']].query('distance > 42')
    data = data.groupby("joy_run_id").count()
    data = data.reset_index()
    data = __top_n(data, 'distance', 10)

    return data

@to_chart('半马王子', '>21公里的记录数量，统计范围2019-01-01～2021-12-31', '{c} 次',
    value_func_params= ('distance', None))
def half_marathon(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']].query('distance > 21')
    data = data.groupby("joy_run_id").count()
    data = data.reset_index()
    data = __top_n(data, 'distance', 10)
        
    return data

@to_chart('跑得远的', '3年累计跑量', '{c} 公里',
    value_func_params= ('distance', lambda x : int(x)))
def distance(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']]
    data = data.groupby("joy_run_id").sum('distance')
    data = data.reset_index()
    data = __top_n(data, 'distance', 10)
    
    return data

@to_chart('坚持得最好的', '没有哪一周不跑步的', '', 'word_cloud',
    value_func_params= ('distance', lambda x : int(x)), chart_props={'height':'720px'})
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

@to_chart('跑得快的', '平均配速 = 总时间 / 总距离，不包含越野', charts.to_ms_formatter,
    value_func_params= ('avg_pace', lambda x : x.total_seconds()))
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

@to_chart('勤奋跑者 - 时间长', '3年累计跑步时长', charts.to_hms_formatter,
    value_func_params= ('time', lambda x : x.total_seconds()))
def time(df:pd.DataFrame):
    data = df[['joy_run_id', 'time']]
    #data = data.groupby("joy_run_id").sum('time')
    # timedelta can't be summed in this way 'sum()'
    data = data.groupby('joy_run_id').agg({'time': 'sum'})
    data = data.reset_index()
    data = __top_n(data, 'time', 10)
    
    return data

@to_chart('勤奋跑者 - 频率高', '有跑过步的天数', '{c} 天',
    value_func_params= ('days', lambda x : int(x)))
def days(df:pd.DataFrame):
    data = df[['joy_run_id', 'end_time']]
    data['end_date'] = data['end_time'].transform(lambda x : x.date())
    data = data[['joy_run_id', 'end_date']]
    data = data.groupby("joy_run_id")['end_date'].nunique()
    data = data.reset_index(name='days')
    data = __top_n(data, 'days', 10)

    return data

@to_chart('步子迈得快的', '平均步频', '{c} 步/分',
    value_func_params= ('cadence', lambda x : int(x)))
def cadence(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data = data.query('cadence > 0 and cadence < 250')
    data = data[['joy_run_id', 'cadence', 'distance']]
    data = data.groupby('joy_run_id').agg({'cadence':'mean','distance':'sum'})
    data = data.reset_index()  
    data = data.query('distance > 1000')
    data = __top_n(data, 'cadence', 10)

    return data

@to_chart('步子跨得大的', '平均步幅', '{c} 米',
    value_func_params= ('stride_len', lambda x : round(x, 2)))
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
    data = df[['joy_run_id', 'month', 'distance']]
    data = data.groupby(['joy_run_id', 'month'])['distance'].sum()
    data = data.reset_index()

    return data
    
def __month_distance_std(df:pd.DataFrame):
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

@to_chart('月跑量平稳', '跑量波动 = 月跑量标准差 / 月平均跑量', '{c} %',
    value_func_params= ('distance', lambda x : round(x * 100, 2)))
def month_distance_std(df:pd.DataFrame):
    return __month_distance_std(df)

@to_chart('月跑量曲线', '', '{value}', 'line',
    values_func = month_distance_detail,chart_props={'height':'400px'})
def month_distance_detail(df:pd.DataFrame):
    data = __month_distance_std(df)
    top_id_list = data['joy_run_id'].to_list()
    data = __regular_pace_run(df)
    data = __month_distance_sum(data)
    data = data.query('joy_run_id == @top_id_list')
    
    return data

@to_chart('跑量平稳', '跑步距离波动 = 距离标准差 / 平均距离', '{c} %',
    value_func_params= ('distance', lambda x : round(x * 100, 2)))
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

def __month_pace_sum(df:pd.DataFrame):
    data = __regular_pace_run(df)
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
    data = __regular_pace_run(df)
    data = data[['joy_run_id', 'year', 'time', 'distance']]
    start = data['year'].min()
    end = data['year'].max()
    data = data.groupby('joy_run_id').apply(_agg_pace_by_year, start, end)
    data = data.reset_index()
    data = data.query('distance > 1000')
    data['pace_diff'] = data.apply(_pace_diff, axis = 1, args = (start, end))
    data = data.query('pace_diff > 0')
    data = __top_n(data, 'pace_diff', 10)
    
    return data

@to_chart('越跑越快的', '每年平均配速都有进步，年平均配速增长累计', '{c} 秒',
    value_func_params= ('pace_diff', lambda x : int(x)))
def pace_progress(df:pd.DataFrame):
    return __pace_progress(df)

@to_chart('月平均配速提升曲线', '', charts.to_ms_formatter, 'line',
    values_func = month_pace_detail, chart_props={'height':'600px', 'y_min':180, 'inverse':True})
def month_pace_progress_detail(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data = data[['joy_run_id', 'month', 'time', 'distance']]
    data = data.groupby(['joy_run_id', 'month']).agg({'time':'sum','distance':'sum'})
    data = data.reset_index() 
    data['avg_pace'] = data.apply(__avg_pace, axis=1)

    top_id_list = __pace_progress(df)['joy_run_id'].to_list()
    data = data.query('joy_run_id == @top_id_list')
    
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
    data = __top_n(data, 'time', 50)

    return data

@to_chart('夜跑达人', '21:00之后开始跑，字越大，次数越多', '', 'word_cloud',
    value_func_params= ('time', None))
def night_run(df:pd.DataFrame):
    data = df[['joy_run_id', 'end_time', 'time']]
    data['start_date'] = df['end_time'] - df['time']
    data = data[data.start_date.dt.hour > 21]
    data = data.groupby('joy_run_id').count()
    data = data.reset_index()
    data = __top_n(data, 'time', 50)

    return data

