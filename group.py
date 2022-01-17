import time
from functools import wraps

def __do_group_row(data_row, group_set):
    if group_set.filter_func and not group_set.filter_func(data_row):
        return
    
    group_value = data_row[group_set.group_by_column]
    value_func = group_set.group_by.value_func
    if value_func:
        group_value = value_func(group_value)
    
    group_index = group_set.group_by.map_group(group_value)
    if group_index >= 0 and group_index < len(group_set.groups):
        group = group_set.groups[group_index]
        group.data_rows.append(data_row)
    else:
        print('%s, %s group index out of range' % (group_set.title, group_index))


def do_group(data_rows, group_sets):
    for data_row in data_rows:
        for group_set in group_sets:
            __do_group_row(data_row, group_set)
    
    for group_set in group_sets:
        for group in group_set.groups:
            group.agg_value = group_set.agg_func(group_set, group)

def print_group_sets(group_sets):
    for group_set in group_sets:
        print(group_set)
        print('\n')

class Group(object):
    def __init__(self, label):
        self.label = label
        self.data_rows = []
        self.agg_value = 0
    
    def row_count(self):
        return len(self.data_rows)
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{%s : %s}' % (self.label, self.agg_value)

class GroupSet(object):
    def __init__(self, title, group_by_column, group_by, agg_func, filter_func = None):
        self.title = title
        self.xtitle = None
        self.ytitle = None
        self.chart_type = 'bar'
        self.group_by_column = group_by_column
        self.group_by = group_by.set_group_set(self)
        self.groups = group_by.groups
        self.filter_func = filter_func
        self.agg_func = agg_func
        self.check_data_item = None
    
    def __str__(self):
        return '{%s, %s, %s}' % (self.title, self.group_by_column, self.groups)
    
    def set_xtitle(self, title):
        self.xtitle = title
        return self
    
    def set_ytitle(self, title):
        self.ytitle = title
        return self
    
    def set_chart_type(self, chart_type):
        self.chart_type = chart_type
        return self

    def get_axis_values(self, drop_zero = True):
        xlist = []
        ylist = []
        for group in self.groups:
            if not drop_zero or group.agg_value > 0:
                xlist.append(group.label)
                ylist.append(group.agg_value)
        
        return [xlist, ylist]
    
    # for data correctness check
    def check_data(self, context):      
        if self.check_data_item:
            total = sum(map(lambda g : g.row_count(), self.groups))
            exp_val = context[self.check_data_item]
            if (exp_val == total):
                print('O check OK %s' % self.title)
            else:
                print('X check FAILED %s (%s)' % (self.title, total - exp_val))
        else:
            print('- check no function %s' % self.title)

def __agg_count_func(group_set, group):
    return len(group.data_rows)

def __agg_sum_func(group_set, group):
    return sum(r[group_set.sum_column] for r in group.data_rows)

def __agg_avg_func(group_set, group):
    return 0

def get_agg_func(func_name):
    if func_name == "count":
        return __agg_count_func
    if func_name == "sum":
        return __agg_sum_func
    if func_name == "avg":
        return __agg_avg_func
    return None

def check_data(check_data_item):
    def check_data_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):            
            group_set = func(*args, **kwargs)
            group_set.check_data_item = check_data_item
            return group_set
        return wrapped_function
    return check_data_decorator
