import csv
from group import do_group, print_groups
from group_range import create_activity_hour_group, create_activity_month_group, create_avg_pace_group, create_avg_run_distance_group
from group_sum import create_activity_type_group
from charts import draw_group_chart

with open('Activities.csv', 'rt') as f:
    rows = list(csv.DictReader(f))
    groups = [create_activity_type_group(),
              create_activity_hour_group(),
              create_avg_pace_group(),
              create_avg_run_distance_group(),
              create_activity_month_group()]

    do_group(rows, groups)
    print_groups(groups)
    
    for group in groups:
        draw_group_chart(group)
