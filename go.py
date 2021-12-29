import sys

from datasource import load_data
import statistic as st

data_dir = sys.argv[1]

df = load_data(data_dir, False)

# st.test(df)

st.full_marathon(df)

st.distance(df)

st.every_week(df)

st.pace(df)

st.total_time(df)

st.total_days(df)

st.top_stride_len(df)

st.month_distance_std(df)



