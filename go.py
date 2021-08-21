import csv
from group import do_group
from group_range import create_activity_hour_group, create_activity_month_group, create_avg_pace_group, create_avg_run_distance_group
from group_sum import create_activity_type_group

with open('Activities.csv', 'rt') as f:
    rows = list(csv.DictReader(f))
    groups = [create_activity_type_group(),
              create_activity_hour_group(),
              create_avg_pace_group(),
              create_avg_run_distance_group(),
              create_activity_month_group()]

    for group in groups:
        do_group(rows, group)
