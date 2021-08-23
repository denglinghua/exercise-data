import sys
import csv
from group import do_group, print_groups
from group_sum import get_sum_groups
from group_range import get_range_groups
from charts import draw_groups_chart
from lang import set_lang

data_file = sys.argv[1]
set_lang(int(sys.argv[2]))

with open(data_file, 'rt', encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
    groups = get_sum_groups() + get_range_groups()
    do_group(rows, groups)
    print_groups(groups)    
    draw_groups_chart("Triathlon execise data review", groups)
