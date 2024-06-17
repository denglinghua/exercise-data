from lang import lang
from core.group_by import GroupBy
from core.group import GroupSet

def _filter_activity_type(data_row, keyword):
    return data_row[lang.data__activity_type].find(keyword) >= 0

def is_running(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_running)

def is_swimming(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_swimming)

def is_cycling(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_cycling)

class ActivityTypeGroupBy(GroupBy):
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
        print(self.group_set.title + ': unknown activity type:' + val)
        return -1

def create_activity_type_group_set(title, column, agg_func, filter_func = None):
    group_set = GroupSet(title, column, ActivityTypeGroupBy(), agg_func, filter_func)
    return group_set

class MonthGroupBy(GroupBy):
    def __init__(self) -> None:
        super().__init__()

    def map_group_key(self, val):
        month = self.get_month(val)
        return month
    
    def get_month(self, val):
        return "{:04d}-{:02d}".format(val.tm_year, val.tm_mon)