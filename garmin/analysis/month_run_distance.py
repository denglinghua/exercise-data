from core.group import GroupSet, get_agg_func, check_data
from analysis.common import is_running, MonthGroupBy
from lang import lang
from data import data2json

@check_data('run_times')
def _month_run_distance_group_set():
    title = 'Monthly Running Distance'
    column = lang.data__date

    agg_func = get_agg_func("sum")

    group_set = GroupSet(title, column, MonthGroupBy(), agg_func, is_running)
    group_set.name = 'month_run_distance'
    group_set.sum_column = lang.data__distance
    group_set.chart_type = 'line'

    group_set.json = lambda group_set: data2json.xy_to_json(group_set.title, group_set.get_axis_values(False, True))

    return group_set

def group_sets():
    return [
        _month_run_distance_group_set(),
    ]