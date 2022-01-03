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
    def __init__(self, items, xvalues, yvalues):
        self.chart_type = items[0]
        self.title = items[1]
        self.sub_title = items[2]
        self.formatter = items[3]
        
        self.xvalues = xvalues
        self.yvalues = yvalues


def create_chart_data(df : pd.DataFrame, config_items, value_creator):
    val_func = value_creator[0]
    params = value_creator[1]
    values = val_func(df, params)
    chart_data = ChartData(config_items, values[0], values[1])
    chart_data_list.append(chart_data)

def to_chart(chart_config, value_creator):
    def to_chart_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):            
            df = func(*args, **kwargs)
            func_name = func.__name__
            __print_df(df, func_name)
            create_chart_data(df, chart_config, value_creator)
            return df
        return wrapped_function
    return to_chart_decorator

def name_value_pair_data(df, params):
    value_column = params[0]
    value_func = params[1]
    xvalues = []
    yvalues = []
    for index, row in df.iterrows():
        xvalues.append(user_id_to_name(row['joy_run_id']))
        yvalue = value_func(row[value_column]) if value_func else row[value_column].item()
        yvalues.append(yvalue)
    
    return (xvalues, yvalues)

