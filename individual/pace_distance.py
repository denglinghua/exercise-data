def gen_data(df):
    data = df
    result = []
    for index, row in data.iterrows():
        distance = row['distance']
        pace = row['pace'].total_seconds()
        result.append([distance, pace])
    
    return {'name':'pace_distance', 'data' : result }