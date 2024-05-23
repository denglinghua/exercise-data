import sys

from lang import set_lang
import data.csv_reader as csv_reader
from data import data_source
from core.group import do_group, print_group_sets

from analysis import group_basic
from analysis.group_range import get_range_group_sets
from analysis import activitiy_type_time, run_place, month_activity_freq, week_hour_activity, month_run_distance
from chart.charts import draw_groups_chart
from chart.test_charts import draw_groups_chart as draw_test_chart

data_dir = sys.argv[1]
set_lang(int(sys.argv[2]), int(sys.argv[3]))

rows = data_source.load_data(data_dir)

group_sets = [] # group_basic.group_sets() + get_range_group_sets()
group_sets += activitiy_type_time.group_sets()
group_sets += run_place.group_sets()
group_sets += month_activity_freq.group_sets()
group_sets += week_hour_activity.group_sets()
group_sets += month_run_distance.group_sets()

do_group(rows, group_sets)
print_group_sets(group_sets)    
draw_groups_chart("Triathlon execise data review", group_sets, rows)

draw_test_chart("Percent charts", group_sets)

# check group data is correct?
check_context = {}
check_context["data_rows_count"] = len(rows)
check_context["activity_times"] = len(rows)
check_context["run_times"] = data_source.running_activities
check_context["swim_times"] = data_source.swimming_activities
check_context["cycle_times"] = data_source.cycling_activities

for group_set in group_sets:
    group_set.check_data(check_context)
