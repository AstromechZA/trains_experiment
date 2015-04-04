#!/usr/bin/env python

import os
import json
import urllib
import urllib2

from constants import data_dir


def load_data(overpass_query):
    # format POST data string
    data = urllib.urlencode({'data': overpass_query})
    # build request object
    response = urllib2.urlopen(urllib2.Request('http://overpass-api.de/api/interpreter', data))
    # read response and parse into JSON
    plain_text = response.read()
    print 'Downloaded %d bytes of JSON for query=%r' % (len(plain_text), overpass_query)
    return json.loads(plain_text)


def main():
    # ensure data dir exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # load rail data for cape town

    bounds = '-34.087355326480655,18.369827270507812,-33.95076486932678,18.952102661132812'
    bounds = '-33.856372,18.310666,-34.2213058,18.7786471'
    bounds = '-34.2213058,18.310666,-33.856372,18.7786471'

    query = ('[out:json][timeout:25];'
             '('
             'way["railway"]({bounds});'
             'node["railway"="station"]({bounds});'
             ');'
             'out body;>;out skel qt;').format(bounds=bounds)

    rails_data = load_data(query)

    # write it into data dir
    with open(os.path.join(data_dir, 'rail_data.json'), 'w') as f:
        f.write(json.dumps(rails_data))

    for e in rails_data['elements']:
        print e





if __name__ == '__main__':
    main()
