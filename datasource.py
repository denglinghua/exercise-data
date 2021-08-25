import time

from lang import get_lang

def __to_time(str):
    strlen = len(str)
    format = ''
    if (strlen > 10):
        format = '%Y-%m-%d %H:%M:%S'
    elif (strlen > 6):
        format = '%H:%M:%S'
    else:
        format = '%M:%S'
    
    return time.strptime(str, format)

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

def __to_time_min(str):
    items = str.split(':')
    h = int(items[0])
    m = int(items[1])
    s = float(items[2])
    return int(h * 60 + m + int(s/60))

def __handle_data_row(row, data_type_map):
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
    data_type_map[get_lang('date')] = (__to_time,)
    data_type_map[get_lang('distance')] = (__to_float,)
    data_type_map[get_lang('avg_pace')] = (__to_time, __to_float) # 不同运动配速类型不同
    data_type_map[get_lang('avg_run_cadence')] = (__to_int,)
    data_type_map[get_lang('avg_stride_length')] = (__to_float,)
    data_type_map[get_lang('calories')] = (__to_int,)
    data_type_map[get_lang('time')] = (__to_time_min,)

    for row in raw_data:    
        __handle_data_row(row, data_type_map)


    