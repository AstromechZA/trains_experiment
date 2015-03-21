#!/usr/bin/env python

import os
import json
import urllib
import urllib2

directory = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(directory, 'osm_data')

def load_data(overpass_query):
    # format POST data string
    data = urllib.urlencode({'data':overpass_query})
    # build request object
    response = urllib2.urlopen(urllib2.Request('http://overpass-api.de/api/interpreter', data))
    # read response and parse into JSON
    data = json.loads(response.read())
    return data

def main():
    # ensure data dir exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # load rail data for cape town
    rails_data = load_data('[out:json][timeout:25];(way["railway"="rail"](-34.087355326480655,18.369827270507812,-33.95076486932678,18.952102661132812););out body;>;out skel qt;')

    # write it into data dir
    with open(os.path.join(data_dir, 'rail_data.json'), 'w') as f:
        f.write(json.dumps(rails_data))

if __name__ == '__main__':
    main()
