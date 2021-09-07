from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons import utils
from group import GroupSet
from lang import lang


def draw_group_chart(group_set):
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

def draw_groups_chart(title, group_sets):
    page = Page()
    page.page_title = title
    for group_set in group_sets:
        page.add(draw_group_chart(group_set))
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
