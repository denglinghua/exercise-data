import sys

import datasource
import statistic as st
import charts

debug = False

data_dir = sys.argv[1]
if len(sys.argv) > 2 :
    debug = True if sys.argv[2] == 'debug' else False

print('data dir :' + data_dir)
print('debug :' + str(debug))

df = datasource.load_data(data_dir, debug)
#df.to_pickle('data.pkl')
print(df.info())
print(df.describe())

datasource.init_user_id_name_map(df)

#st.test(df)
#sys.exit(0)

st.marathon(df)

st.half_marathon(df)

st.distance(df)

st.pace(df)

st.time(df)

st.days(df)

st.cadence(df)

st.stride(df)

st.month_distance_std(df)

st.month_distance_detail(df)

st.distance_std(df)

st.pace_std(df)

st.pace_progress(df)

st.every_week(df)

#print(df.info())

charts.draw_charts()


