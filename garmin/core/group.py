from functools import wraps

def _do_group_row(data_row, group_set):
    if group_set.filter_func and not group_set.filter_func(data_row):
        return
    
    group_value = data_row[group_set.group_by_column]
    value_func = group_set.group_by.value_func
    if value_func:
        group_value = value_func(group_value)
    
    group_key = group_set.group_by.map_group_key(group_value)
    group = group_set.groups.get(group_key)
    if group is None and not group_set.fixed:
        group = Group(group_key)
        group_set.groups[group_key] = group
    if group:
        group.data_rows.append(data_row)
    else:
        print('[%s:%s:%s] can not map to a group' % (group_set.title, group_value, group_key))


def do_group(data_rows, group_sets):
    for data_row in data_rows:
        for group_set in group_sets:
            _do_group_row(data_row, group_set)
    
    for group_set in group_sets:
        for group in group_set.groups.values():
            group.agg_value = group_set.agg_func(group_set, group)

def print_group_sets(group_sets):
    for group_set in group_sets:
        print(group_set)
        print('\n')

class Group(object):
    def __init__(self, label):
        self.label = label
        self.data_rows = []
        self.agg_value = None
    
    def row_count(self):
        return len(self.data_rows)
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{%s : %s}' % (self.label, self.agg_value)

class GroupSet(object):
    def __init__(self, title, group_by_column, group_by, agg_func, filter_func = None):
        self.name = None
        self.title = title
        self.xtitle = None
        self.ytitle = None
        self.chart_type = 'bar'
        self.group_by_column = group_by_column
        self.group_by = group_by.set_group_set(self)
        self.groups = group_by.groups or {}
        self.fixed = len(self.groups.values()) > 0
        self.filter_func = filter_func
        self.agg_func = agg_func
        self.check_data_item = None
        self.json = None
    
    def __str__(self):
        return '{%s, %s, %s}' % (self.title, self.group_by_column, self.groups.values())
    
    def set_xtitle(self, title):
        self.xtitle = title
        return self
    
    def set_ytitle(self, title):
        self.ytitle = title
        return self
    
    def set_chart_type(self, chart_type):
        self.chart_type = chart_type
        return self

    @staticmethod
    def check_num(var):
        return isinstance(var, int) or isinstance(var, float)

    def get_axis_values(self, drop_zero = True, x_sort = False):
        xlist = []
        ylist = []

        keys = self.groups.keys()
        if x_sort:
            keys = sorted(keys)

        for key in keys:
            group = self.groups[key]
            if not self.check_num(group.agg_value) or not drop_zero or group.agg_value > 0:
                xlist.append(group.label)
                ylist.append(group.agg_value)
        return [xlist, ylist]
    
    def get_json(self):
        series = []
        for group in self.groups.values():
            series.append([group.label, group.agg_value])
        return {
            'title': self.title,
            'series': series
        }
        
    # for data correctness check
    def check_data(self, context):      
        if self.check_data_item:
            total = sum(map(lambda g : g.row_count(), self.groups.values()))
            exp_val = context[self.check_data_item]
            if (exp_val == total):
                print('O check OK %s' % self.title)
            else:
                print('X check FAILED %s (%s)' % (self.title, total - exp_val))
        else:
            print('- check no function %s' % self.title)

def _agg_count_func(group_set, group):
    return len(group.data_rows)

def _agg_sum_func(group_set, group):
    return sum(r[group_set.sum_column] for r in group.data_rows)

def _agg_avg_func(group_set, group):
    # TODO
    return 0

def get_agg_func(func_name):
    if func_name == "count":
        return _agg_count_func
    if func_name == "sum":
        return _agg_sum_func
    if func_name == "avg":
        return _agg_avg_func
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
