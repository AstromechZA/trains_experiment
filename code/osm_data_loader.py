#!/usr/bin/env python
import re
import os
import json

from validoot import typ

from constants import project_root, data_dir
from models.node import Node
from models.way import Way
from utils.index_map import IndexMap
from utils.connection import Connection

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


def parse_time(time_str):
    time_str = time_str.replace(':', '')
    hours = int(time_str[:2])
    mins = int(time_str[2:])
    return (hours * 60 + mins) * 60


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
    stations = filter(typ(Node), elements)
    stations = filter(lambda e: 'railway' in e.tags and e.tags['railway'] == 'station', stations)
    stations = filter(lambda e: 'name' in e.tags, stations)

    stations_we_have_positions_for = set()
    for s in stations:
        if 'name' in s.tags:
            stations_we_have_positions_for.add(sanitize_station_name(s.tags['name']))

    unknown_stations = stations_we_have_routes_for - stations_we_have_positions_for
    if len(unknown_stations) > 0:
        print 'Unknown Stations:', unknown_stations

    # Build index-name maps. Useful for forgetting about silly
    station_map = IndexMap(stations_we_have_routes_for)

    # Add attributes to the index map
    for s in stations:
        n = sanitize_station_name(s.tags['name'])
        if n in station_map:
            i = station_map.geti(n)
            station_map.geta(i)['name'] = s.tags['name']
            station_map.geta(i)['lat'] = s.latitude
            station_map.geta(i)['lon'] = s.longitude

    connections = set()

    # Rebuild train_times map
    new_train_times = {}
    for day, trains in train_times.items():
        new_trains = []
        for train in trains:
            new_stops = []
            last_stop = None
            for stop in train['stops']:
                stopi = station_map.geti(sanitize_station_name(stop[0]))
                new_stops.append([stopi, parse_time(stop[1])])
                if last_stop is not None:
                    connections.add(Connection(last_stop, stopi))
                last_stop = stopi

            new_trains.append({
                'train_number': train['train_number'],
                'stops': new_stops
            })
        new_train_times[day] = new_trains

    stations_json = dict(list([a, c] for a, b, c in station_map))
    trains_json = new_train_times
    connections_json = [[c.frm, c.to] for c in connections]

    with open(os.path.join(project_root, 'web_source', 'data', 'all_data.js'), 'w') as f:
        f.write('window.data_stations = %s\n' % json.dumps(stations_json))
        f.write('window.data_trains = %s\n' % json.dumps(trains_json))
        f.write('window.data_connections = %s\n' % json.dumps(connections_json))
        f.write('window.callback_data_loaded()')
