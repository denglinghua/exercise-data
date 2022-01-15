from pyecharts import options as opts
from pyecharts.charts import Bar, Calendar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons import utils
from group import GroupSet
from lang import lang

def draw_bar_chart(group_set):
    __init_formatter()

    axis_values = group_set.get_axis_values()
    xtitle = ''
    ytitle = ''
    if (group_set.xtitle):
        xtitle = group_set.xtitle
    if (group_set.ytitle):
        ytitle = group_set.ytitle
    c = (Bar(init_opts=opts.InitOpts(bg_color='white'))
         .add_xaxis(axis_values[0])
         .add_yaxis("", axis_values[1], itemstyle_opts=opts.ItemStyleOpts(color='purple'))
         .set_series_opts(label_opts=opts.LabelOpts(formatter=__get_formatter(group_set.title, ytitle)))
         .set_global_opts(title_opts=opts.TitleOpts(title=group_set.title, subtitle="", pos_left='center'),
                        xaxis_opts=opts.AxisOpts(name=xtitle),
                        yaxis_opts=opts.AxisOpts(is_show=False))
         )
    
    return c

def draw_calendar_chart(group_set):
    axis_values = group_set.get_axis_values(drop_zero = False)
    data = []
    for items in zip(axis_values[0], axis_values[1]):
        data.append([items[0], items[1]])

    xtitle = ''
    ytitle = ''
    if (group_set.xtitle):
        xtitle = group_set.xtitle
    if (group_set.ytitle):
        ytitle = group_set.ytitle
    
    c = (Calendar()
        .add("", data, calendar_opts=opts.CalendarOpts(range_="2021"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=group_set.title),
            visualmap_opts=opts.VisualMapOpts(
                max_=600,
                min_=0,
                pieces = [
                    {"min": 240, "color":'#900C3F'}, 
                    {"min": 181, "max": 240, "color":'#C70039'},
                    {"min": 121, "max": 180, "color":'#FF5733'},
                    {"min": 61, "max": 120, "color": '#FFC300'},
                    {"min": 1, "max": 60, "color": '#DAF7A6'},
                    {"value" : 0, "label":'REST', "color":'#7B7D7A'}
                ],
                orient="horizontal",
                is_piecewise=True,
                pos_top="230px",
                pos_left="100px",
            )
        )
    )
    
    return c

def draw_groups_chart(title, group_sets):
    page = Page()
    page.page_title = title
    for group_set in group_sets:
        draw_chart_func = __chart_types[group_set.chart_type]
        page.add(draw_chart_func(group_set))
    page.render('chart_html/all.html')

__mins_to_hm_formatter = """function (params) {
        mins = params.value;
        h = Math.floor(mins / 60); m = mins %% 60;
        r = '';
        if (h > 0) r += (h + ' %s ');
        if (m > 0) r += (m + ' %s ');
        return r;
    }
"""

__formatters = {}

def __init_formatter():
    __formatters[lang.total_activity_time] = __mins_to_hm_formatter % (lang.hour_short, lang.min_short)

def __get_formatter(title, ytitle):
    if title in __formatters:
        return utils.JsCode(__formatters[title])
    else:
        return '{c} %s' % ytitle

__chart_types = {
    'bar' : draw_bar_chart,
    'calendar' : draw_calendar_chart,
}
