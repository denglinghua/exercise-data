def gen_data(df):
    data = df[['month', 'distance']].copy()
    data = data.groupby('month').sum('distance')
    x = []
    y = []
    for month, row in data.iterrows():
        x.append(month.strftime('%Y-%m'))
        y.append(row['distance'])
    
    return {'name':'month_distance', 'data' : { 'x':x, 'y':y } }