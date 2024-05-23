from core.group import GroupSet, get_agg_func, check_data
from core.group_by import GroupBy
from lang import lang

class WeekhourGroupBy(GroupBy):
    def __init__(self) -> None:
        super().__init__()
        ws = range(0, 7)
        hr = range(0, 24)
        values = []
        for w in ws:
            for h in hr:
                values.append("{:d}-{:d}".format(w, h))
        self.create_groups(values, group_key_stragety='dict')

    def map_group_key(self, val):
        w = val.tm_wday
        h = val.tm_hour
        key = "{:d}-{:d}".format(w, h)
        return key

@check_data('data_rows_count')
def _week_hour_activity_group_set():
    title = 'Exercise Routine'
    column = lang.data__date

    agg_func = get_agg_func("count")

    group_set = GroupSet(title, column, WeekhourGroupBy(), agg_func)
    group_set.chart_type = 'heatmap'

    return group_set

def get_week_hour_activity_group_sets():
    return [
        _week_hour_activity_group_set(),
    ]