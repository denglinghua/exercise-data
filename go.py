import sys

from datasource import load_data, user_id_name_map
import statistic as st
from charts import create_chart_data, draw_charts
from chart_config import charts

debug = False

data_dir = sys.argv[1]
if len(sys.argv) > 2 :
    debug = True if sys.argv[2] == 'debug' else False

print('data dir :' + data_dir)
print('debug :' + str(debug))

df = load_data(data_dir, debug)

id_name = user_id_name_map(df)

def add_chart(chart_config, df):
    create_chart_data(df, id_name, chart_config)

# st.test(df)

add_chart(charts.marathon, st.full_marathon(df))

add_chart(charts.distance, st.distance(df))

st.every_week(df)

add_chart(charts.pace, st.pace(df))

add_chart(charts.time, st.total_time(df))

add_chart(charts.days, st.total_days(df))

add_chart(charts.stride, st.top_stride_len(df))

add_chart(charts.month_distance_std, st.month_distance_std(df))

add_chart(charts.pace_std, st.pace_std(df))

#print(df.info())

draw_charts()


