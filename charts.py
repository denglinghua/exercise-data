from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons import utils
from group import Group
from lang import lang


def draw_group_chart(group):
    __init_formatter()

    axis_values = group.get_axis_values()
    xtitle = ''
    ytitle = ''
    if (group.xtitle):
        xtitle = group.xtitle
    if (group.ytitle):
        ytitle = group.ytitle
    c = (Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
         .add_xaxis(axis_values[0])
         .add_yaxis("", axis_values[1], itemstyle_opts=opts.ItemStyleOpts(color='purple'))
         .set_series_opts(label_opts=opts.LabelOpts(formatter=__get_formatter(group.title, ytitle)))
         .set_global_opts(title_opts=opts.TitleOpts(title=group.title, subtitle=""),
                        xaxis_opts=opts.AxisOpts(name=xtitle),
                        yaxis_opts=opts.AxisOpts(is_show=False))
         )
    
    return c

def draw_groups_chart(title, groups):
    page = Page()
    page.page_title = title
    for group in groups:
        page.add(draw_group_chart(group))
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
    __formatters[lang.total_activity_time] = __mins_to_hm_formatter % (lang.hour, lang.min)

def __get_formatter(title, ytitle):
    if title in __formatters:
        return utils.JsCode(__formatters[title])
    else:
        return '{c} %s' % ytitle
