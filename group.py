import time

def __do_group_row(data_row, group):
    if group.filter_func and not group.filter_func(data_row):
        return
    for group_row in group.rows:
        if (group.in_this_group_func(data_row, group, group_row)):
            group_row.data_rows.append(data_row)
            break

def do_group(data_rows, groups):
    for data_row in data_rows:
        for group in groups:
            __do_group_row(data_row, group)
    
    for group in groups:
        for row in group.rows:
            group.calc_func(row)

def print_groups(groups):
    for group in groups:
        print(group)
        print('\n')

class GroupRow(object):
    def __init__(self, label):
        self.label = label
        self.data_rows = []
        self.value = 0
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{%s : %s}' % (self.label, self.value)

class Group(object):
    def __init__(self, title, column, rows, in_this_group_func, calc_func, filter_func = None):
        self.title = title
        self.column = column
        self.rows = rows
        self.filter_func = filter_func
        self.in_this_group_func = in_this_group_func
        self.calc_func = calc_func
    
    def __str__(self):
        return '{%s, %s, %s}' % (self.title, self.column, self.rows)
    
    def get_axis_values(self):
        xlist = []
        ylist = []
        for row in self.rows:
            if (row.value > 0):
                xlist.append(row.label)
                ylist.append(row.value)
        
        return [xlist, ylist]

def str_to_time(str):
    strlen = len(str)
    format = ''
    if (strlen > 10):
        format = '%Y-%m-%d %H:%M:%S'
    elif (strlen > 6):
        format = '%H:%M:%S'
    else:
        format = '%M:%S'
    
    return time.strptime(str, format)

def __calc_count_func(group_row):
    group_row.value = len(group_row.data_rows)

def __calc_avg_func(group_row):
    group_row.value = 0

def get_calc_func(func_name):
    if func_name == "count":
        return __calc_count_func
    if func_name == "avg":
        return __calc_avg_func
    return None


