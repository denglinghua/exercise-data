from core.group import GroupSet, get_agg_func, check_data
from core.group_by import GroupBy
from analysis.common import create_activity_type_group_set
from lang import lang

@check_data('data_rows_count')
def _activity_type_count_group_set():
    title = lang.activities
    column = lang.data__activity_type

    agg_func = get_agg_func("count")

    return create_activity_type_group_set(title, column, agg_func).set_ytitle(lang.activity_times)

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

    return create_activity_type_group_set(title, column, agg_func).set_ytitle(lang.km)

@check_data('data_rows_count')
def _activity_type_calory_group_set():
    title = lang.activity_calories
    column = lang.data__activity_type

    agg_func = get_agg_func('sum')

    group_set = create_activity_type_group_set(title, column, agg_func)
    group_set.sum_column = lang.data__calories
    group_set.set_ytitle(lang.kcal)

    return group_set

def group_sets():
    return [
        _activity_type_count_group_set(),
        _activity_type_distance_group_set(),
        _activity_type_calory_group_set()
    ]
