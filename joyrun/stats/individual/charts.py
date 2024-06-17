import os
from pyecharts import options as opts
from pyecharts.charts import Page, Line, Scatter, HeatMap
from pyecharts.faker import Faker
from pyecharts.commons import utils

bg_color = '#eeeeee'

def create_month_distance_line(name, title, data):
    _init_formatter()

    xtitle = ''
    c = (Line(init_opts=opts.InitOpts(bg_color=bg_color))
         .add_xaxis(data['x'])
         .add_yaxis("", data['y'], is_symbol_show=False, itemstyle_opts=opts.ItemStyleOpts(color='green'),
                    markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
         .set_series_opts(label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
         .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle="", pos_left='center'),
                        xaxis_opts=opts.AxisOpts(name=xtitle),
                        yaxis_opts=opts.AxisOpts(is_show=True, name='公里'))
         )
    
    return c

def create_month_pace_line(name, title, data):
    _init_formatter()

    xtitle = ''
    c = (Line(init_opts=opts.InitOpts(bg_color=bg_color))
         .add_xaxis(data['x'])
         .add_yaxis("", data['y'], is_symbol_show=False, itemstyle_opts=opts.ItemStyleOpts(color='orange'),
                    markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
         .set_series_opts(label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
         .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle="", pos_left='center'),
                        xaxis_opts=opts.AxisOpts(name=xtitle),
                        yaxis_opts=opts.AxisOpts(is_show=True, name='', is_inverse = True, min_ = 240,
                                                 axislabel_opts=opts.LabelOpts(formatter=to_ms_formatter)))
         )
    
    return c

def create_pace_distance_scatter(name, title, data):
    x_data = []
    y_data = []
    for row in data:
            p = row[1]
            if p < 600:
                x_data.append(row[0])
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
        title_opts=opts.TitleOpts(title=title, subtitle="", pos_left='center'),
        xaxis_opts=opts.AxisOpts(
            name='距离',
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        yaxis_opts=opts.AxisOpts(
            name='配速',
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

def create_week_hour_heatmap(name, title, data):
    value = data
    
    weekDays = ["一", "二", "三", "四", "五", "六", "日"]
    hours = [c.upper() for c in Faker.clock]
    c = (
        HeatMap(init_opts=opts.InitOpts(bg_color=bg_color))
        .add_xaxis(hours)
        .add_yaxis(
            "", weekDays, value, label_opts=opts.LabelOpts(position="inside")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title = title, pos_left='center'),
            visualmap_opts=opts.VisualMapOpts(is_calculable=True, orient="horizontal", pos_left="center",
                range_color=generate_color_palette()),
        )
        )

    return c

def draw_groups_chart(title, all_data):
    page = Page()
    page.page_title = title
    for name, data in all_data.items():
        print(name, data)
        draw_chart_func = _chart_types[name]
        page.add(draw_chart_func(name, data['title'], data['data']))
    
    html_dir = os.path.join(os.getcwd(), 'chart_html')
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    html_path = os.path.join(html_dir, 'individual.html')
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

def _get_formatter(title, ytitle):
    if title in _formatters:
        return utils.JsCode(_formatters[title])
    else:
        return '{c} %s' % ytitle

_chart_types = {
    'month_distance' : create_month_distance_line,
    'week_hour' : create_week_hour_heatmap,
    'pace_distance' : create_pace_distance_scatter,
    'month_pace' : create_month_pace_line,
}

def _calendar_data_to_file(file, data):
    with open(file + '.log', 'w') as f:
        f.write('[')
        for item in data:
            f.write('\t\t["%s", "%s"],\n' % (item[0], item[1]))
        f.write(']')
