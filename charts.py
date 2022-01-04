from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, Line, Grid, Page
from pyecharts.globals import ThemeType, SymbolType
from pyecharts.commons import utils
from pyecharts.types import Tooltip

from chart_data import ChartData, chart_data_list

def draw_rank_bar_chart(chart_data : ChartData):
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

def draw_line_chart(chart_data : ChartData):
    h = chart_data.height if hasattr(chart_data, 'height') else '500px'
    min_ = chart_data.y_min if hasattr(chart_data, 'y_min') else 0
    print(min_)
    c = Line(init_opts=opts.InitOpts(bg_color='white', width='1080px', height=h))
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=chart_data.title, subtitle=chart_data.sub_title, pos_left='center'),
        tooltip_opts=opts.TooltipOpts(is_show=False), #trigger="axis", 
        legend_opts = opts.LegendOpts(orient='vertical', pos_right='1px', pos_top="50px"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            min_ = min_,
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=True),
            axislabel_opts=opts.LabelOpts(formatter=chart_data.formatter),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False))
    c.add_xaxis(xaxis_data=chart_data.xvalues)
    for y in chart_data.yvalues:
        c.add_yaxis(y[0], y[1], label_opts=opts.LabelOpts(is_show=False), is_symbol_show=False, is_smooth=True)

    grid=Grid()
    grid.add(c,grid_opts=opts.GridOpts(pos_right="14%"))
    
    return grid

chart_drawers = {
    'rank_bar' : draw_rank_bar_chart,
    'word_cloud' : draw_word_cloud_chart,
    'line' : draw_line_chart
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
        seconds =  isNaN(params) ? params.value : params;
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
        seconds =  isNaN(params) ? params.value : params;
        mins = Math.floor(seconds/60);
        seconds = seconds % 60;
        seconds = ('0' + seconds).slice(-2);
        return mins + ':' + seconds
    }
""")