def gen_data(df):
    data = df[['end_time', 'time']].copy()
    data['start_date'] = df['end_time'] - df['time']
    data['week_day'] = data['start_date'].map(lambda x : x.weekday())
    data['hour'] = data['start_date'].map(lambda x : x.hour)
    data = data.groupby(['week_day', 'hour']).count()
    result = []
    for (week_day, hour), row in data.iterrows():
        result.append([hour, week_day, int(row['time'])])
    
    return {'name':'week_hour', 'title' :'跑步时辰', 'data':result}