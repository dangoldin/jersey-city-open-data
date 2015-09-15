#!/usr/bin/python

import json
import time

from geopy.geocoders import Nominatim, GoogleV3
from pyhull.convex_hull import ConvexHull

import settings

TIMEOUT_SECONDS = 1

MAX_ATTEMPTS = 5

# geolocator = Nominatim(timeout=TIMEOUT_SECONDS)
geolocator = GoogleV3(timeout=TIMEOUT_SECONDS,api_key=settings.GOOGLE_MAPS_API_KEY)

def get_addrs(addr_range):
    parts = addr_range.split('--')

    if len(parts) == 2:
        street_parts = parts[1].split(' ')
        return [
            parts[0] + ' ' + ' '.join(street_parts[1:]) + ' Jersey City, NJ',
            parts[1] + ' Jersey City, NJ',
        ]
    return []

def geocode(addr, attempts_left = MAX_ATTEMPTS):
    print 'Geocoding: ', addr
    while attempts_left > 0:
        try:
            loc = geolocator.geocode(addr)
            return (loc.latitude, loc.longitude)
        except Exception, e:
            print 'Failed to geocode: ', addr, e
            attempts_left -= 1
            time.sleep(TIMEOUT_SECONDS * 2 * (MAX_ATTEMPTS - attempts_left + 1))

    return None

def convex_hull(lat_lngs):
    hull = ConvexHull(lat_lngs)
    vertices = dict((x, y) for x, y in hull.vertices)
    poly = []
    curr = hull.vertices[0][0]
    while len(poly) < len(hull.vertices):
        poly.append( lat_lngs[curr] )
        curr = vertices[curr]
    return poly

with open('zone-permit-zones.json','r') as f:
    j = json.loads(f.read())

    out = {}
    for zone, zone_addrs in j.iteritems():
        if zone == 'ZONE 1':
            addrs = []
            for addr_range in zone_addrs:
                addr_pair = get_addrs(addr_range)
                if len(addr_pair) > 0:
                    addrs.extend(addr_pair)

            print addrs

            lat_lngs = [geocode(a) for a in addrs]

            print lat_lngs

            out[zone] = convex_hull(lat_lngs)

            print out

    with open('zone-permit-geocoded.json', 'w') as g:
        g.write(json.dumps(out, indent=2))
