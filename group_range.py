from group import Group, GroupSet, get_calc_func, check_data, create_series
from lang import lang

def __in_range_group_func(data_row, group_set, group):
    val = data_row[group_set.group_by_column]
    if group_set.value_func :
        val = group_set.value_func(val)
    return val >= group.low and val < group.up

def __filter_activity_type(data_row, keyword):
    return data_row[lang.col_activity_type].find(keyword) >= 0

def __filter_running_func(data_row):
    return __filter_activity_type(data_row, lang.running)

def __filter_swimming_func(data_row):
    return __filter_activity_type(data_row, lang.swimming)

def __filter_cycling_func(data_row):
    return __filter_activity_type(data_row, lang.cycling_keyword)

def __range_group_set(title, column, series, filter_func, value_func=None):
    groups = []
    for s in series:
        group = Group(s[0])
        group.low = s[1]
        group.up = s[2]
        groups.append(group)

    in_this_group_func = __in_range_group_func

    calc_func = get_calc_func("count")
    group_set = GroupSet(title, column, groups, in_this_group_func, calc_func, filter_func)
    group_set.value_func = value_func

    group_set.set_ytitle(lang.activity_times)
    return group_set

@check_data(lambda ctx, total : total == ctx['run_times'])
def __run_pace_group_set():
    title = lang.average_run_pace
    col = lang.col_avg_pace
    series = create_series(4, 9, 1, '%s:00')
    
    def value_func(val): return val.tm_min

    group_set = __range_group_set(title, col, series, __filter_running_func, value_func)
    group_set.xtitle = lang.run_pace_unit
    return group_set

@check_data(lambda ctx, total : total == ctx['run_times'])
def __run_cadence_group_set():
    title = lang.average_run_cadence
    col = lang.col_avg_run_cadence
    series = create_series(160, 200, 10, '%s')
    
    group_set = __range_group_set(title, col, series, __filter_running_func)
    group_set.xtitle = lang.steps_per_min
    return group_set

@check_data(lambda ctx, total : total == ctx['run_times'])
def __run_stride_group_set():
    title = lang.average_stride_length
    col = lang.col_avg_stride_length
    series = [("<0.7", 0, 0.7)]
    series.extend(map(lambda n : ('%s-%s' % (n, round(n+.1,2)), n, round(n+.1,2)), [0.7, 0.8, 0.9,1.0,1.1]))
    series.append((">=1.2", 1.2, 999))
    
    group_set = __range_group_set(title, col, series, __filter_running_func)
    group_set.xtitle = lang.m
    return group_set

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def __activity_hour_group_set():
    title = lang.activity_hours
    col = lang.col_date
    series = map(lambda h : (str(h) + lang.activity_h, h, h+1), range(0, 24))

    def value_func(val): return val.tm_hour

    return __range_group_set(title, col, series, None, value_func)

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def __activity_weekday_group_set():
    title = lang.activity_weekdays
    col = lang.col_date
    weekDays = lang.days_of_week
    series = map(lambda w : (weekDays[w], w, w+1), range(0, 7))

    def value_func(val): return val.tm_wday #Monday is 0

    return __range_group_set(title, col, series, None, value_func)

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def __activity_month_group_set():
    title = lang.activity_months
    col = lang.col_date
    months = lang.months
    series = map(lambda m : (months[m-1], m, m+1), range(1, 13))

    def value_func(val): return val.tm_mon

    return __range_group_set(title, col, series, None, value_func)

@check_data(lambda ctx, total : total == ctx['run_times'])
def __run_distance_group_set():
    title = lang.running_distance
    col = lang.col_distance
    series = create_series(5, 100, 5)
    group_set = __range_group_set(title, col, series, __filter_running_func)
    group_set.xtitle = lang.km
    return group_set

@check_data(lambda ctx, total : total == ctx['swim_times'])
def __swimming_distance_group_set():
    title = lang.swimming_distance
    col = lang.col_distance
    series = create_series(500, 5000, 500)

    group_set = __range_group_set(title, col, series, __filter_swimming_func)
    group_set.xtitle = lang.m
    return group_set

@check_data(lambda ctx, total : total == ctx['cycle_times'])
def __cycling_distance_group_set():
    title = lang.cycling_distance
    col = lang.col_distance
    series = create_series(20, 100, 20)

    group_set = __range_group_set(title, col, series, __filter_cycling_func)
    group_set.xtitle = lang.km
    return group_set

@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def __activity_time_group_set():
    title = lang.activity_time
    col = lang.col_time
    series = create_series(30, 180, 30)
    
    group_set = __range_group_set(title, col, series, None)
    group_set.xtitle = lang.min_full
    return group_set

def get_range_group_sets():
    return [
        __activity_time_group_set(),
        __activity_month_group_set(),
        __activity_weekday_group_set(),
        __activity_hour_group_set(),
        __run_distance_group_set(),
        __run_pace_group_set(),
        __run_cadence_group_set(),
        __run_stride_group_set(),
        __swimming_distance_group_set(),
        __cycling_distance_group_set()
    ]
