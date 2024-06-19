def gen_data(df, _):
    data = df[df['pace'].dt.total_seconds() < 660]
    # data = df
    result = []
    for _, row in data.iterrows():
        distance = round(row['distance'], 2)
        pace = int(row['pace'].total_seconds())
        result.append([distance, pace])
    
    return {'name':'pace_distance', 'title' :'距离/配速分布', 'series' : result }