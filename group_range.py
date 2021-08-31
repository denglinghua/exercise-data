from group import Group, GroupRow, get_calc_func, check_data
from lang import lang

def __in_range_group_func(data_row, group, group_row):
    val = data_row[group.column]
    if group.value_func :
        val = group.value_func(val)
    return val >= group_row.low and val < group_row.up

def __filter_running_func(data_row):
    return data_row[lang.col_activity_type].find(lang.running) >= 0

def __filter_swimming_func(data_row):
    return data_row[lang.col_activity_type].find(lang.swimming) >= 0

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

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_pace_group():
    title = lang.average_run_pace
    col = lang.col_avg_pace
    rows = [("<4:00", 1, 4)]
    rows.extend(map(lambda n : ('%s:00-%s:00' % (n, n+1), n, n + 1), range(4, 9)))    
    rows.append((">9:00", 9, 999))
    
    def value_func(val): return val.tm_min

    group = create_range_group(title, col, rows, __filter_running_func, value_func)
    group.xtitle = lang.run_pace_unit
    return group

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_cadence_group():
    title = lang.average_run_cadence
    col = lang.col_avg_run_cadence
    rows = [("<160", 1, 160)]
    rows.extend(map(lambda n : ('%s+' % n, n, n + 10), [160, 170, 180, 190]))
    rows.append((">200", 200, 999))
    
    group = create_range_group(title, col, rows, __filter_running_func)
    group.xtitle = lang.steps_per_min
    return group

@check_data(lambda ctx, total : total == ctx['run_times'])
def create_run_stride_group():
    title = lang.average_stride_length
    col = lang.col_avg_stride_length
    rows = [("<0.7", 0, 0.7)]
    rows.extend(map(lambda n : ('%s' % n, n, n + 0.1), [0.7, 0.8, 0.9,1.0,1.1]))
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
    rows = map(lambda d : ('%s-%s' % (d*5, (d+1)*5), d*5, (d+1)*5), range(0, 20))
    group = create_range_group(title, col, rows, __filter_running_func)
    group.xtitle = lang.km
    return group

@check_data(lambda ctx, total : total == ctx['swim_times'])
def create_swimming_distance_group():
    title = lang.swimming_distance
    col = lang.col_distance
    rows = [('<500', 0, 500)]
    rows.extend(map(lambda i : ('%s-%s' % (i*500, (i+1)*500), i*500, (i+1)*500), range(1,9)))
    rows.append(('>5000', 5000, 999999))

    group = create_range_group(title, col, rows, __filter_swimming_func)
    group.xtitle = lang.m
    return group

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
