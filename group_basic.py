from group import Group, GroupSet, get_agg_func, check_data
from group_by import GroupBy
from lang import lang


class ActivityGroupBy(GroupBy):
    def __init__(self) -> None:
        super().__init__()
        self.create_groups([lang.running, lang.swimming, lang.cycling])

    def map_group(self, val) -> int:
        keywords = [lang.running, lang.swimming, lang.cycling_keyword]
        i = 0
        for key in keywords:
            if val.find(key) >= 0:
                return i
            i = i + 1
        print(self.group_set.title + ': unknown activity:' + val)
        return -1


def __basic_group_set(title, column, agg_func, filter_func = None):
    group_set = GroupSet(title, column, ActivityGroupBy(),
                         agg_func, filter_func)
    return group_set


@check_data(lambda ctx, total: total == ctx['data_rows_count'])
def __activity_type_count_group_set():
    title = lang.activities
    column = lang.col_activity_type

    agg_func = get_agg_func("count")

    group_set = __basic_group_set(title, column, agg_func)
    group_set.set_ytitle(lang.activity_times)

    return group_set


def __activity_type_distance_group_set():
    title = lang.total_distance
    column = lang.col_activity_type

    def agg_func(group, group_row):
        val = sum(r[lang.col_distance] for r in group_row.data_rows)
        if group_row.label == lang.swimming:
            val = val / 1000
        return int(val)

    group_set = __basic_group_set(title, column, agg_func)
    group_set.set_ytitle(lang.km)

    return group_set


def __activity_type_calory_group_set():
    title = lang.activity_calories
    column = lang.col_activity_type

    agg_func = get_agg_func('sum')

    group_set = __basic_group_set(title, column, agg_func)
    group_set.sum_column = lang.col_calories
    group_set.set_ytitle(lang.kcal)

    return group_set


def __activity_type_time_group_set():
    title = lang.total_activity_time
    column = lang.col_activity_type

    agg_func = get_agg_func('sum')

    group_set = __basic_group_set(title, column, agg_func)
    group_set.sum_column = lang.col_time

    return group_set


def get_basic_group_sets():
    return [
        __activity_type_count_group_set(),
        __activity_type_distance_group_set(),
        __activity_type_time_group_set(),
        __activity_type_calory_group_set()
    ]
