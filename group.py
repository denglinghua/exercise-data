import time
from functools import wraps

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
            row.value = group.calc_func(group, row)

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
    #export_groups = []
    #@staticmethod
    #def export(fn):
    #    Group.export_groups.append((fn, fn.__name__))

    def __init__(self, title, column, rows, in_this_group_func, calc_func, filter_func = None):
        self.title = title
        self.xtitle = None
        self.ytitle = None
        self.column = column
        self.rows = rows
        self.filter_func = filter_func
        self.in_this_group_func = in_this_group_func
        self.calc_func = calc_func
        self.check_data_func = None
    
    def __str__(self):
        return '{%s, %s, %s}' % (self.title, self.column, self.rows)
    
    def set_xtitle(self, title):
        self.xtitle = title
        return self
    
    def set_ytitle(self, title):
        self.ytitle = title
        return self

    def get_axis_values(self):
        xlist = []
        ylist = []
        for row in self.rows:
            if (row.value > 0):
                xlist.append(row.label)
                ylist.append(row.value)
        
        return [xlist, ylist]
    
    # for data correctness check
    def check_data(self, context):      
        if self.check_data_func:
            total = sum(map(lambda r : r.value, self.rows))
            if (self.check_data_func(context, total)):
                print('O check OK %s' % self.title)
            else:
                print('X check FAILED %s' % self.title)
        else:
            print('- check no function %s' % self.title)

def __calc_count_func(group, group_row):
    return len(group_row.data_rows)

def __calc_sum_func(group, group_row):
    return sum(r[group.sum_column] for r in group_row.data_rows)

def __calc_avg_func(group, group_row):
    return 0

def get_calc_func(func_name):
    if func_name == "count":
        return __calc_count_func
    if func_name == "sum":
        return __calc_sum_func
    if func_name == "avg":
        return __calc_avg_func
    return None

def check_data(check_data_func):
    def check_data_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):            
            group = func(*args, **kwargs)
            group.check_data_func = check_data_func
            return group
        return wrapped_function
    return check_data_decorator
