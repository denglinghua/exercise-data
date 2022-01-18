import time

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
        except ValueError:
            #print(row)
            alt_value_func = data_type_map[key][1]
            row[key] = alt_value_func(row[key])

def prehandle_data(raw_data):
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


    