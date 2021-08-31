from group import Group, GroupRow, get_calc_func, check_data
from lang import lang

def __in_range_group_func(data_row, group, group_row):
    val = data_row[group.column]
    if group.value_func :
        val = group.value_func(val)
    return val >= group_row.low and val < group_row.up

def __filter_activity_type(data_row, keyword):
    return data_row[lang.col_activity_type].find(keyword) >= 0

def __filter_running_func(data_row):
    return __filter_activity_type(data_row, lang.running)

def __filter_swimming_func(data_row):
    return __filter_activity_type(data_row, lang.swimming)

def __filter_cycling_func(data_row):
    return __filter_activity_type(data_row, lang.cycling_keyword)

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

    group.set_ytitle(lang.activity_times)
    return group

def __create_series(start, end, step=1, format='%s', list = None):
    series = [("<" + format % start, 0, start)]
    def map_func(n):
        s = n
        e = n + step
        label = '%s-%s' % (format % s, format % e)
        return (label, s, e)
    if list:
        series.extend(map(map_func, list))
    else:
        series.extend(map(map_func, range(start, end, step)))
    series.append((">" + format % end, end, 9999999))
    return series

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_pace_group():
    title = lang.average_run_pace
    col = lang.col_avg_pace
    rows = __create_series(4, 9, 1, '%s:00')
    
    def value_func(val): return val.tm_min

    group = create_range_group(title, col, rows, __filter_running_func, value_func)
    group.xtitle = lang.run_pace_unit
    return group

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_cadence_group():
    title = lang.average_run_cadence
    col = lang.col_avg_run_cadence
    rows = __create_series(160, 200, 10, '%s')
    
    group = create_range_group(title, col, rows, __filter_running_func)
    group.xtitle = lang.steps_per_min
    return group

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_stride_group():
    title = lang.average_stride_length
    col = lang.col_avg_stride_length
    rows = [("<0.7", 0, 0.7)]
    rows.extend(map(lambda n : ('%s-%s' % (n, round(n+.1,2)), n, round(n+.1,2)), [0.7, 0.8, 0.9,1.0,1.1]))
    rows.append((">1.2", 1.2, 999))
    
    group = create_range_group(title, col, rows, __filter_running_func)
    group.xtitle = lang.m
    return group

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_hour_group():
    title = lang.activity_hours
    col = lang.col_date
    rows = map(lambda h : (str(h) + lang.activity_h, h, h+1), range(0, 24))

    def value_func(val): return val.tm_hour

    return create_range_group(title, col, rows, None, value_func)

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_weekday_group():
    title = lang.activity_weekdays
    col = lang.col_date
    weekDays = lang.days_of_week
    rows = map(lambda w : (weekDays[w], w, w+1), range(0, 7))

    def value_func(val): return val.tm_wday

    return create_range_group(title, col, rows, None, value_func)

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_month_group():
    title = lang.activity_months
    col = lang.col_date
    months = lang.months
    rows = map(lambda m : (months[m-1], m, m+1), range(1, 13))

    def value_func(val): return val.tm_mon

    return create_range_group(title, col, rows, None, value_func)

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_distance_group():
    title = lang.running_distance
    col = lang.col_distance
    rows = __create_series(5, 100, 5)
    group = create_range_group(title, col, rows, __filter_running_func)
    group.xtitle = lang.km
    return group

@check_data(lambda ctx, total : total == ctx['swim_times'])
def create_swimming_distance_group():
    title = lang.swimming_distance
    col = lang.col_distance
    rows = __create_series(500, 5000, 500)

    group = create_range_group(title, col, rows, __filter_swimming_func)
    group.xtitle = lang.m
    return group

@check_data(lambda ctx, total : total == ctx['cycle_times'])
def create_cycling_distance_group():
    title = lang.cycling_distance
    col = lang.col_distance
    rows = __create_series(20, 100, 20)

    group = create_range_group(title, col, rows, __filter_cycling_func)
    group.xtitle = lang.km
    return group

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_time_group():
    title = lang.activity_time
    col = lang.col_time
    rows = __create_series(30, 180, 30)
    
    group = create_range_group(title, col, rows, None)
    group.xtitle = lang.min_full
    return group

def get_range_groups():
    return [
        create_activity_time_group(),
        create_activity_month_group(),
        create_activity_weekday_group(),
        create_activity_hour_group(),
        create_run_distance_group(),
        create_run_pace_group(),
        create_run_cadence_group(),
        create_run_stride_group(),
        create_swimming_distance_group(),
        create_cycling_distance_group()
    ]
