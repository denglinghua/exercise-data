import time
from functools import wraps

import pandas as pd

from datasource import user_id_to_name

chart_data_list = []

def __print_df(df, message=''):
    print('\n')
    print(message)
    print(df)
    return df

class ChartData(object):
    def __init__(self, title, sub_title, formatter, chart_type, chart_props, xvalues, yvalues):
        self.chart_type = chart_type
        self.title = title
        self.sub_title = sub_title
        self.formatter = formatter
        
        self.xvalues = xvalues
        self.yvalues = yvalues

        for key in chart_props:
            setattr(self, key, chart_props[key])

def create_chart_data(df : pd.DataFrame, title, sub_title, formatter, chart_type, 
                values_func, value_func_params, chart_props):
    values = values_func(df, value_func_params)
    chart_data = ChartData(title, sub_title, formatter, chart_type, chart_props, values[0], values[1])
    chart_data_list.append(chart_data)

def name_value_pair_data(df, params):
    value_column = params[0]
    value_func = params[1]
    xvalues = []
    yvalues = []
    for index, row in df.iterrows():
        xvalues.append(user_id_to_name(row['joy_run_id']))
        # pyecharts doesn't support numpy int64, so call item()
        yvalue = value_func(row[value_column]) if value_func else row[value_column].item()
        yvalues.append(yvalue)
    
    return (xvalues, yvalues)

def to_chart(title:str, sub_title:str, formatter:str, chart_type:str = 'rank_bar',
    values_func:callable = name_value_pair_data, value_func_params : tuple = (),
    chart_props : dict = {}
    ):
    def to_chart_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):   
            tic = time.perf_counter()
            df = func(*args, **kwargs)
            toc = time.perf_counter()
            func_name = func.__name__
            __print_df(df, func_name)
            print(f"\nexec {func_name} time : {toc - tic:0.4f} seconds")
            create_chart_data(df, title, sub_title, formatter, chart_type, 
                values_func, value_func_params, chart_props)
            return df
        return wrapped_function
    return to_chart_decorator

def month_distance_detail(df, params):
    xvalues = []
    yvalues = []
    for g, data in df.groupby('joy_run_id'):
        xs = [m.strftime('%y-%m') for m in data['month'].to_list()]
        
        if (len(xs) > len(xvalues)):
            xvalues = xs
        
        yvalues.append((user_id_to_name(g), data['distance'].to_list()))
    
    return (xvalues, yvalues)

def month_pace_detail(df, params):
    xvalues = []
    yvalues = []
    missed_ys = []
    for g, data in df.groupby('joy_run_id'):
        xs = [m.strftime('%y-%m') for m in data['month'].to_list()]
        
        if (len(xs) > len(xvalues)):
            xvalues = xs
        
        name = user_id_to_name(g)
        ys = {}
        for index, row in data.iterrows():
            ys[row['month'].strftime('%y-%m')] = row['avg_pace'].total_seconds()
        missed_ys.append((name, ys))
        #yvalues.append((user_id_to_name(g), [p.total_seconds() for p in data['avg_pace'].to_list()]))
    
    for my in missed_ys:
        values = my[1]
        # some month value missed
        if len(values) != len(xvalues):
            for xv in xvalues:
                if xv not in values:
                    values[xv] = None
            
    for my in missed_ys:
        name = my[0]
        values = []
        for xv in xvalues:
            values.append(my[1][xv])
        yvalues.append((name, values))
    
    return (xvalues, yvalues)