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
    data.joy_run_id = data.joy_run_id.astype("category")
    data.joy_run_id.cat.set_categories(id_list[::-1], inplace=True)
    data.sort_values(['joy_run_id'])
    
    return data