def gen_data(df):
    data = df[['month', 'pace']].copy()
    data = data[data['pace'].dt.total_seconds() < 600]
    data = data.groupby('month').mean()
    x = []
    y = []
    for month, row in data.iterrows():
        x.append(month.strftime('%Y-%m'))
        y.append(row['pace'].total_seconds())
    
    return {'name':'month_pace', 'data' : { 'x':x, 'y':y } }