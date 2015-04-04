#!/usr/bin/env python

import os
import json

from validoot import typ

from constants import project_root, data_dir
from models.node import Node
from models.way import Way

def load_item(obj):
    if 'type' in obj:
        if obj['type'] == 'node':
            return Node.from_dict(obj)
        if obj['type'] == 'way':
            return Way.from_dict(obj)
    raise AttributeError("Obj %s was unrecognisable" % obj)

if __name__ == '__main__':

    with open(os.path.join(data_dir, 'rail_data.json')) as f:
        data = json.loads(f.read())

    elements = [load_item(o) for o in data['elements']]

    stations = filter(typ(Node)._and(lambda e: 'railway' in e.tags and e.tags['railway'] == 'station'), elements)

    prejson = {'points': [{'lat': s.latitude, 'lon': s.longitude} for s in stations]}

    javascript = "window.drawme({});".format(json.dumps(prejson))

    with open(os.path.join(project_root, 'web_build', 'data', 'drawme.js'), 'w') as f:
        f.write(javascript)