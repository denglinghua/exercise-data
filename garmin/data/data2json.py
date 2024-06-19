import os
import json

from lang import lang

def save_data(rows, group_sets):
    obj = {}
    for group_set in group_sets:
        axis_values = group_set.get_axis_values()
        obj[group_set.name] = {
            'title': group_set.title,
            'series': { 'x' : axis_values[0], 'y' : axis_values[1] }
        }

    pace_distance = []
    for row in rows:
        isRun = row[lang.data__activity_type].find(lang.data__keyword_running) >= 0
        if isRun:
            p = row[lang.data__avg_pace]
            p = p.tm_min * 60 + p.tm_sec
            if p < 600:
                pace_distance.append([row[lang.data__distance], p])
    
    obj['pace_distance'] = {
        'title': 'Distribution of Pace Over Distance',
         'series': pace_distance 
    }

    save_file(obj)

def save_file(all_data):
    data_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    file_name = os.path.join(data_dir, 'triathlon')
    with open(file_name, 'w') as f:
        json.dump(all_data, f)