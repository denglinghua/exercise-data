from datetime import datetime, timedelta
import glob
import os

import pandas as pd

_file_data = {'min_year' : 9999, 'max_year':0, 'seq':1}

def _add_file_data(df:pd.DataFrame, file_path):
    global _file_data
    
    # ...\2016_0101-0131.xlsx
    end_mon_day = file_path[-9:-5]
    start_mon_day = file_path[-14:-10]
    year = int(file_path[-19:-15])
    
    if year < _file_data['min_year']:
        _file_data['min_year'] = year
    if year > _file_data['max_year']:
        _file_data['max_year'] = year
    
    max_data_date = df['end_time'].max()
    min_data_date = df['end_time'].min()

    def check_date(date, year, month_day):
        return date.strftime('%Y%m%d') == '%s%s' % (year, month_day)
    
    result = check_date(min_data_date, year, start_mon_day) and check_date(max_data_date,year, end_mon_day)

    key_ym = '%s%s' % (year, start_mon_day[0:2])
    _file_data[key_ym] = result

    desc = '' if result else '(%s - %s)' % (min_data_date, max_data_date)

    print('load data : [%s:%s:%s]%s' % (_file_data['seq'], key_ym, result, desc))
    _file_data['seq'] += 1

def _check_data():
    global _file_data
    for year in range(_file_data['min_year'], _file_data['max_year'] + 1):
        for m in range(1, 13):
            key = '%s%s' % (year, "{:02d}".format(m))
            failed_reason = None
            if key not in _file_data:
                failed_reason = 'file missed'
            else:
                if not _file_data[key]:
                    failed_reason = 'data not complete'
            if failed_reason:    
                print('#### %s data check failed - %s.' % (key, failed_reason))

def _to_date_time(str):
    format = '%Y-%m-%d %H:%M:%S'    
    return datetime.strptime(str, format)

def _to_time_delta(str):
    time_items = str.split(':')
    s = int(time_items[-1])
    m = int(time_items[-2])
    h = 0
    if (len(time_items) == 3):
        h = int(time_items[0])

    return timedelta(hours=h, minutes=m, seconds=s)

def _to_float(str):
    try:
        return float(str.replace(',', '')) # commas separate thousands
    except ValueError:
        return 0

def _to_int(str):
    try:
        return int(str.replace(',', '')) # commas separate thousands
    except ValueError:
        return 0

def _to_pace_time(str):
    time_items = str.split("'")
    m = int(time_items[0])
    s = int(time_items[1][:-1])
    
    return timedelta(minutes=m, seconds=s)

def _col_converts():
    ct = {
    'id': lambda a : int(a),
    'end_time': _to_date_time,
    'time': _to_time_delta,
    'pace': _to_pace_time,
    'cadence': _to_int,
    'stride': _to_float
    }

    return ct

def _calendar_table(from_date, years):
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

def _add_week_no_column(df:pd.DataFrame):
    earliest_date = df.at[0,'end_time']
    calendar = _calendar_table(earliest_date, 30)
    df["week_no"] = df.apply(lambda row: calendar[row['end_time'].strftime('%Y-%m-%d')], axis=1)

def load_data(data_dir):
    if data_dir.endswith('.pkl'):
        return pd.read_pickle(data_dir)

    cols = ['end_time', 'status', 'id', 'name', 'gender', 'distance', 'time', 'run_type',
                'pace', 'cadence', 'stride']
    df = pd.DataFrame(columns=cols)

    data_files = glob.glob(os.path.join(data_dir, '*.xlsx'))
    data_files.sort()

    # file named by date, so files ordered by date
    # data rows in a single file ordered by date too
    # so if all files loaded into one dataframe, these data rows ordered by date (end_time column)
    for file in data_files:
        one_file_df = pd.read_excel(file, header=7, names=cols, converters=_col_converts())
        # print(one_file_df)
        _add_file_data(one_file_df, file)
        df = df.append(one_file_df, ignore_index=True)
    
    _check_data()

    df['year'] = df['end_time'].dt.year
    df['month'] = df['end_time'].dt.to_period('M')

    _add_week_no_column(df)

    return df

_id_name = {}

def init_user_id_name_map(df:pd.DataFrame):
    data = df.groupby(['id', 'name']).count()
    data = data.reset_index()
    data = data[['id', 'name']]

    global _id_name 

    for index, row in data.iterrows():
        _id_name[row['id']] = row['name']

def user_id_to_name(id):
    global _id_name
    return _id_name[id]