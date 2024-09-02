import sys
import os
import pandas as pd
import pyecharts
import json

import datasource
from individual import week_hour, month_distance, pace_distance, month_pace, month_sessions, date_distance, date_pace

print('\nstart...')
print('python version :' + sys.version)
print('pandas version :' + pd.__version__)
print('pyecharts version :' + pyecharts.__version__)

# usage : python go.py data_path [op=report]
op = 'report'
data_path = sys.argv[1]

if (len(sys.argv) > 2):
    op = sys.argv[2]

print('data path :' + data_path)
print('op :' + op)

df = datasource.load_data(data_path)

print(df.info())
print(df.describe())

def save_data(id, all_data):
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    file_name = os.path.join(data_dir, str(id))
    with open(file_name, 'w') as f:
        json.dump(all_data, f)

if op == 'pkl':
    data_range = sys.argv[3] if (len(sys.argv) > 3) else ''
    datasource.pkl_data(df, data_range)

if op == 'report':
    datasource.init_data_range(df)
    datasource.init_user_id_name_map(df)

    data_gens = [week_hour.gen_data, pace_distance.gen_data, month_distance.gen_data, month_pace.gen_data, month_sessions.gen_data, date_distance.gen_data, date_pace.gen_data]
    index = 0
    all_data = {}
    for g, one_runner_data in df.groupby('id'):
        all_data = { 'runner' : datasource.user_id_to_name(g), 'dataset' : {} }
        for gen in data_gens:
            # the second parameter is the group(id) just used to debuging
            data = gen(one_runner_data, g)
            all_data['dataset'][data['name']] = { 'title' : data['title'], 'series' : data['series'] }
        save_data(g, all_data)
            
        index += 1
    
    print('total runners : ' + str(index))

print('done...')