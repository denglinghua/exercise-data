# encoding:utf-8

import pandas as pd

from chart_data import to_chart, calendar_data
from datasource import user_id_to_name

@to_chart('的跑步日历', '', '{c}', chart_type='calendar', values_func=calendar_data,
    value_func_params= ('end_date', 'distance', None))
def calendar_distance(df:pd.DataFrame, id):
    data = df.query('id==@id')
    begin = data['year'].min()
    end = data['year'].max()
    data['end_date'] = data['end_time'].map(lambda x : x.date())
    data = data[['end_date', 'distance']]
    data = data.groupby("end_date").sum('distance')
    data = data.reset_index()
    data = data.sort_values('end_date')

    props = {
        'runner' : user_id_to_name(id),
        'begin' : begin,
        'end' : end
    }

    return (data, props)

