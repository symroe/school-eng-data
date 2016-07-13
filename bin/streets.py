#!/usr/bin/env python3

import sys
import csv
from glob import glob

fields = ['street', 'name', 'name-cy', 'locality', 'town', 'local-authority', 'polyline', 'end-date']

streets = {}

if __name__ == '__main__':

    # load streets from addresses
    for row in csv.DictReader(sys.stdin, delimiter='\t'):
        streets[row['street']] = {}

    # output streets mentioned in the map

    print("\t".join(fields))

    for path in glob('../address-data/data/street/*.tsv'):
        for row in csv.DictReader(open(path), delimiter='\t'):
            if (row['street'] in streets):
                streets[row['street']] = row

    for street in sorted(streets):
        if 'street' not in streets[street]:
            print("unknown street: ", street, file=sys.stderr)
        else:
            print("\t".join([streets[street][field] for field in fields]))
