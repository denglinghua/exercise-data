# encoding:utf-8
from group import Group, GroupRow, str_to_time, get_calc_func
from lang import get_lang

def __in_range_group_func(data_row, group, group_row):
    val = group.value_func(data_row[group.column])
    return val >= group_row.low and val < group_row.up

def __filter_running_func(data_row):
    return data_row[get_lang('activity_type')].find(get_lang('running')) >= 0

def __filter_swimming_func(data_row):
    return data_row[get_lang('activity_type')].find(get_lang('swimming')) >= 0

def create_range_group(title, column, rows, filter_func, value_func):
    group_rows = []
    for row in rows:
        group_row = GroupRow(row[0])
        group_row.low = row[1]
        group_row.up = row[2]
        group_rows.append(group_row)

    in_this_group_func = __in_range_group_func

    calc_func = get_calc_func("count")
    group = Group(title, column, group_rows, in_this_group_func, calc_func, filter_func)
    group.value_func = value_func

    group.set_ytitle("次")

    return group

def create_run_pace_group():
    title = '跑多快'
    col = get_lang('avg_pace')
    rows = [("<4:00分", 1, 4)]
    for n in range(4, 9):
        rows.append(('%s-%s:00分' % (n, n+1), n, n + 1))
    rows.append((">9:00分", 9, 999))
    
    def value_func(val): return str_to_time(val).tm_min

    return create_range_group(title, col, rows, __filter_running_func, value_func)

def create_run_cadence_group():
    title = '步频'
    col = get_lang('avg_run_cadence')
    rows = [
        ("<160步/分", 1, 160),
        ("160+步/分", 160, 170),
        ("170+步/分", 170, 180),
        ("180+步/分", 180, 190),
        ("190+步/分", 190, 200),
        (">200步/分", 200, 999)
        ]
    
    def value_func(val): return int(val)

    def filter_running_cadence(data_row):
        return __filter_running_func(data_row) and data_row[col].isdigit()

    return create_range_group(title, col, rows, filter_running_cadence, value_func)

def create_run_stride_group():
    title = '步长'
    col = get_lang('avg_stride_length')
    rows = [
        ("<0.7m", 0, 0.7),
        ("0.7+m", 0.7, 0.8),
        ("0.8+m", 0.8, 0.9),
        ("0.9+m", 0.9, 1.0),
        ("1.0+m", 1.0, 1.1),
        ("1.1+m", 1.1, 1.2),
        (">1.2m", 1.2, 999)
        ]
    
    def value_func(val): return float(val)

    def filter_running_stride(data_row):
        return __filter_running_func(data_row) and not data_row[col].startswith('-')

    return create_range_group(title, col, rows, filter_running_stride, value_func)

def create_activity_hour_group():
    title = '那些时辰比较活跃'
    col = get_lang('date')
    rows = []
    for h in range(0, 24):
        rows.append((str(h) + "时", h, h+1))

    def value_func(val): return str_to_time(val).tm_hour

    return create_range_group(title, col, rows, None, value_func)

def create_activity_weekday_group():
    title = '星期几比较活跃'
    col = get_lang('date')
    weekDays = ("一","二","三","四","五","六","日")
    rows = []
    for w in range(0, 7):
        rows.append((weekDays[w], w, w+1))

    def value_func(val): return str_to_time(val).tm_wday

    return create_range_group(title, col, rows, None, value_func)

def create_activity_month_group():
    title = '那些月份比较活跃'
    col = get_lang('date')
    rows = []
    for m in range(1, 13):
        rows.append((str(m) + "月", m, m+1))

    def value_func(val): return str_to_time(val).tm_mon

    return create_range_group(title, col, rows, None, value_func)

def create_run_distance_group():
    title = '跑多远'
    col = get_lang('distance')
    rows = []
    for d in range(0, 20):
        start = d * 5
        end = start + 5
        rows.append(('%s-%skm' % (start, end), start, end))

    def value_func(val): return float(val)

    return create_range_group(title, col, rows, __filter_running_func, value_func)

def create_swimming_distance_group():
    title = '游多远'
    col = get_lang('distance')
    rows = [('<500m', 0, 500)]
    for i in range(1, 9):
        start = i * 500
        end = start + 500
        rows.append(('%s-%sm' % (start, end), start, end))
    rows.append(('>5000m', 5000, 999999))

    def value_func(val): return int(val.replace(',', ''))

    return create_range_group(title, col, rows, __filter_swimming_func, value_func)

def get_range_groups():
    return [
        create_activity_month_group(),
        create_activity_weekday_group(),
        create_activity_hour_group(),
        create_run_distance_group(),
        create_run_pace_group(),
        create_run_cadence_group(),
        create_run_stride_group(),
        create_swimming_distance_group()
    ]

