def print_df(df, message=''):
    print('\n')
    print(message)
    print(df)
    return df

def top_n(df, column, n, ascending=True):
    data = df.nlargest(n, column, 'all')
    data = data.sort_values(column, ascending=ascending)
    return data

def sort_data_by_id_list(data, id_list):
    data.id = data.id.astype("category")
    # data.id.cat.set_categories(id_list[::-1], inplace=True)
    data['id'] = data['id'].cat.set_categories(id_list[::-1])
    data.sort_values(['id'])
    
    return data