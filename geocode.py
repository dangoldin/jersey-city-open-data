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
    pass

with open('zone-permit-zones.json','r') as f:
    j = json.loads(f.read())

    zone1 = j['ZONE 1']

    addrs = []
    for addr_range in zone1:
        addr_pair = get_addrs(addr_range)
        if len(addr_pair) > 0:
            addrs.extend(addr_pair)

    print addrs