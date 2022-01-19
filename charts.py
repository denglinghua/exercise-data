from pyecharts import options as opts
from pyecharts.charts import Bar, Calendar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons import utils
from group import GroupSet
from lang import lang

def draw_bar_chart(group_set):
    _init_formatter()

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
         .set_series_opts(label_opts=opts.LabelOpts(formatter=_get_formatter(group_set.title, ytitle)))
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
    
    _calendar_data_to_file(group_set.title, data)

    xtitle = ''
    ytitle = ''
    if (group_set.xtitle):
        xtitle = group_set.xtitle
    if (group_set.ytitle):
        ytitle = group_set.ytitle
    
    c = (Calendar()
        .add("", data, calendar_opts=opts.CalendarOpts(range_="2021",
            daylabel_opts=opts.CalendarDayLabelOpts(name_map=lang.calendar_name),
            monthlabel_opts=opts.CalendarMonthLabelOpts(name_map=lang.calendar_name)))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=group_set.title),
            visualmap_opts=opts.VisualMapOpts(
                max_=600,
                min_=0,
                pieces = [
                    {"min": 180, "label" : '>3 %s' % lang.hour_short, "color":'#E73C07'},
                    {"min": 120, "max": 180, "label" : '2+ %s' % lang.hour_short,"color":'#FFC300'},
                    {"min": 60, "max": 120, "label" : '1+ %s' % lang.hour_short, "color": '#66EE10'},
                    {"min": 0, "max": 60, "label" : '<1 %s' % lang.hour_short, "color": '#1FE5F7'},
                    {"value" : 0, "label":lang.rest, "color":'#BCC3C4'}
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
        draw_chart_func = _chart_types[group_set.chart_type]
        page.add(draw_chart_func(group_set))
    page.render('chart_html/all.html')

_mins_to_hm_formatter = """function (params) {
        mins = params.value;
        h = Math.floor(mins / 60); m = mins %% 60;
        r = '';
        if (h > 0) r += (h + ' %s ');
        if (m > 0) r += (m + ' %s ');
        return r;
    }
"""

_formatters = {}

def _init_formatter():
    _formatters[lang.total_activity_time] = _mins_to_hm_formatter % (lang.hour_short, lang.min_short)

def _get_formatter(title, ytitle):
    if title in _formatters:
        return utils.JsCode(_formatters[title])
    else:
        return '{c} %s' % ytitle

_chart_types = {
    'bar' : draw_bar_chart,
    'calendar' : draw_calendar_chart,
}

def _calendar_data_to_file(file, data):
    with open(file + '.log', 'w') as f:
        f.write('[')
        for item in data:
            f.write('\t\t["%s", "%s"],\n' % (item[0], item[1]))
        f.write(']')
