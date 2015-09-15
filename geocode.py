import json
from geopy.geocoders import Nominatim
from pyhull.convex_hull import ConvexHull

geolocator = Nominatim()

def get_addrs(addr_range):
    parts = addr_range.split('--')

    if len(parts) == 2:
        street_parts = parts[1].split(' ')
        return [
            parts[0] + ' ' + ' '.join(street_parts[1:]),
            parts[1]
        ]
    return []

def geocode(addr):
    loc = geolocator.geocode(addr)
    return (loc.latitude, loc.longitude)

def convex_hull(lat_lngs):
    hull = ConvexHull(lat_lngs)
    return hull.vertices

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
