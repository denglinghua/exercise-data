# encoding:utf-8
from group import Group, GroupRow, get_calc_func
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

def create_activity_type_times_group():
    title = "三项分别做了多少次"
    column = get_lang('activity_type')
    rows = __activity_type_rows()

    def in_this_group_func(
        data_row, group, group_row): return data_row[column].find(group_row.keyword) >= 0
    
    calc_func = get_calc_func("count")

    return create_basic_group(title, column, rows, None, in_this_group_func, calc_func).set_ytitle("次")

def create_activity_type_distance_group():
    title = "三项距离"
    column = get_lang('activity_type')
    rows = __activity_type_rows()

    def in_this_group_func(
        data_row, group, group_row): return data_row[column].find(group_row.keyword) >= 0
    
    def calc_func(group, group_row):
        val = sum(r[get_lang("distance")] for r in group_row.data_rows)
        if group_row.label =='游泳':
            val = val / 1000
        return int(val)

    group = create_basic_group(title, column, rows, None, in_this_group_func, calc_func)
    group.set_ytitle("km")
    
    return group

def get_basic_groups() :
    return [
        create_activity_type_times_group(),
        create_activity_type_distance_group()
    ]
