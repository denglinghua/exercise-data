from core.group import GroupSet, get_agg_func, check_data
from core.group_by import GroupBy
from analysis.common import create_activity_type_group_set
from lang import lang

@check_data('activity_times')
def _activity_type_time_group_set():
    title = 'Exercise Time Breakdown'
    column = lang.data__activity_type

    agg_func = get_agg_func('sum')

    group_set = create_activity_type_group_set(title, column, agg_func)
    group_set.name = 'activity_type_time'
    group_set.chart_type = 'pie'
    group_set.sum_column = lang.data__time

    return group_set

def group_sets():
    return [
        _activity_type_time_group_set()
    ]