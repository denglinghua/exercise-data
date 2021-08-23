# encoding:utf-8
__cur_lang = 0
__lang_dict = {
    'activity_type':('Activity Type', '活动类型'),
    'running':('Running', '跑步'),
    'swimming':('Swimming','游泳'),
    'cycling':('Cycling','骑行'),
    'avg_pace':('Avg Pace', '平均配速'),
    'date':('Date', '日期'),
    'distance':('Distance', '距离')
}

def get_lang(key):
    return __lang_dict[key][__cur_lang]

def set_lang(lang_index):
    global __cur_lang
    __cur_lang = lang_index