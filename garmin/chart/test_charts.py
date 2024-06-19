from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from lang import lang;

def draw_group_chart(group_set):

    axis_values = group_set.get_axis_values()
    xvalues = axis_values[0]
    yvalues = []
    total = sum(axis_values[1])
    for yvalue in axis_values[1]:
        percent = round(yvalue * 100 / total, 1)
        yvalues.append({"value": yvalue, "percent": '%s%%' % percent})
    
    percent_formatter=JsCode("function(x){return x.data.percent;}")

    xtitle = ''
    ytitle = ''
    if (group_set.xtitle):
        xtitle = group_set.xtitle
    if (group_set.ytitle):
        ytitle = group_set.ytitle
    c = (Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
         .add_xaxis(axis_values[0])
         .add_yaxis("", yvalues, itemstyle_opts=opts.ItemStyleOpts(color='purple'))
         .set_series_opts(label_opts=opts.LabelOpts(formatter=percent_formatter))
         .set_global_opts(title_opts=opts.TitleOpts(title=group_set.title, subtitle=""),
                        xaxis_opts=opts.AxisOpts(name=xtitle),
                        yaxis_opts=opts.AxisOpts(is_show=False))
         )
    
    return c

def draw_groups_chart(title, group_sets):
    page = Page()
    page.page_title = title
    groups_to_draw = [lang.average_run_pace, lang.running_distance]
    for group_set in group_sets:
        if group_set.title in groups_to_draw:
            page.add(draw_group_chart(group_set))
    page.render('output/bar_percent.html')