import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, Grid, Page
from pyecharts.globals import ThemeType, SymbolType
from pyecharts.commons import utils

from datasource import user_id_to_name

class ChartData(object):
    def __init__(self, items):
        self.title = items[0]
        self.sub_title = items[1]
        self.value_column = items[2]
        self.value_func = items[3]
        self.formatter = items[4]
        self.chart_type = 'default' if items[5] is None else items[5]
        
        self.xvalues = []
        self.yvalues = []
        
    def add_axis(self, x, y):
        self.xvalues.append(x)
        self.yvalues.append(y)

chart_data_list = []

def create_chart_data(df : pd.DataFrame, config_items):
    chart_data = ChartData(config_items)
    for index, row in df.iterrows():
        #print(type(row[value_col].item()))
        val_col = chart_data.value_column
        val_func = chart_data.value_func
        yvalue = val_func(row[val_col]) if val_func else row[val_col].item()
        chart_data.add_axis(user_id_to_name(row['joy_run_id']), yvalue)
    
    chart_data_list.append(chart_data)

def draw_chart(chart_data : ChartData):
    xtitle = ''
    ytitle = ''
    height = len(chart_data.yvalues) * 20
    height = height if height > 480 else 480
    c = (Bar(init_opts=opts.InitOpts(bg_color='white', width='640px', height='%spx' % height))
        .add_xaxis(chart_data.xvalues)
        .add_yaxis(ytitle, chart_data.yvalues)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position='right', formatter=chart_data.formatter))
        .set_global_opts(title_opts=opts.TitleOpts(title=chart_data.title, subtitle=chart_data.sub_title, pos_left='center'),
                        xaxis_opts=opts.AxisOpts(name=xtitle, is_show=False),
                        yaxis_opts=opts.AxisOpts())
    )

    grid = Grid()
    grid.add(c, grid_opts=opts.GridOpts(pos_left="15%"))
    
    return grid
    #return c

def draw_word_cloud_chart(chart_data : ChartData):
    words = []
    for w, c in zip(chart_data.xvalues, chart_data.yvalues):
        words.append((w, c))

    wc = (WordCloud(init_opts=opts.InitOpts(bg_color='white', height='720px'))
        .add("", words, shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title=chart_data.title, subtitle=chart_data.sub_title, pos_left='center'))
    )

    return wc

chart_drawers = {
    'default' : draw_chart,
    'word_cloud' : draw_word_cloud_chart
}

def draw_charts():
    page = Page()
    page.page_title = 'Joyrun team run data stat'
    for chart_data in chart_data_list:
        print(chart_data.xvalues)
        print(chart_data.yvalues)
        draw_func = chart_drawers[chart_data.chart_type]
        page.add(draw_func(chart_data))
    page.render('chart_html/all.html')

to_hms_formatter = utils.JsCode("""function (params) {
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

to_ms_formatter = utils.JsCode("""function (params) {
        seconds = params.value;
        mins = Math.floor(seconds/60);
        seconds = seconds % 60;
        seconds = ('0' + seconds).slice(-2);
        return mins + ':' + seconds
    }
""")