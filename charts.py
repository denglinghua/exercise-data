import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, Page
from pyecharts.globals import ThemeType, SymbolType

class ChartData(object):
    def __init__(self, chart_confg):
        self.config = chart_confg
        self.xvalues = []
        self.yvalues = []
        
    def add_axis(self, x, y):
        self.xvalues.append(x)
        self.yvalues.append(y)

chart_data_list = []

def create_chart_data(df : pd.DataFrame, id_name, chart_config):
    chart_data = ChartData(chart_config)
    for index, row in df.iterrows():
        #print(type(row[value_col].item()))
        val_col = chart_config.value_column
        val_func = chart_config.value_func
        yvalue = val_func(row[val_col]) if val_func else row[val_col].item()
        chart_data.add_axis(id_name[row['joy_run_id']], yvalue)
    
    chart_data_list.append(chart_data)

def draw_chart(chart_data : ChartData):
    #__init_formatter()
    print(chart_data.xvalues)
    print(chart_data.yvalues)
    xtitle = ''
    ytitle = ''
    height = len(chart_data.yvalues) * 20
    height = height if height > 500 else 500
    c = (Bar(init_opts=opts.InitOpts(bg_color='white', width='1200px', height='%spx' % height))
        .add_xaxis(chart_data.xvalues)
        .add_yaxis(ytitle, chart_data.yvalues)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position='right', formatter=chart_data.config.formatter))
        .set_global_opts(title_opts=opts.TitleOpts(title=chart_data.config.title, subtitle=chart_data.config.sub_title, pos_left='center'),
                        xaxis_opts=opts.AxisOpts(name=xtitle, is_show=False))
    )
    
    return c

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