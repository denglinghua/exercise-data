from lang import lang
from core.group_by import GroupBy

def _filter_activity_type(data_row, keyword):
    return data_row[lang.data__activity_type].find(keyword) >= 0

def is_running(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_running)

def is_swimming(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_swimming)

def is_cycling(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_cycling)

class MonthGroupBy(GroupBy):
    def __init__(self) -> None:
        super().__init__()

    def map_group_key(self, val):
        month = self.get_month(val)
        return month
    
    def get_month(self, val):
        return "{:04d}-{:02d}".format(val.tm_year, val.tm_mon)