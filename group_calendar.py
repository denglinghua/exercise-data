import datetime

from group import Group, GroupSet, get_agg_func, check_data
from group_by import GroupBy
from lang import lang

def _gen_year_days(year):
    begin = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    return [str(begin + datetime.timedelta(days=i)) for i in range((end - begin).days + 1)]

class ActivityTimeGroupByCalendar(GroupBy):
    def __init__(self, year) -> None:
        super().__init__()
        self.start_date = datetime.date(year, 1, 1)
        self.create_groups(_gen_year_days(year))

    def map_group(self, val) -> int:
        return (datetime.date(val.tm_year, val.tm_mon, val.tm_mday) - self.start_date).days

@check_data('data_rows_count')
def _activity_time_calendar_group_set():
    title = lang.activity_time_calendar
    column = lang.data__date

    agg_func = get_agg_func("sum")

    group_set = GroupSet(title, column, ActivityTimeGroupByCalendar(2021), agg_func)
    group_set.sum_column = lang.data__time
    group_set.chart_type = 'calendar'
    
    return group_set

def get_calendar_group_sets():
    return [
        _activity_time_calendar_group_set(),
    ]