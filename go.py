import sys

from datasource import load_data, user_id_name_map
import statistic as st
from charts import create_chart_data, draw_charts

data_dir = sys.argv[1]

df = load_data(data_dir, False)

id_name = user_id_name_map(df)

chart_data_list = []

def add_chart(title, val_col, df):
    chart_data_list.append(create_chart_data(df, val_col, id_name, title))

# st.test(df)

add_chart('full marathon', 'distance', st.full_marathon(df))

add_chart('top distance', 'distance', st.distance(df))

st.every_week(df)

st.pace(df)

st.total_time(df)

st.total_days(df)

st.top_stride_len(df)

st.month_distance_std(df)

#print(df.info())

draw_charts('Joyrun team run data stat', chart_data_list)


