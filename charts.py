# encoding:utf-8
from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from group import Group


def draw_group_chart(group):
    yaxis_opts = None
    if (group.ytitle):
        yaxis_opts = opts.AxisOpts(axislabel_opts=opts.LabelOpts(
            formatter="{value} /%s" % group.ytitle))

    axis_values = group.get_axis_values()
    c = (Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
         .add_xaxis(axis_values[0])
         .add_yaxis("", axis_values[1], itemstyle_opts=opts.ItemStyleOpts(color='purple'))
         .set_global_opts(title_opts=opts.TitleOpts(title=group.title, subtitle=""), yaxis_opts=yaxis_opts)
         # .render('chart_html/' + group.title + ".html")
         )

    return c


def draw_groups_chart(title, groups):
    page = Page()
    page.page_title = title
    for group in groups:
        page.add(draw_group_chart(group))
    page.render('chart_html/all.html')
