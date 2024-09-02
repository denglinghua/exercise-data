def gen_data(df, _):
    data = df
    result = []
    for _, row in data.iterrows():
        date = row['end_time'].strftime('%Y-%m-%d')
        distance = round(row['distance'], 2)
        result.append([date, distance])
    
    return {'name':'date_distance', 'title' :'时间/距离分布', 'series' : result }