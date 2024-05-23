from core.group import GroupSet, get_agg_func, check_data
from core.group_by import GroupBy
from lang import lang

class RunPlaceGroupBy(GroupBy):
    def __init__(self) -> None:
        super().__init__()

    def map_group_key(self, val):
        p = self.extract_run_place(val)
        return p
    
    def merge_place(self, place):
        p = place.replace('广州-', '')
        if ('深圳' in place):
            p = '深圳'
        return p

    def extract_run_place(self, title):
        t = title.replace('-Manual', '')
        items = t.split('-')
        ilen = len(items)
        t = ''               
        if ilen > 2:
            t = '-'.join(items[:2])
        elif ilen == 2:
            t = items[0]
        else:
            t = items[0].split(' Running')[0]
        
        #print(title, '-->', t)
        return self.merge_place(t)

@check_data('run_times')
def _run_place_group_set():
    title = lang.run_place
    column = 'Title'

    agg_func = get_agg_func("count")

    group_set = GroupSet(title, column, RunPlaceGroupBy(), agg_func, _filter_running_func)
    group_set.chart_type = 'wordcloud'
    
    return group_set

def _filter_running_func(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_running)

def _filter_activity_type(data_row, keyword):
    return data_row[lang.data__activity_type].find(keyword) >= 0

def get_run_place_group_sets():
    return [
        _run_place_group_set(),
    ]