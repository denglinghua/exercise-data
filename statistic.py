from datetime import timedelta
from functools import wraps

import pandas as pd

from charts import create_chart_data

def __print_df(df, message=''):
    print('\n')
    print(message)
    print(df)
    return df

def __top_n(df, column, n, ascending=True):
    data = df.nlargest(n, column, 'all')
    data = data.sort_values(column, ascending=ascending)
    return data

def to_chart():
    def to_chart_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):            
            df = func(*args, **kwargs)
            func_name = func.__name__
            __print_df(df, func_name)
            create_chart_data(func_name, df)
            return df
        return wrapped_function
    return to_chart_decorator

def test(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']]
    __print_df(data, '2 cols')
    data = data.query('distance > 42')
    __print_df(data, 'query > 42')
    data = data.groupby("joy_run_id").count()
    __print_df(data, 'group and count')
    data = data.reset_index()
    __print_df(data, 'reset index')
    data['rank'] = data['distance'].rank(method='max')
    __print_df(data, 'rank max')
    data = data.sort_values('distance', ascending=False)
    __print_df(data, 'sort')
    data = data.head(10)
    __print_df(data, 'head')

@to_chart()
def marathon(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']].query('distance > 42')
    data = data.groupby("joy_run_id").count()
    data = data.reset_index()
    data = __top_n(data, 'distance', 10)
        
    return data

@to_chart()
def distance(df:pd.DataFrame):
    data = df[['joy_run_id', 'distance']]
    data = data.groupby("joy_run_id").sum('distance')
    data = data.reset_index()
    data = __top_n(data, 'distance', 10)
    
    return data

@to_chart()
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

@to_chart()
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

@to_chart()
def time(df:pd.DataFrame):
    data = df[['joy_run_id', 'time']]
    #data = data.groupby("joy_run_id").sum('time')
    # timedelta can't be summed in this way 'sum()'
    data = data.groupby('joy_run_id').agg({'time': 'sum'})
    data = data.reset_index()
    data = __top_n(data, 'time', 10)
    
    return data

@to_chart()
def days(df:pd.DataFrame):
    data = df[['joy_run_id', 'end_time']]
    data['end_date'] = data['end_time'].transform(lambda x : x.date())
    data = data[['joy_run_id', 'end_date']]
    data = data.groupby("joy_run_id")['end_date'].nunique()
    data = data.reset_index(name='days')
    data = __top_n(data, 'days', 10)

    return data

@to_chart()
def cadence(df:pd.DataFrame):
    data = __regular_pace_run(df)
    data = data.query('cadence > 0 and cadence < 250')
    data = data[['joy_run_id', 'cadence', 'distance']]
    data = data.groupby('joy_run_id').agg({'cadence':'mean','distance':'sum'})
    data = data.reset_index()  
    data = data.query('distance > 1000')
    data = __top_n(data, 'cadence', 10)

    return data

@to_chart()
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
    
@to_chart()
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

@to_chart()
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

@to_chart()
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


@to_chart()
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

