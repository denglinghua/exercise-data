from core.group import GroupSet, get_agg_func, check_data
from core.group_by import GroupBy
from lang import lang

class ActivityGroupBy(GroupBy):
    def __init__(self) -> None:
        super().__init__()
        self.create_groups([lang.running, lang.swimming, lang.cycling])
    
    def map_group_key(self, val):
        keywords = [lang.data__keyword_running, lang.data__keyword_swimming, lang.data__keyword_cycling]
        i = 0
        for key in keywords:
            if val.find(key) >= 0:
                return i
            i = i + 1
        print(self.group_set.title + ': unknown activity:' + val)
        return -1

def _basic_group_set(title, column, agg_func, filter_func = None):
    group_set = GroupSet(title, column, ActivityGroupBy(),
                         agg_func, filter_func)
    return group_set

@check_data('data_rows_count')
def _activity_type_count_group_set():
    title = lang.activities
    column = lang.data__activity_type

    agg_func = get_agg_func("count")

    return _basic_group_set(title, column, agg_func).set_ytitle(lang.activity_times)

@check_data('data_rows_count')
def _activity_type_distance_group_set():
    title = lang.total_distance
    column = lang.data__activity_type

    def agg_func(group, group_row):
        val = sum(r[lang.data__distance] for r in group_row.data_rows)
        if group_row.label == lang.swimming:
            #swimming unit is meter
            val = val / 1000
        return int(val)

    return _basic_group_set(title, column, agg_func).set_ytitle(lang.km)

@check_data('data_rows_count')
def _activity_type_calory_group_set():
    title = lang.activity_calories
    column = lang.data__activity_type

    agg_func = get_agg_func('sum')

    group_set = _basic_group_set(title, column, agg_func)
    group_set.sum_column = lang.data__calories
    group_set.set_ytitle(lang.kcal)

    return group_set

@check_data('data_rows_count')
def _activity_type_time_group_set():
    title = 'Exercise Time Breakdown'
    column = lang.data__activity_type

    agg_func = get_agg_func('sum')

    group_set = _basic_group_set(title, column, agg_func)
    group_set.chart_type = 'pie'
    group_set.sum_column = lang.data__time

    return group_set

def get_basic_group_sets():
    return [
        _activity_type_count_group_set(),
        _activity_type_distance_group_set(),
        _activity_type_time_group_set(),
        _activity_type_calory_group_set()
    ]
