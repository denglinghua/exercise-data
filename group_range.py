from group import Group, GroupRow, str_to_time

def in_range_group_func(data_row, group, group_row):
    val = group.value_func(data_row[group.column])
    return val >= group_row.low and val < group_row.up

def create_range_group(column, rows, filter_func, value_func):
    group_rows = []
    for row in rows:
        group_row = GroupRow(row[0])
        group_row.low = row[1]
        group_row.up = row[2]
        group_rows.append(group_row)

    in_this_group_func = in_range_group_func

    group = Group(column, group_rows, filter_func, in_this_group_func)
    group.value_func = value_func

    return group

def create_avg_pace_group():
    col = 'Avg Pace'
    rows = [
        ("<4:00", 1, 4),
        ("4-5:00", 4, 5),
        ("5-6:00", 5, 6),
        ("6-7:00", 6, 7),
        ("7-8:00", 7, 8),
        ("8-9:00", 8, 9),
        (">9:00", 9, 999)
    ]
    def filter_func(data_row): return data_row['Activity Type'].find('Running') >= 0

    def value_func(val): return str_to_time(val).tm_min

    return create_range_group(col, rows, filter_func, value_func)

def create_activity_hour_group():
    col = 'Date'
    rows = []
    for h in range(0, 24):
        rows.append((str(h) + "H", h, h+1))

    def value_func(val): return str_to_time(val).tm_hour

    return create_range_group(col, rows, None, value_func)

def create_activity_month_group():
    col = 'Date'
    rows = []
    for m in range(1, 13):
        rows.append((str(m) + "M", m, m+1))

    def value_func(val): return str_to_time(val).tm_mon

    return create_range_group(col, rows, None, value_func)

def create_avg_run_distance_group():
    col = 'Distance'
    rows = []
    for d in range(0, 20):
        start = d * 5
        end = start + 5
        rows.append((str(start) + '-' + str(end), start, end))
    def filter_func(data_row): return data_row['Activity Type'].find('Running') >= 0

    def value_func(val): return float(val)

    return create_range_group(col, rows, filter_func, value_func)

