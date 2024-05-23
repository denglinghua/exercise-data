import sys
import glob

from lang import set_lang
import data.csv_reader as csv_reader
from data.datasource import prehandle_data
from core.group import do_group, print_group_sets

from analysis.group_basic import get_basic_group_sets
from analysis.group_range import get_range_group_sets
from analysis.run_place import get_run_place_group_sets
from analysis.month_activity_freq import get_month_activity_freq_group_sets
from analysis.week_hour_activity import get_week_hour_activity_group_sets
from analysis.month_run_distance import get_month_run_distance_group_sets
from chart.charts import draw_groups_chart
from chart.test_charts import draw_groups_chart as draw_test_chart

data_dir = sys.argv[1]
set_lang(int(sys.argv[2]), int(sys.argv[3]))

files = glob.glob(data_dir + "/*_en.csv")
rows = []
for file in files:
    rows.extend(csv_reader.read_dict(file))
print("Read %d files, %d rows" % (len(files), len(rows)))
prehandle_data(rows)
group_sets = get_basic_group_sets() + get_range_group_sets() + get_run_place_group_sets()
group_sets += get_month_activity_freq_group_sets() + get_week_hour_activity_group_sets()
group_sets += get_month_run_distance_group_sets()
do_group(rows, group_sets)
print_group_sets(group_sets)    
draw_groups_chart("Triathlon execise data review", group_sets, rows)

draw_test_chart("Percent charts", group_sets)

# check group data is correct?
check_context = {}
check_context["data_rows_count"] = len(rows)
sum_group_set = group_sets[0]
check_context["activity_times"] = sum(map(lambda r : r.agg_value, sum_group_set.groups.values()))
check_context["run_times"] = sum_group_set.groups[0].agg_value
check_context["swim_times"] = sum_group_set.groups[1].agg_value
check_context["cycle_times"] = sum_group_set.groups[2].agg_value

for group_set in group_sets:
    group_set.check_data(check_context)
