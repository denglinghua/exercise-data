from core.group import GroupSet, get_agg_func, check_data
from analysis.common import is_running, MonthGroupBy
from lang import lang

@check_data('run_times')
def _month_run_distance_group_set():
    title = 'Monthly Running Distance Sum'
    column = lang.data__date

    agg_func = get_agg_func("sum")

    group_set = GroupSet(title, column, MonthGroupBy(), agg_func, is_running)
    group_set.sum_column = lang.data__distance
    group_set.chart_type = 'line'

    return group_set

def group_sets():
    return [
        _month_run_distance_group_set(),
    ]