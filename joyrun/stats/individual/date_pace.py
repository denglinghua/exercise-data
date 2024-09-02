def gen_data(df, _):
    data = df[df['pace'].dt.total_seconds() < 660]
    result = []
    for _, row in data.iterrows():
        date = row['end_time'].strftime('%Y-%m-%d')
        pace = int(row['pace'].total_seconds())
        result.append([date, pace])
    
    return {'name':'date_pace', 'title' :'时间/配速分布', 'series' : result }