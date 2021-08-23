import time

def __do_group_row(data_row, group):
    if group.filter_func and not group.filter_func(data_row):
        return
    for group_row in group.rows:
        if (group.in_this_group_func(data_row, group, group_row)):
            group_row.count = group_row.count + 1
            break

def do_group(data_rows, groups):
    for data_row in data_rows:
        for group in groups:
            __do_group_row(data_row, group)

def print_groups(groups):
    for group in groups:
        print(group)
        print('\n')

class GroupRow(object):
    def __init__(self, label):
        self.label = label
        self.count = 0
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{%s : %s}' % (self.label, self.count)

class Group(object):
    def __init__(self, title, column, rows, filter_func, in_this_group_func):
        self.title = title
        self.column = column
        self.rows = rows
        self.filter_func = filter_func
        self.in_this_group_func = in_this_group_func
    
    def __str__(self):
        return '{%s, %s, %s}' % (self.title, self.column, self.rows)
    
    def get_axis_values(self):
        xlist = []
        ylist = []
        for row in self.rows:
            if (row.count > 0):
                xlist.append(row.label)
                ylist.append(row.count)
        
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