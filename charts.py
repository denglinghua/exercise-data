# encoding:utf-8
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker
from group import Group


def draw_group_chart(group):
    axis_values = group.get_axis_values()
    c = (Bar()
         .add_xaxis(axis_values[0])
         .add_yaxis("", axis_values[1])
         .set_global_opts(title_opts=opts.TitleOpts(title=group.title, subtitle=""))
         .render('chart_html/' + group.title + ".html"))
