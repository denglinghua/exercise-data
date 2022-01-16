# encoding:utf-8

import pandas as pd

from chart_data import to_chart, calendar_data

@to_chart('跑步日历', '', '{c} 次', chart_type='calendar', values_func=calendar_data,
    value_func_params= ('end_date', 'distance', None))
def calendar_distance(df:pd.DataFrame, id):
    data = df.query('id==@id')
    data['end_date'] = data['end_time'].map(lambda x : x.date())
    data = data[['end_date', 'distance']]
    data = data.groupby("end_date").sum('distance')
    data = data.reset_index()
    data = data.sort_values('end_date')

    return data

