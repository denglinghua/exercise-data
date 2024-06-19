def _avg_pace(row):
    total_time_secs = row['time'].total_seconds()
    total_distance = row['distance']
    avg_pace = int(total_time_secs / total_distance)

    return avg_pace

def _create_result(x, y):
    return {'name':'month_pace', 'title' :'平均配速趋势', 'series' : { 'x':x, 'y':y } }

def gen_data(df, id):
    data = df[df['pace'].dt.total_seconds() < 660]
    if data.empty:
        print('No valid data for month_pace', id)
        return _create_result([], [])
    
    data = data[['month', 'time', 'distance']].copy()
    data = data.groupby("month").agg({'time':'sum','distance':'sum'})
    data = data.reset_index()
    data['avg_pace'] = data.apply(_avg_pace, axis=1)

    x = []
    y = []
    for _, row in data.iterrows():
        x.append(row['month'].strftime('%Y-%m'))
        y.append(row['avg_pace'])
    
    return _create_result(x, y)