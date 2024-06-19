def gen_data(df, _):
    data = df[['month', 'distance']].copy()
    data = data.groupby('month').count()
    x = []
    y = []
    for month, row in data.iterrows():
        x.append(month.strftime('%Y-%m'))
        y.append(row['distance'].item())
    
    return {'name':'month_sessions', 'title' :'月跑步次数趋势', 'series' : { 'x':x, 'y':y } }