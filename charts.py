import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, Grid, Page
from pyecharts.globals import ThemeType, SymbolType

from chart_config import charts
from datasource import user_id_to_name

class ChartData(object):
    def __init__(self, chart_confg):
        self.config = chart_confg
        self.xvalues = []
        self.yvalues = []
        
    def add_axis(self, x, y):
        self.xvalues.append(x)
        self.yvalues.append(y)

chart_data_list = []

def create_chart_data(chart_name, df : pd.DataFrame):
    chart_config = charts[chart_name]
    chart_data = ChartData(chart_config)
    for index, row in df.iterrows():
        #print(type(row[value_col].item()))
        val_col = chart_config.value_column
        val_func = chart_config.value_func
        yvalue = val_func(row[val_col]) if val_func else row[val_col].item()
        chart_data.add_axis(user_id_to_name(row['joy_run_id']), yvalue)
    
    chart_data_list.append(chart_data)

def draw_chart(chart_data : ChartData):
    #__init_formatter()
    print(chart_data.xvalues)
    print(chart_data.yvalues)
    xtitle = ''
    ytitle = ''
    height = len(chart_data.yvalues) * 20
    height = height if height > 480 else 480
    c = (Bar(init_opts=opts.InitOpts(bg_color='white', width='640px', height='%spx' % height, renderer= "svg"))
        .add_xaxis(chart_data.xvalues)
        .add_yaxis(ytitle, chart_data.yvalues)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position='right', formatter=chart_data.config.formatter))
        .set_global_opts(title_opts=opts.TitleOpts(title=chart_data.config.title, subtitle=chart_data.config.sub_title, pos_left='center'),
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

    wc = (WordCloud(init_opts=opts.InitOpts(bg_color='white'))
        .add("", words, shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title=chart_data.config.title, subtitle=chart_data.config.sub_title, pos_left='center'))
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
        draw_func = chart_drawers[chart_data.config.chart_type]
        page.add(draw_func(chart_data))
    page.render('chart_html/all.html')