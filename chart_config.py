# encoding:utf-8
from pyecharts.commons import utils

__to_hms_formatter = utils.JsCode("""function (params) {
        seconds = params.value;
        arr = [0,0,0];
        arr[0] = Math.floor(seconds/3600);
        seconds %= 3600;
        arr[1] = Math.floor(seconds/60);
        arr[1] = ('0' + arr[1]).slice(-2);
        arr[2] = seconds % 60;
        arr[2] = ('0' + arr[2]).slice(-2);
        return arr.join(':')
    }
""")

__to_ms_formatter = utils.JsCode("""function (params) {
        seconds = params.value;
        mins = Math.floor(seconds/60);
        seconds = seconds % 60;
        seconds = ('0' + seconds).slice(-2);
        return mins + ':' + seconds
    }
""")

__chart_config = {
    'marathon':('全程马拉松', '>42公里的记录数量，统计范围2019-01-01～2021-12-31', 'distance', None, '{c} 次', None),
    'distance':('跑得远的', '3年累计跑量', 'distance', lambda x : int(x), '{c} 公里', None),
    'pace':('跑得快的', '平均配速 = 总时间 / 总距离，不包含越野', 'avg_pace', lambda x : x.total_seconds(), __to_ms_formatter, None),
    'time':('勤奋跑者 - 时间长', '3年累计跑步时长', 'time', lambda x : x.total_seconds(), __to_hms_formatter, None),  
    'days':('勤奋跑者 - 频率高', '有跑过步的天数', 'days', lambda x : int(x), '{c} 天', None),
    'cadence':('步子迈得快的', '平均步频', 'cadence', lambda x : int(x), '{c} 步/分', None),
    'stride':('步子跨得大的', '平均步幅', 'stride_len', lambda x : round(x, 2), '{c} 米', None),
    'month_distance_std':('月跑量平稳', '跑量波动 = 月跑量标准差 / 月平均跑量', 'distance', lambda x : round(x * 100, 2), '{c} %', None),
    'distance_std':('跑量平稳', '跑步距离波动 = 距离标准差 / 平均距离', 'distance', lambda x : round(x * 100, 2), '{c} %', None),
    'pace_std':('配速平稳', '配速波动 = 配速标准差 / 平均配速', 'pace_secs', lambda x : round(x * 100, 2), '{c} %', None),
    'every_week':('坚持得最好的', '没有哪一周不跑步的', 'distance', lambda x : int(x), '', 'word_cloud'),
    'pace_progress':('越跑越快的', '每年平均配速都有进步，年平均配速增长累计', 'pace_diff', lambda x : int(x), '{c} 秒', None)
}

class __Chart(object):
    pass

charts = {}

for key in __chart_config:
    items = __chart_config[key]
    c = __Chart()
    c.title = items[0]
    c.sub_title = items[1]
    c.value_column = items[2]
    c.value_func = items[3]
    c.formatter = items[4]
    c.chart_type = 'default' if items[5] is None else items[5]
    
    charts[key] = c