from datetime import datetime, timedelta
import glob
import os

import pandas as pd

def __to_date_time(str):
    format = '%Y-%m-%d %H:%M:%S'    
    return datetime.strptime(str, format)

def __to_time_delta(str):
    time_items = str.split(':')
    s = int(time_items[-1])
    m = int(time_items[-2])
    h = 0
    if (len(time_items) == 3):
        h = int(time_items[0])

    return timedelta(hours=h, minutes=m, seconds=s)

def __to_float(str):
    try:
        return float(str.replace(',', '')) # commas separate thousands
    except ValueError:
        return 0

def __to_int(str):
    try:
        return int(str.replace(',', '')) # commas separate thousands
    except ValueError:
        return 0

def __to_pace_time(str):
    time_items = str.split("'")
    m = int(time_items[0])
    s = int(time_items[1][:-1])
    
    return timedelta(minutes=m, seconds=s)

def __col_converts():
    ct = {
    'joy_run_id': lambda a : int(a),
    'end_time': __to_date_time,
    'time': __to_time_delta,
    'pace': __to_pace_time,
    'cadence': __to_int,
    'stride_len': __to_float
    }

    return ct

def calendar_table(from_date, years):
    t = {}
    week_no = 1
    d = from_date
    end_date = from_date + timedelta(days=years * 365)
    while d <= end_date:
        t[d.strftime('%Y-%m-%d')] = week_no
        d = d + timedelta(days=1)
        if d.weekday() == 0:
            week_no = week_no + 1
    
    return t

def add_week_no_column(df:pd.DataFrame):
    earliest_date = df.at[0,'end_time']
    calendar = calendar_table(earliest_date, 30)
    df["week_no"] = df.apply(lambda row: calendar[row['end_time'].strftime('%Y-%m-%d')], axis=1)

def load_data(data_dir, debug = False):
    cols = ['end_time', 'status', 'joy_run_id', 'name', 'gender', 'distance', 'time', 'run_type',
                'pace', 'cadence', 'stride_len']
    df = pd.DataFrame(columns=cols)

    data_files = glob.glob(os.path.join(data_dir, '*.xlsx'))
    data_files.sort()

    if debug :
        data_files = data_files[0:1]
    
    # file named by date, so files ordered by date
    # data rows in a single file ordered by date too
    # so if all files loaded into one dataframe, these data rows ordered by date (end_time column)
    for file in data_files:
        one_file_df = pd.read_excel(file, header=7, names=cols, converters=__col_converts())
        # print(one_file_df)
        df = df.append(one_file_df, ignore_index=True)
    
    add_week_no_column(df)

    print(df.info())
    print(df.describe())

    return df

def user_id_name_map(df:pd.DataFrame):
    data = df.groupby(['joy_run_id', 'name']).count()
    data = data.reset_index()
    data = data[['joy_run_id', 'name']]

    id_name = {}

    for index, row in data.iterrows():
        id_name[row['joy_run_id']] = row['name']


    return id_name