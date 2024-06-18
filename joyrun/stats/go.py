import sys
import os
import pandas as pd
import pyecharts
import json

import datasource
from individual import charts, week_hour, month_distance, pace_distance, month_pace, month_sessions

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

if op in ['calendar', 'kline'] :
    id = int(sys.argv[3])

print('data path :' + data_path)
print('op :' + op)

df = datasource.load_data(data_path)
if op == 'pkl':
    data_range = sys.argv[3] if (len(sys.argv) > 3) else ''
    datasource.pkl_data(df, data_range)
    sys.exit()

print(df.info())
print(df.describe())

datasource.init_data_range(df)
datasource.init_user_id_name_map(df)

def save_data(id, all_data):
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    file_name = os.path.join(data_dir, str(id))
    with open(file_name, 'w') as f:
        json.dump(all_data, f)

data_gens = [week_hour.gen_data, pace_distance.gen_data, month_distance.gen_data, month_pace.gen_data, month_sessions.gen_data]
index = 0
all_data = {}
for g, one_runner_data in df.groupby('id'):
    all_data = { 'runner' : datasource.user_id_to_name(g), 'dataset' : {} }
    for gen in data_gens:
        data = gen(one_runner_data)
        all_data['dataset'][data['name']] = { 'title' : data['title'], 'series' : data['series'] }
    save_data(g, all_data)
        
    index += 1

#print(all_data)

# charts.draw_groups_chart('individual', all_data['dataset'])

'''
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

if op == 'calendar':
    st_i.calendar_distance(df, id)

if op == 'kline':
    st_i.kline_pace(df,id)

charts.draw_charts()
'''

