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

debug = False
id = 0

data_dir = sys.argv[1]
if (len(sys.argv) > 2):
    id = int(sys.argv[2])

if len(sys.argv) > 3 :
    debug = True if sys.argv[3] == 'debug' else False

print('data dir :' + data_dir)
print('debug :' + str(debug))

df = datasource.load_data(data_dir, debug)
#df.to_pickle('data.pkl')
#sys.exit(0)
print(df.info())
print(df.describe())

datasource.init_user_id_name_map(df)

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

if (id > 0):
    st_i.calendar_distance(df, id)

charts.draw_charts()


