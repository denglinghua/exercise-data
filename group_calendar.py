import datetime
from re import I

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

def _activity_type_index(act_type):
    keywords = [lang.data__keyword_running, lang.data__keyword_swimming, lang.data__keyword_cycling]
    i = 0
    for key in keywords:
        if act_type.find(key) >= 0:
            return i
        i = i + 1
    return -1

def _agg_activity_type(group_set, group):
    flags = [0, 0, 0]
    for r in group.data_rows:
        act_type = r[lang.data__activity_type]
        act_index = _activity_type_index(act_type)
        if act_index >= 0:
            flags[act_index] = 1
    
    items = []
    for index, flag in enumerate(flags):
        if(flag == 1):
            items.append(index)
    
    return '|'.join(map(str, items))      

@check_data('data_rows_count')
def _activity_type_calendar_group_set():
    title = lang.activity_type_calendar
    column = lang.data__date

    group_set = GroupSet(title, column, ActivityTimeGroupByCalendar(2021), _agg_activity_type)
    group_set.chart_type = 'calendar'
    
    return group_set

def get_calendar_group_sets():
    return [
        _activity_time_calendar_group_set(),
        _activity_type_calendar_group_set()
    ]