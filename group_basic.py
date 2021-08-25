# encoding:utf-8
from group import Group, GroupRow, get_calc_func, check_data
from lang import get_lang

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
        ("跑步", get_lang('running')),
        ("游泳", get_lang('swimming')),
        ("自行车", get_lang('cycling'))
    ]

def __in_activity_type_group_func(data_row, group, group_row): 
    return data_row[get_lang('activity_type')].find(group_row.keyword) >= 0
    
@check_data(lambda ctx, total : total == ctx['data_rows_count'])
def create_activity_type_count_group():
    title = "三项分别做了多少次"
    column = get_lang('activity_type')
    rows = __activity_type_rows()

    calc_func = get_calc_func("count")

    group = create_basic_group(title, column, rows, None, __in_activity_type_group_func, calc_func)
    group.set_ytitle("次")

    return group

def create_activity_type_distance_group():
    title = "三项距离"
    column = get_lang('activity_type')
    rows = __activity_type_rows()

    def calc_func(group, group_row):
        val = sum(r[get_lang("distance")] for r in group_row.data_rows)
        if group_row.label =='游泳':
            val = val / 1000
        return int(val)

    group = create_basic_group(title, column, rows, None, __in_activity_type_group_func, calc_func)
    group.set_ytitle("公里")
    
    return group

def create_activity_type_calory_group():
    title = "三项热量消耗"
    column = get_lang('activity_type')
    rows = __activity_type_rows()

    calc_func = get_calc_func('sum')

    group = create_basic_group(title, column, rows, None, __in_activity_type_group_func, calc_func)
    group.sum_column = get_lang('calories')
    group.set_ytitle("千卡")
    
    return group

def create_activity_type_time_group():
    title = "三项耗时"
    column = get_lang('activity_type')
    rows = __activity_type_rows()

    calc_func = get_calc_func('sum')

    group = create_basic_group(title, column, rows, None, __in_activity_type_group_func, calc_func)
    group.sum_column = get_lang('time')
    group.set_ytitle("分钟")
    
    return group

def get_basic_groups() :
    return [
        create_activity_type_count_group(),
        create_activity_type_distance_group(),
        create_activity_type_time_group(),
        create_activity_type_calory_group()
    ]
