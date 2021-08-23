# encoding:utf-8
from group import Group, GroupRow

def create_sum_group(title, column, rows, filter_func, in_this_group_func):
    group = Group(title, column, rows, filter_func, in_this_group_func)
    return group

def create_activity_type_group():
    title = "三项分别做了多少"
    column = 'Activity Type'
    rows = [
        GroupRow('Running'),
        GroupRow('Swimming'),
        GroupRow('Cycling')
    ]

    def in_this_group_func(
        data_row, group, group_row): return data_row[group.column].find(group_row.label) >= 0

    return create_sum_group(title, column, rows, None, in_this_group_func)

sum_groups = [
    create_activity_type_group()
]
