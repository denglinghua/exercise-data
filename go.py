import csv
from group import do_group, print_groups
from group_sum import sum_groups
from group_range import range_groups
from charts import draw_groups_chart

with open('Activities.csv', 'rt') as f:
    rows = list(csv.DictReader(f))
    groups = sum_groups + range_groups
    do_group(rows, groups)
    print_groups(groups)    
    draw_groups_chart(groups)
