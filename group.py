import time
from functools import wraps

def __do_group_row(data_row, group_set):
    if group_set.filter_func and not group_set.filter_func(data_row):
        return
    for group in group_set.groups:
        if (group_set.in_this_group_func(data_row, group_set, group)):
            group.data_rows.append(data_row)
            break

def do_group(data_rows, group_sets):
    for data_row in data_rows:
        for group_set in group_sets:
            __do_group_row(data_row, group_set)
    
    for group_set in group_sets:
        for group in group_set.groups:
            group.value = group_set.calc_func(group_set, group)

def print_group_sets(group_sets):
    for group_set in group_sets:
        print(group_set)
        print('\n')

class Group(object):
    def __init__(self, label):
        self.label = label
        self.data_rows = []
        self.value = 0
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{%s : %s}' % (self.label, self.value)

class GroupSet(object):
    #export_groups = []
    #@staticmethod
    #def export(fn):
    #    Group.export_groups.append((fn, fn.__name__))

    def __init__(self, title, group_by_column, groups, in_this_group_func, calc_func, filter_func = None):
        self.title = title
        self.xtitle = None
        self.ytitle = None
        self.group_by_column = group_by_column
        self.groups = groups
        self.filter_func = filter_func
        self.in_this_group_func = in_this_group_func
        self.calc_func = calc_func
        self.check_data_func = None
    
    def __str__(self):
        return '{%s, %s, %s}' % (self.title, self.group_by_column, self.groups)
    
    def set_xtitle(self, title):
        self.xtitle = title
        return self
    
    def set_ytitle(self, title):
        self.ytitle = title
        return self

    def get_axis_values(self):
        xlist = []
        ylist = []
        for group in self.groups:
            if (group.value > 0):
                xlist.append(group.label)
                ylist.append(group.value)
        
        return [xlist, ylist]
    
    # for data correctness check
    def check_data(self, context):      
        if self.check_data_func:
            total = sum(map(lambda g : g.value, self.groups))
            if (self.check_data_func(context, total)):
                print('O check OK %s' % self.title)
            else:
                print('X check FAILED %s' % self.title)
        else:
            print('- check no function %s' % self.title)

def __calc_count_func(group_set, group):
    return len(group.data_rows)

def __calc_sum_func(group_set, group):
    return sum(r[group_set.sum_column] for r in group.data_rows)

def __calc_avg_func(group_set, group):
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
            group_set = func(*args, **kwargs)
            group_set.check_data_func = check_data_func
            return group_set
        return wrapped_function
    return check_data_decorator

def create_series(start, end, step=1, format='%s', list = None):
    series = [("<" + format % start, 0, start)]
    def map_func(n):
        s = n
        e = n + step
        label = '%s-%s' % (format % s, format % e)
        return (label, s, e)
    if list:
        series.extend(map(map_func, list))
    else:
        series.extend(map(map_func, range(start, end, step)))
    series.append((">=" + format % end, end, 9999999))
    return series
