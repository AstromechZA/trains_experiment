#!/usr/bin/env python
import re
import os
import json

from validoot import typ

from constants import project_root, data_dir
from models.node import Node
from models.way import Way


KNOWN_TRANSLATIONS = {
    'dieprivier': 'diepriver'
}


def load_item(obj):
    if 'type' in obj:
        if obj['type'] == 'node':
            return Node.from_dict(obj)
        if obj['type'] == 'way':
            return Way.from_dict(obj)
    raise AttributeError("Obj %s was unrecognisable" % obj)


def sanitize_station_name(name):
    # replace rd
    name = name.lower().strip().replace(' rd', ' road')
    name = re.sub(r'[^a-z0-9]', '', name)
    name = KNOWN_TRANSLATIONS.get(name, name)
    return name


if __name__ == '__main__':

    with open(os.path.join(data_dir, 'rail_data.json')) as f:
        rail_data = json.loads(f.read())

    with open(os.path.join(data_dir, 'train_times.json')) as f:
        train_times = json.loads(f.read())

    stations_we_have_routes_for = set()
    for t in train_times['weekdays']:
        for s in t['stops']:
            stations_we_have_routes_for.add(sanitize_station_name(s[0]))

    elements = [load_item(o) for o in rail_data['elements']]
    stations = filter(typ(Node)._and(lambda e: 'railway' in e.tags and e.tags['railway'] == 'station'), elements)
    stations = filter(lambda e: 'name' in e.tags, stations)

    stations_we_have_positions_for = set()
    for s in stations:
        if 'name' in s.tags:
            stations_we_have_positions_for.add(sanitize_station_name(s.tags['name']))

    unknown_stations = stations_we_have_routes_for - stations_we_have_positions_for
    if len(unknown_stations) > 0:
        print 'Unknown Stations:', unknown_stations

    points = []
    for s in stations:
        if sanitize_station_name(s.tags['name']) in stations_we_have_routes_for:
            points.append({'lat': s.latitude, 'lon': s.longitude, 'name': s.tags['name']})

    prejson = {'points': points}
    javascript = "window.drawme({});".format(json.dumps(prejson))
    with open(os.path.join(project_root, 'web_build', 'data', 'drawme.js'), 'w') as f:
        f.write(javascript)