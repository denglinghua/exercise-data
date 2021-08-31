from group import Group, GroupRow, get_calc_func, check_data
from lang import lang

def create_basic_group(title, column, rows, filter_func, in_this_group_func, calc_func):
    group_rows = []
    for r in rows:
        group_row = GroupRow(r[0])
        group_row.keyword = r[1]
        group_rows.append(group_row)
        
    group = Group(title, column, group_rows, in_this_group_func, calc_func, filter_func)
    return group

def __activity_type_rows():
    return [
        (lang.running, lang.running),
        (lang.swimming, lang.swimming),
        (lang.cycling, lang.cycling_keyword)
    ]

def __in_activity_type_group_func(data_row, group, group_row): 
    return data_row[lang.col_activity_type].find(group_row.keyword) >= 0
    
@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_type_count_group():
    title = lang.activities
    column = lang.col_activity_type
    rows = __activity_type_rows()

    calc_func = get_calc_func("count")

    group = create_basic_group(title, column, rows, None, __in_activity_type_group_func, calc_func)
    group.set_ytitle(lang.activity_times)

    return group

def create_activity_type_distance_group():
    title = lang.total_distance
    column = lang.col_activity_type
    rows = __activity_type_rows()

    def calc_func(group, group_row):
        val = sum(r[lang.col_distance] for r in group_row.data_rows)
        if group_row.label ==lang.swimming:
            val = val / 1000
        return int(val)

    group = create_basic_group(title, column, rows, None, __in_activity_type_group_func, calc_func)
    group.set_ytitle(lang.km)
    
    return group

def create_activity_type_calory_group():
    title = lang.activity_calories
    column = lang.col_activity_type
    rows = __activity_type_rows()

    calc_func = get_calc_func('sum')

    group = create_basic_group(title, column, rows, None, __in_activity_type_group_func, calc_func)
    group.sum_column = lang.col_calories
    group.set_ytitle(lang.kcal)
    
    return group

def create_activity_type_time_group():
    title = lang.total_activity_time
    column = lang.col_activity_type
    rows = __activity_type_rows()

    calc_func = get_calc_func('sum')

    group = create_basic_group(title, column, rows, None, __in_activity_type_group_func, calc_func)
    group.sum_column = lang.col_time
    
    return group

def get_basic_groups() :
    return [
        create_activity_type_count_group(),
        create_activity_type_distance_group(),
        create_activity_type_time_group(),
        create_activity_type_calory_group()
    ]
