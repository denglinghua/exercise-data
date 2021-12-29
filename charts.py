import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons import utils

class ChartData(object):
    def __init__(self, title):
        self.title = title
        self.xtitle = None
        self.ytitle = None
        self.xvalues = []
        self.yvalues = []
        
    def set_xtitle(self, title):
        self.xtitle = title
        return self
    
    def set_ytitle(self, title):
        self.ytitle = title
        return self

    def add_axis(self, x, y):
        self.xvalues.append(x)
        self.yvalues.append(y)

def create_chart_data(df : pd.DataFrame, value_col, id_name, title):
    chart_data = ChartData(title)
    for index, row in df.iterrows():
        chart_data.add_axis(id_name[row['joy_run_id']], int(row[value_col]))
    return chart_data

def draw_chart(chart_data : ChartData):
    #__init_formatter()
    print(chart_data.xvalues)
    print(chart_data.yvalues)
    xtitle = ''
    ytitle = ''
    if (chart_data.xtitle):
        xtitle = chart_data.xtitle
    if (chart_data.ytitle):
        ytitle = chart_data.ytitle
    c = (Bar(init_opts=opts.InitOpts(bg_color='white'))
        .add_xaxis(chart_data.xvalues)
        .add_yaxis(ytitle, chart_data.yvalues)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title=chart_data.title))
    )
    
    return c

def draw_charts(title, chart_data_list):
    page = Page()
    page.page_title = title
    for chart_data in chart_data_list:
        page.add(draw_chart(chart_data))
    page.render('chart_html/all.html')