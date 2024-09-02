from datetime import datetime, timedelta
import glob
import os

import pandas as pd

_file_data = {'min_year' : 9999, 'max_year':0, 'seq':1}
_data_range = ''

def _extract_date(file_path):
    # ...\2016_0101-0131.xlsx
    end_day = file_path[-7:-5]
    start_day = file_path[-12:-10]
    month = file_path[-14:-12]
    year = int(file_path[-19:-15])
    return year, month, start_day, end_day

def _add_file_data(df:pd.DataFrame, file_path):
    global _file_data
    
    year, month, start_day, end_day = _extract_date(file_path)
    
    if year < _file_data['min_year']:
        _file_data['min_year'] = year
    if year > _file_data['max_year']:
        _file_data['max_year'] = year
    
    max_data_date = df['end_time'].max()
    min_data_date = df['end_time'].min()

    def check_date(date, year, month, day):
        return date.strftime('%Y%m%d') == '%s%s%s' % (year, month, day)
    
    result = check_date(min_data_date, year, month, start_day) and check_date(max_data_date,year, month, end_day)

    key_ym = '%s%s' % (year, month)
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
    # if pkl file exists, load it
    df = None
    max_data_date = None
    if os.path.exists('data_.pkl'):
        df = pd.read_pickle('data_.pkl')
        max_data_date = df['end_time'].max()
        print('exist data max date: %s' % max_data_date)
    else:
        df = pd.DataFrame(columns=cols)

    data_files = glob.glob(os.path.join(data_dir, '*.xlsx'))
    data_files.sort()

    # file named by date, so files ordered by date
    # data rows in a single file ordered by date too
    # so if all files loaded into one dataframe, these data rows ordered by date (end_time column)
    for file in data_files:
        if max_data_date:
            year, month, start_day, _ = _extract_date(file)
            if max_data_date > datetime(year, int(month), int(start_day)):
                print('skip file: %s' % file)
                continue
        one_file_df = pd.read_excel(file, header=7, names=cols, converters=_col_converts())
        # print(one_file_df)
        _add_file_data(one_file_df, file)
        df = pd.concat([df, one_file_df], ignore_index=True)
    
    _check_data()

    df['year'] = df['end_time'].dt.year
    df['month'] = df['end_time'].dt.to_period('M')

    _add_week_no_column(df)

    return df

def pkl_data(df:pd.DataFrame, data_range:str):
    data = df
    if data_range:
        print('data range: ' + data_range)
        items = data_range.split("-")
        start_year = int(items[0])
        end_year = int(items[1])
        data = df[df.year.between(start_year, end_year)]
    
    data.to_pickle('data_' + data_range + '.pkl')

def init_data_range(df:pd.DataFrame):
    begin = df['year'].min()
    end = df['year'].max()
    global _data_range
    _data_range = '%s-%s' % (begin, end)

def data_range():
    return _data_range

_id_name = {}

def init_user_id_name_map(df:pd.DataFrame):
    data = df[['id', 'name', 'end_time']]
    data = data.groupby(['id', 'name']).max()
    data = data.reset_index()
    data = data[['id', 'name', 'end_time']]
    # some runner might change name, so use the last end_time to get the latest name
    data = data.sort_values(by=['end_time'], ascending=[True])

    global _id_name 

    for index, row in data.iterrows():
        _id_name[row['id']] = row['name']

def user_id_to_name(id):
    global _id_name
    return _id_name[id]