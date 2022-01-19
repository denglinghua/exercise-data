import sys

import pandas as pd
import pyecharts

import datasource
import stat_distance as st_d
import stat_pace as  st_p
import stat_time as st_t
import stat_individual as st_i
import charts

print('\nstart...')
print('python version :' + sys.version)
print('pandas version :' + pd.__version__)
print('pyecharts version :' + pyecharts.__version__)

# usage : python go.py data_path [op=report] [id=0]
op = 'report'
id = 0
data_path = sys.argv[1]

if (len(sys.argv) > 2):
    op = sys.argv[2]

if op == 'calendar' :
    id = int(sys.argv[3])

print('data path :' + data_path)
print('op :' + op)

df = datasource.load_data(data_path)
if op == 'pkl':
    df.to_pickle('data.pkl')

print(df.info())
print(df.describe())

datasource.init_user_id_name_map(df)

if op == 'report':
    st_d.marathon(df)
    st_d.half_marathon(df)
    st_d.distance(df)
    st_d.month_distance_std(df)
    st_d.month_distance_detail(df)

    st_p.pace(df)
    st_p.month_pace_std(df)
    st_p.month_pace_even_detail(df)
    st_p.pace_progress(df)
    st_p.month_pace_progress_detail(df)
    st_p.cadence(df)
    st_p.stride(df)

    st_t.time(df)
    st_t.days(df)
    st_t.every_week(df)
    st_t.morning_run(df)
    st_t.night_run(df)

if (op == 'calendar'):
    st_i.calendar_distance(df, id)

charts.draw_charts()


