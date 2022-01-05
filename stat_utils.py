def print_df(df, message=''):
    print('\n')
    print(message)
    print(df)
    return df

def top_n(df, column, n, ascending=True):
    data = df.nlargest(n, column, 'all')
    data = data.sort_values(column, ascending=ascending)
    return data