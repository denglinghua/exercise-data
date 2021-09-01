from group import Group, GroupSet, get_calc_func, check_data
from lang import lang

def __basic_group_set(title, column, series, filter_func, in_this_group_func, calc_func):
    groups = []
    for s in series:
        group = Group(s[0])
        group.keyword = s[1]
        groups.append(group)
        
    group_set = GroupSet(title, column, groups, in_this_group_func, calc_func, filter_func)
    return group_set

def __activity_type_series():
    return [
        (lang.running, lang.running),
        (lang.swimming, lang.swimming),
        (lang.cycling, lang.cycling_keyword)
    ]

def __in_activity_type_group_func(data_row, group, group_row): 
    return data_row[lang.col_activity_type].find(group_row.keyword) >= 0
    
@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def __activity_type_count_group_set():
    title = lang.activities
    column = lang.col_activity_type
    series = __activity_type_series()

    calc_func = get_calc_func("count")

    group_set = __basic_group_set(title, column, series, None, __in_activity_type_group_func, calc_func)
    group_set.set_ytitle(lang.activity_times)

    return group_set

def __activity_type_distance_group_set():
    title = lang.total_distance
    column = lang.col_activity_type
    series = __activity_type_series()

    def calc_func(group, group_row):
        val = sum(r[lang.col_distance] for r in group_row.data_rows)
        if group_row.label ==lang.swimming:
            val = val / 1000
        return int(val)

    group_set = __basic_group_set(title, column, series, None, __in_activity_type_group_func, calc_func)
    group_set.set_ytitle(lang.km)
    
    return group_set

def __activity_type_calory_group_set():
    title = lang.activity_calories
    column = lang.col_activity_type
    series = __activity_type_series()

    calc_func = get_calc_func('sum')

    group_set = __basic_group_set(title, column, series, None, __in_activity_type_group_func, calc_func)
    group_set.sum_column = lang.col_calories
    group_set.set_ytitle(lang.kcal)
    
    return group_set

def __activity_type_time_group_set():
    title = lang.total_activity_time
    column = lang.col_activity_type
    series = __activity_type_series()

    calc_func = get_calc_func('sum')

    group_set = __basic_group_set(title, column, series, None, __in_activity_type_group_func, calc_func)
    group_set.sum_column = lang.col_time
    
    return group_set

def get_basic_group_sets() :
    return [
        __activity_type_count_group_set(),
        __activity_type_distance_group_set(),
        __activity_type_time_group_set(),
        __activity_type_calory_group_set()
    ]
