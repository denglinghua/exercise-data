# encoding:utf-8
from group import Group, GroupRow, str_to_time
from lang import get_lang

def __in_range_group_func(data_row, group, group_row):
    val = group.value_func(data_row[group.column])
    return val >= group_row.low and val < group_row.up

def __filter_running_func(data_row):
    return data_row[get_lang('activity_type')].find(get_lang('running')) >= 0

def create_range_group(title, column, rows, filter_func, value_func):
    group_rows = []
    for row in rows:
        group_row = GroupRow(row[0])
        group_row.low = row[1]
        group_row.up = row[2]
        group_rows.append(group_row)

    in_this_group_func = __in_range_group_func

    group = Group(title, column, group_rows, filter_func, in_this_group_func)
    group.value_func = value_func

    return group

def create_avg_pace_group():
    title = '跑多快'
    col = get_lang('avg_pace')
    rows = [("<4:00分", 1, 4)]
    for n in range(4, 9):
        rows.append(('%s-%s:00分' % (n, n+1), n, n + 1))
    rows.append((">9:00分", 9, 999))
    
    def value_func(val): return str_to_time(val).tm_min

    return create_range_group(title, col, rows, __filter_running_func, value_func)

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

def create_avg_run_distance_group():
    title = '跑多远'
    col = get_lang('distance')
    rows = []
    for d in range(0, 20):
        start = d * 5
        end = start + 5
        rows.append(('%s-%skm' % (start, end), start, end))

    def value_func(val): return float(val)

    return create_range_group(title, col, rows, __filter_running_func, value_func)

def get_range_groups():
    return [
        create_activity_month_group(),
        create_activity_weekday_group(),
        create_activity_hour_group(),
        create_avg_run_distance_group(),
        create_avg_pace_group()
    ]

