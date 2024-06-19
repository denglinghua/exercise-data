from core.group import GroupSet, get_agg_func, check_data
from core.group_by import GroupBy
from analysis.common import is_running
from lang import lang

class RunPlaceGroupBy(GroupBy):
    def __init__(self) -> None:
        super().__init__()
        self.place_en_names = self.create_place_en_names()

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
        t = self.merge_place(t)
        t= self.place_en_name(t)
        
        return t
    
    def place_en_name(self, place):
        return self.place_en_names[place] if place in self.place_en_names else place
    
    def create_place_en_names(self):
        map = {
            '珠江公园': 'Pearl River Park',
            '生物岛': 'Biology Island',
            '江边': 'River Side',
            '奥体': 'Olympic Center',
            '深圳': 'Shenzhen',
            '大学城': 'University Town',
            '广东-惠州': 'Huizhou',
            '北京-玉渊潭': 'Beijing',
            '广东-英德': 'Yingde',
            '广西-阳朔': 'Yangshuo',
            '旭景': 'Xujing',
            '天鹿山': 'Tianlu Mountain',
            '贵州-贵阳': 'Guiyang',
            '大夫山': 'Dafu Mountain',
            '海珠湖': 'Haizhu Lake',
            '珠江新城': 'Zhujiang Town',
            '华农': 'SCA University',
            '广东-清远': 'Qingyuan',
            '天体': 'Tianti',
            '二沙岛': 'Ersha Island',
            '湖北-京山': 'Jingshan',
            '香港': 'Hong Kong',
            '广东-佛山': 'Foshan',
            '海南-万宁': 'Wanning',
            '海南-琼海': 'Qionghai',
            '海南-文昌': 'Wenchang',
            '车陂涌': 'CheBeiYong',
            '南沙': 'Nansha',
            '陕西-西安': 'XiAn',
            '湖北-武汉': 'Wuhan',
            '白水寨': 'Baishuizhai',
            '广东-东莞': 'Dongguan',
            '黄埔': 'Huangpu',
            '广西-桂林': 'Guilin',
            '暨大': 'JiDa',
            '重庆': 'Chongqing',
            '长沙-橘子洲头': 'Changsha',
            '花都': 'Huadu',
            '天河公园': 'Tianhe Park',
            '大沙地': 'Dashadi',
            '佛山-南海': 'Nanhai',
            '广东-顺德': 'Shunde',
            '海南-三亚': 'Sanya',
            '海南-陵水': 'Lingshui',
            '海南-保亭': 'Baoting',
            '大观湿地公园': 'Daguan Wetland Park',
            '河北-张家口': 'Zhangjiakou',
            '油麻山': 'Youma Mountain',
            '岭头村水库': 'Lingtou Village',
            '龙凤火': 'Longfenghuo',
        }
        
        return map
        
@check_data('run_times')
def _run_place_group_set():
    title = lang.run_place
    column = 'Title'

    agg_func = get_agg_func("count")

    group_set = GroupSet(title, column, RunPlaceGroupBy(), agg_func, is_running)
    group_set.name = 'run_place'
    group_set.chart_type = 'wordcloud'
    
    return group_set

def group_sets():
    return [
        _run_place_group_set(),
    ]