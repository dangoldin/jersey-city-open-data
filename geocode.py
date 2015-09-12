import json

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
    lat, lng = geopy.geocode(addr)
    return (lat, lng)

# Figure out the algo here
def convex_poly(lat_lngs):
    poly = []
    for lat, lng in lat_lngs:
        pass
    return poly

with open('zone-permit-zones.json','r') as f:
    j = json.loads(f.read())

    out = {}
    for zone, zone_addrs in j.iteritems():
        addrs = []
        for addr_range in zone_addrs:
            addr_pair = get_addrs(addr_range)
            if len(addr_pair) > 0:
                addrs.extend(addr_pair)

        print addrs

        lat_lngs = [geocode(a) for a in addrs]

        out[zone] = convex_poly(lat_lngs)

    with open('zone-permit-geocoded.json', 'w') as g:
        g.write(json.dumps(out, indent=2))
