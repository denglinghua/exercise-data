import time
import glob

from data import csv_reader
from analysis import common

from lang import lang

def _to_time(str):
    strlen = len(str)
    format = ''
    if (strlen > 10):
        format = '%Y-%m-%d %H:%M:%S'
    elif (strlen > 6):
        format = '%H:%M:%S'
    else:
        format = '%M:%S'
    
    return time.strptime(str, format)

def _to_time_en(str):
    return time.strptime(str, '%m/%d/%Y %H:%M')

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

def _to_time_min(str):
    items = str.split(':')
    if len(items) < 3 :
        items.insert(0, 0)
    h = int(items[0])
    m = int(items[1])
    s = float(items[2])
    return int(h * 60 + m + int(s/60))

def _handle_data_row(row, data_type_map):
    for key in data_type_map:
        try:
            value_func = data_type_map[key][0]
            row[key] = value_func(row[key])
            # some records have 0 time, use Elapsed Time instead
            if key == 'Time':
                row[key] = value_func(row['Elapsed Time'])
        except ValueError:
            #print(row)
            alt_value_func = data_type_map[key][1]
            row[key] = alt_value_func(row[key])

def _prehandle_data(raw_data):
    data_type_map = {}
    data_type_map[lang.data__date] = (_to_time, _to_time_en)
    data_type_map[lang.data__distance] = (_to_float,)
    # the pace value varies by activity types
    # mm:ss/km for running, km/hour for cycling
    data_type_map[lang.data__avg_pace] = (_to_time, _to_float)
    data_type_map[lang.data__avg_run_cadence] = (_to_int,)
    data_type_map[lang.data__avg_stride_length] = (_to_float,)
    data_type_map[lang.data__calories] = (_to_int,)
    data_type_map[lang.data__time] = (_to_time_min,)

    for row in raw_data:    
        _handle_data_row(row, data_type_map)

def _filter_triathlon_data(rows):
    return [row for row in rows if _check_thriathlon_data(row)]

running_activities = 0
swimming_activities = 0
cycling_activities = 0

# for simplicity, it is a method with side effects
def _check_thriathlon_data(row):
    global running_activities, swimming_activities, cycling_activities
    if common.is_running(row):
        running_activities += 1
        return True
    if common.is_swimming(row):
        swimming_activities += 1
        return True
    if common.is_cycling(row):
        cycling_activities += 1
        return True
    return False 

def load_data(data_dir):
    files = glob.glob(data_dir + "/*_en.csv")
    rows = []
    for file in files:
        rows.extend(csv_reader.read_dict(file))
    print("Read %d files, %d rows" % (len(files), len(rows)))
    
    _prehandle_data(rows)
    
    rows = _filter_triathlon_data(rows)
    
    print("Triathon activities : %d, running: %d, swimming: %d, cycling: %d" % (len(rows), running_activities, swimming_activities, cycling_activities))
    
    return rows


    