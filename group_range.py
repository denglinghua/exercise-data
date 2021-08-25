# encoding:utf-8
from group import Group, GroupRow, get_calc_func, check_data
from lang import get_lang

def __in_range_group_func(data_row, group, group_row):
    val = data_row[group.column]
    if group.value_func :
        val = group.value_func(val)
    return val >= group_row.low and val < group_row.up

def __filter_running_func(data_row):
    return data_row[get_lang('activity_type')].find(get_lang('running')) >= 0

def __filter_swimming_func(data_row):
    return data_row[get_lang('activity_type')].find(get_lang('swimming')) >= 0

def create_range_group(title, column, rows, filter_func, value_func=None):
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

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_pace_group():
    title = '跑多快'
    col = get_lang('avg_pace')
    rows = [("<4:00分", 1, 4)]
    rows.extend(map(lambda n : ('%s:00-%s:00分' % (n, n+1), n, n + 1), range(4, 9)))    
    rows.append((">9:00分", 9, 999))
    
    def value_func(val): return val.tm_min

    return create_range_group(title, col, rows, __filter_running_func, value_func)

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_cadence_group():
    title = '步频'
    col = get_lang('avg_run_cadence')
    rows = [("<160 步/分", 1, 160)]
    rows.extend(map(lambda n : ('%s+ 步/分' % n, n, n + 10), [160, 170, 180, 190]))
    rows.append((">200 步/分", 200, 999))
    
    return create_range_group(title, col, rows, __filter_running_func)

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_stride_group():
    title = '步长'
    col = get_lang('avg_stride_length')
    rows = [("<0.7 m", 0, 0.7)]
    rows.extend(map(lambda n : ('%s+ m' % n, n, n + 0.1), [0.7, 0.8, 0.9,1.0,1.1]))
    rows.append((">1.2 m", 1.2, 999))
    
    return create_range_group(title, col, rows, __filter_running_func)

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_hour_group():
    title = '那些时辰比较活跃'
    col = get_lang('date')
    rows = map(lambda h : (str(h) + '时', h, h+1), range(0, 24))

    def value_func(val): return val.tm_hour

    return create_range_group(title, col, rows, None, value_func)

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_weekday_group():
    title = '星期几比较活跃'
    col = get_lang('date')
    weekDays = ("一","二","三","四","五","六","日")
    rows = map(lambda w : (weekDays[w], w, w+1), range(0, 7))

    def value_func(val): return val.tm_wday

    return create_range_group(title, col, rows, None, value_func)

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_month_group():
    title = '那些月份比较活跃'
    col = get_lang('date')
    rows = map(lambda m : ((str(m) + "月", m, m+1)), range(1, 13))

    def value_func(val): return val.tm_mon

    return create_range_group(title, col, rows, None, value_func)

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_distance_group():
    title = '跑多远'
    col = get_lang('distance')
    rows = map(lambda d : ('%s-%skm' % (d*5, (d+1)*5), d*5, (d+1)*5), range(0, 20))
    return create_range_group(title, col, rows, __filter_running_func)

@check_data(lambda ctx, total : total == ctx['swim_times'])
def create_swimming_distance_group():
    title = '游多远'
    col = get_lang('distance')
    rows = [('<500m', 0, 500)]
    rows.extend(map(lambda i : ('%s-%sm' % (i*500, (i+1)*500), i*500, (i+1)*500), range(1,9)))
    rows.append(('>5000m', 5000, 999999))

    return create_range_group(title, col, rows, __filter_swimming_func)

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
