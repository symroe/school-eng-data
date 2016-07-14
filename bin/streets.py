#!/usr/bin/env python3

import sys
import csv
from glob import glob

fields = ['street', 'name', 'name-cy', 'place', 'local-authority', 'polyline', 'end-date']

streets = {}
places = {}


def place_key(row):
    return ":".join([row['local-authority'], row['town'], row['locality']])


if __name__ == '__main__':

    # load streets from addresses
    for row in csv.DictReader(sys.stdin, delimiter='\t'):
        streets[row['street']] = {}

    # load school locality to place map
    for row in csv.DictReader(open('maps/locality.tsv'), delimiter='\t'):
        places[place_key(row)] = row['place']

    # output streets mentioned in the map

    print("\t".join(fields))

    for path in glob('../address-data/data/street/*.tsv'):
        for row in csv.DictReader(open(path), delimiter='\t'):
            if (row['street'] in streets):
                streets[row['street']] = row

    for street in sorted(streets):
        if 'street' not in streets[street]:
            print("unknown street: ", street, file=sys.stderr)
            continue

        # try and find the place
        if 'place' not in street:
            key = place_key(streets[street])
            if key in places:
                streets[street]['place'] = places[key]

        if 'place' not in streets[street]:
            print("unknown place: ", key, file=sys.stderr)
            streets[street]['place'] = ''

        print("\t".join([streets[street][field] for field in fields]))
