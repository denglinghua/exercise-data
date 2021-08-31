import sys
import csv
from lang import set_lang
from group import do_group, print_groups
from group_basic import get_basic_groups
from group_range import get_range_groups
from charts import draw_groups_chart
from datasource import prehandle_data

data_file = sys.argv[1]
set_lang(int(sys.argv[2]))

with open(data_file, 'rt', encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
    prehandle_data(rows)
    groups = get_basic_groups() + get_range_groups()
    do_group(rows, groups)
    print_groups(groups)    
    draw_groups_chart("Triathlon execise data review", groups)

    # check group data is correct?
    check_context = {}
    check_context["data_rows_count"] = len(rows)
    sum_group = groups[0]
    check_context["activity_times"] = sum(map(lambda r : r.value, sum_group.rows))
    check_context["run_times"] = sum_group.rows[0].value
    check_context["swim_times"] = sum_group.rows[1].value
    check_context["cycle_times"] = sum_group.rows[2].value
    for group in groups:
        group.check_data(check_context)
