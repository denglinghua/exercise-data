def gen_data(df, _):
    data = df[['month', 'distance']].copy()
    data = data.groupby('month').sum('distance')
    x = []
    y = []
    for month, row in data.iterrows():
        x.append(month.strftime('%Y-%m'))
        y.append(round(row['distance'],2))
    
    return {'name':'month_distance', 'title' :'月跑量趋势', 'series' : { 'x':x, 'y':y } }