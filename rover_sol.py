#!/usr/bin/env python
# -*- encoding:utf8 -*-

__author__ = "Jean Guirro (brut4l1ty@gmail.com)"
__version__ = "1.0.1"
__license__ = "GPL"
__status__ = "Development"

#https://mars.jpl.nasa.gov/msl-raw-images/image/image_manifest.json

import requests
import collections
from datetime import datetime
import xmltodict
import json

def sol():
    mars = requests.get('https://mars.jpl.nasa.gov/msl-raw-images/image/image_manifest.json')
    data = mars.json()
    last_upd = data['sols'][-1]['last_updated']
    sol = data['sols'][-1]['sol']
    catalog = data['sols'][-1]['catalog_url']
    date_posted = last_upd
    date = datetime.strptime(date_posted, '%Y-%m-%dT%H:%M:%SZ')
    earth_day = (sol * 1.0303)
    return date, sol, earth_day

def location():
    mars_loc = requests.get('https://mars.jpl.nasa.gov/msl-raw-images/locations.xml')
    mars_loc = mars_loc.text
    d = xmltodict.parse(mars_loc, xml_attribs=True)
    json_data = json.dumps(d, indent=4)
    location_data = json.loads(json_data)
    lat = location_data['msl']['location'][-1]['lat']
    z = location_data['msl']['location'][-1]['z']
    y = location_data['msl']['location'][-1]['y']
    x = location_data['msl']['location'][-1]['x']
    endSol = location_data['msl']['location'][-1]['endSol']
    return lat, z, y, x, endSol

def main():
    last_date, last_sol, earth = sol()
    print "Curiosity last update was in %s\nSol\t\t%d\nEarth Days\t%d" % (last_date, last_sol, earth)
    loc_lat, loc_z, loc_y, loc_x, loc_endSol = location()
    print "\nCurrent Location (Sol %s):\nLatitude\t%s\nZ\t\t%s\nY\t\t%s\nX\t\t%s\n" % (loc_endSol,loc_lat,loc_z,loc_y,loc_x)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Killed by user'
        sys.exit(0)
