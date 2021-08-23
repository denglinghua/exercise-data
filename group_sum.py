# encoding:utf-8
from group import Group, GroupRow
from lang import get_lang

def create_sum_group(title, column, rows, filter_func, in_this_group_func):
    group_rows = []
    for r in rows:
        group_row = GroupRow(r[0])
        group_row.keyword = r[1]
        group_rows.append(group_row)
        
    group = Group(title, column, group_rows, filter_func, in_this_group_func)
    return group

def create_activity_type_group():
    title = "三项分别做了多少"
    column = get_lang('activity_type')
    rows = [
        ("跑步", get_lang('running')),
        ("游泳", get_lang('swimming')),
        ("自行车", get_lang('cycling'))
    ]

    def in_this_group_func(
        data_row, group, group_row): return data_row[group.column].find(group_row.keyword) >= 0

    return create_sum_group(title, column, rows, None, in_this_group_func)

def get_sum_groups() :
    return [
        create_activity_type_group()
    ]
