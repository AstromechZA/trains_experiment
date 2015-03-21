#!/usr/bin/env python

import os
import json
import urllib
import urllib2

from constants import directory, data_dir

def load_data(overpass_query):
    # format POST data string
    data = urllib.urlencode({'data':overpass_query})
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
    rails_data = load_data('[out:json][timeout:25];(way["railway"](-34.087355326480655,18.369827270507812,-33.95076486932678,18.952102661132812);node["railway"="station"](-34.087355326480655,18.369827270507812,-33.95076486932678,18.952102661132812););out body;>;out skel qt;')

    # write it into data dir
    with open(os.path.join(data_dir, 'rail_data.json'), 'w') as f:
        f.write(json.dumps(rails_data))

if __name__ == '__main__':
    main()
