# encoding:utf-8
from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from group import Group


def draw_group_chart(group):
    axis_values = group.get_axis_values()
    ytitle = ''
    if (group.ytitle) :
        ytitle = group.ytitle
    c = (Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
         .add_xaxis(axis_values[0])
         .add_yaxis("", axis_values[1], itemstyle_opts=opts.ItemStyleOpts(color='purple'))
         .set_series_opts(label_opts=opts.LabelOpts(formatter='{c} %s' % ytitle))
         .set_global_opts(title_opts=opts.TitleOpts(title=group.title, subtitle=""),
                          yaxis_opts=opts.AxisOpts(is_show=False))
         )

    return c


def draw_groups_chart(title, groups):
    page = Page()
    page.page_title = title
    for group in groups:
        page.add(draw_group_chart(group))
    page.render('chart_html/all.html')
