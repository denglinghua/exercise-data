from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from lang import lang;

def draw_group_chart(group):

    axis_values = group.get_axis_values()
    xvalues = axis_values[0]
    yvalues = []
    total = sum(axis_values[1])
    for yvalue in axis_values[1]:
        percent = round(yvalue * 100 / total, 1)
        yvalues.append({"value": yvalue, "percent": '%s%%' % percent})
    
    percent_formatter=JsCode("function(x){return x.data.percent;}")

    xtitle = ''
    ytitle = ''
    if (group.xtitle):
        xtitle = group.xtitle
    if (group.ytitle):
        ytitle = group.ytitle
    c = (Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
         .add_xaxis(axis_values[0])
         .add_yaxis("", yvalues, itemstyle_opts=opts.ItemStyleOpts(color='purple'))
         .set_series_opts(label_opts=opts.LabelOpts(formatter=percent_formatter))
         .set_global_opts(title_opts=opts.TitleOpts(title=group.title, subtitle=""),
                        xaxis_opts=opts.AxisOpts(name=xtitle),
                        yaxis_opts=opts.AxisOpts(is_show=False))
         )
    
    return c

def draw_groups_chart(title, groups):
    page = Page()
    page.page_title = title
    groups_to_draw = [lang.average_run_pace, lang.running_distance]
    for group in groups:
        if group.title in groups_to_draw:
            page.add(draw_group_chart(group))
    page.render('chart_html/bar_percent.html')