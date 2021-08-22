# encoding:utf-8
from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from group import Group


def draw_group_chart(group):
    axis_values = group.get_axis_values()
    c = (Bar(init_opts=opts.InitOpts(theme=ThemeType.WHITE))
         .add_xaxis(axis_values[0])
         .add_yaxis("", axis_values[1])
         .set_global_opts(title_opts=opts.TitleOpts(title=group.title, subtitle=""))
         #.render('chart_html/' + group.title + ".html")
    )
    return c

def draw_groups_chart(groups):
    page = Page()
    for group in groups:
        page.add(draw_group_chart(group))
    page.render('chart_html/all.html')
