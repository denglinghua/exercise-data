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
    'marathon':('全程马拉松', 'distance', None, '{c} 次'),
    'distance':('跑量', 'distance', lambda x : int(x), '{c} 公里'),
    'pace':('配速', 'avg_pace', lambda x : x.total_seconds(), __to_ms_formatter),
    'time':('跑步总时间', 'time', lambda x : x.total_seconds(), __to_hms_formatter),  
    'days':('跑步频次（天）', 'days', lambda x : int(x), '{c} 次'),
    'cadence':('步频', 'cadence', lambda x : int(x), '{c} 步/分'),
    'stride':('步幅', 'stride_len', lambda x : round(x, 2), '{c} 米'),
    'month_distance_std':('月跑量波动', 'distance', lambda x : round(x * 100, 2), '{c} %'),
    'pace_std':('配速波动', 'pace_secs', lambda x : round(x * 100, 2), '{c} %')
}

class __Charts(object):
    pass

class __Chart(object):
    pass

charts = __Charts()

for key in __chart_config:
    items = __chart_config[key]
    c = __Chart()
    c.title = items[0]
    c.value_column = items[1]
    c.value_func = items[2]
    c.formatter = items[3]
    setattr(charts, key, c)