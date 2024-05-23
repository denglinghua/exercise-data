from core.group import GroupSet, check_data
from analysis.common import is_running, is_swimming, is_cycling, MonthGroupBy
from lang import lang

@check_data('data_rows_count')
def _month_activity_freq_group_set():
    title = 'Monthly Breakdown of Exercise Sessions'
    column = lang.data__date

    group_set = GroupSet(title, column, MonthGroupBy(), __agg_month_activity)
    group_set.chart_type = 'stacked_line'

    return group_set

def __agg_month_activity(group_set, group):
    result = [0, 0, 0]
    for row in group.data_rows:
        if is_running(row):
            result[0] += 1
        elif is_swimming(row):
            result[1] += 1
        elif is_cycling(row):
            result[2] += 1
    
    return result

def get_month_activity_freq_group_sets():
    return [
        _month_activity_freq_group_set(),
    ]