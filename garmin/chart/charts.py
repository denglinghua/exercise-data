import os
from pyecharts import options as opts
from pyecharts.charts import Bar, Calendar, Page, WordCloud, Line, Scatter, HeatMap, Pie
from pyecharts.globals import SymbolType
from pyecharts.faker import Faker
from pyecharts.commons import utils
from lang import lang

bg_color = '#eeeeee'

def create_bar_chart(group_set):
    _init_formatter()

    axis_values = group_set.get_axis_values()
    xtitle = ''
    ytitle = ''
    if (group_set.xtitle):
        xtitle = group_set.xtitle
    if (group_set.ytitle):
        ytitle = group_set.ytitle
    c = (Bar(init_opts=opts.InitOpts(bg_color=bg_color))
         .add_xaxis(axis_values[0])
         .add_yaxis("", axis_values[1], itemstyle_opts=opts.ItemStyleOpts(color='purple'))
         .set_series_opts(label_opts=opts.LabelOpts(formatter=_get_formatter(group_set.title, ytitle)))
         .set_global_opts(title_opts=opts.TitleOpts(title=group_set.title, subtitle="", pos_left='center'),
                        xaxis_opts=opts.AxisOpts(name=xtitle),
                        yaxis_opts=opts.AxisOpts(is_show=False))
         )
    
    return c

def create_pie_chart(group_set):
    _init_formatter(True)
    axis_values = group_set.get_axis_values()
    c = (
        Pie(init_opts=opts.InitOpts(bg_color=bg_color))
        .add("", [list(z) for z in zip(axis_values[0], axis_values[1])])
        .set_colors(["red", "blue", "yellow"])
        .set_global_opts(title_opts=opts.TitleOpts(title=group_set.title, pos_left='center'),
                         legend_opts=opts.LegendOpts(is_show=False),)
        .set_series_opts(label_opts=opts.LabelOpts(position='inside', formatter=_get_formatter(lang.total_activity_time, lang.hour_short)))
    )

    return c

def create_line_chart(group_set):
    _init_formatter()

    axis_values = group_set.get_axis_values(True, True)
    xtitle = ''
    ytitle = ''
    if (group_set.xtitle):
        xtitle = group_set.xtitle
    if (group_set.ytitle):
        ytitle = group_set.ytitle
    c = (Line(init_opts=opts.InitOpts(bg_color=bg_color))
         .add_xaxis(axis_values[0])
         .add_yaxis("", axis_values[1], is_symbol_show=False, itemstyle_opts=opts.ItemStyleOpts(color='purple'),
                    markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
         .set_series_opts(label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
         .set_global_opts(title_opts=opts.TitleOpts(title=group_set.title, subtitle="", pos_left='center'),
                        xaxis_opts=opts.AxisOpts(name=xtitle),
                        yaxis_opts=opts.AxisOpts(is_show=True, name=lang.km))
         )
    
    return c

def create_stacked_line_chart(group_set):
    _init_formatter()
    
    axis_values = group_set.get_axis_values(False, True)
    activities = [lang.running, lang.swimming, lang.cycling]
    
    ys = []
    for i in range(len(activities)):
        ys.append([])
    
    for items in axis_values[1]:
        i = 0
        for a in activities:
            ys[i].append(items[i])
            i += 1
    
    c = Line(init_opts=opts.InitOpts(bg_color=bg_color)).add_xaxis(xaxis_data=axis_values[0])
    
    i = 0     
    for a in activities:
        c.add_yaxis(series_name=a, 
                    stack="Total",
                    y_axis=ys[i], 
                    areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                    is_symbol_show=False,
                    label_opts=opts.LabelOpts(is_show=False, position="top"),)
        i += 1
    
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=group_set.title, subtitle="", pos_left='center'),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="horizontal", pos_top="95%", pos_left="center"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name="Activities",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
    
    return c

def create_word_cloud_chart(group_set):
    words = []
    axis_values = group_set.get_axis_values()
    for items in zip(axis_values[0], axis_values[1]):
        words.append(items)

    wc = (WordCloud(init_opts=opts.InitOpts(bg_color=bg_color))
        .add("", words, shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title=group_set.title, subtitle='', pos_left='center'))
    )

    return wc

def create_scatter_chart(rows):
    x_data = []
    y_data = []
    for row in rows:
        isRun = row[lang.data__activity_type].find(lang.data__keyword_running) >= 0
        if isRun:
            p = row[lang.data__avg_pace]
            p = p.tm_min * 60 + p.tm_sec
            if p < 600:
                x_data.append(row[lang.data__distance])
                y_data.append(p)

    st = (Scatter(init_opts=opts.InitOpts(bg_color=bg_color))
     .add_xaxis(xaxis_data=x_data)
     .add_yaxis(series_name="",
        y_axis=y_data,
        symbol_size=5,
        # itemstyle_opts=opts.ItemStyleOpts(color='blue'),
        label_opts=opts.LabelOpts(is_show=False),)
    .set_series_opts()
    .set_global_opts(
        title_opts=opts.TitleOpts(title='Distribution of Pace Over Distance', subtitle="", pos_left='center'),
        xaxis_opts=opts.AxisOpts(
            name=lang.km,
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        yaxis_opts=opts.AxisOpts(
            name='Avg Pace(min/km)',
            type_="value",
            min_=240,
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
            axislabel_opts=opts.LabelOpts(formatter=to_ms_formatter),
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False)))
    
    return st

def generate_color_palette():
    colors = ['#1d4877', '#1b8a5a', '#fbb021', '#f68838', '#ee3e32']
    return colors

def create_heatmap_chart(group_set):
    value = []
    axis_values = group_set.get_axis_values()
    for items in zip(axis_values[0], axis_values[1]):
        wh = items[0].split('-')
        value.append([int(wh[1]), int(wh[0]), items[1]])
    
    weekDays = lang.days_of_week
    hours = [c.upper() for c in Faker.clock]
    c = (
        HeatMap(init_opts=opts.InitOpts(bg_color=bg_color))
        .add_xaxis(hours)
        .add_yaxis(
            "", lang.days_of_week, value, label_opts=opts.LabelOpts(position="inside")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title = group_set.title, pos_left='center'),
            visualmap_opts=opts.VisualMapOpts(is_calculable=True, orient="horizontal", pos_left="center",
                range_color=generate_color_palette()),
        )
        )

    return c

def create_calendar_chart(group_set):
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

def draw_groups_chart(title, group_sets, rows):
    page = Page()
    page.page_title = title
    for group_set in group_sets:
        draw_chart_func = _chart_types[group_set.chart_type]
        page.add(draw_chart_func(group_set))
    
    page.add(create_scatter_chart(rows))
    
    html_dir = os.path.join(os.getcwd(), 'chart_html')
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    html_path = os.path.join(html_dir, 'all.html')
    page.render(html_path)

_mins_to_hm_formatter = """function (params) {
        mins = params.value;
        h = Math.floor(mins / 60); m = mins %% 60;
        r = '';
        if (h > 0) r += (h + ' %s ');
        if (m > 0) r += (m + ' %s ');
        if (%s) r = params.name + ': ' + r;
        return r;
    }
"""

to_ms_formatter = utils.JsCode("""function (params) {
        seconds =  isNaN(params) ? params.value : params;
        mins = Math.floor(seconds/60);
        seconds = seconds % 60;
        seconds = ('0' + seconds).slice(-2);
        return mins + ':' + seconds
    }
""")

_formatters = {}

def _init_formatter(showName = False):
    name = 'true' if showName else 'false'
    _formatters[lang.total_activity_time] = _mins_to_hm_formatter % (lang.hour_short, lang.min_short, name)

def _get_formatter(title, ytitle):
    if title in _formatters:
        return utils.JsCode(_formatters[title])
    else:
        return '{c} %s' % ytitle

_chart_types = {
    'bar' : create_bar_chart,
    'wordcloud' : create_word_cloud_chart,
    'line' : create_line_chart,
    'calendar' : create_calendar_chart,
    'heatmap' : create_heatmap_chart,
    'pie' : create_pie_chart,
    'stacked_line' : create_stacked_line_chart,
}

def _calendar_data_to_file(file, data):
    with open(file + '.log', 'w') as f:
        f.write('[')
        for item in data:
            f.write('\t\t["%s", "%s"],\n' % (item[0], item[1]))
        f.write(']')
