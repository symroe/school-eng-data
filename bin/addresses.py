#!/usr/bin/env python3

import sys
import csv
from glob import glob

fields = ['address', 'parent-address', 'primary-address', 'street', 'name', 'name-cy', 'point', 'end-date']

addresses = {}

if __name__ == '__main__':

    # load addresses from the map
    for row in csv.DictReader(sys.stdin, delimiter='\t'):
        addresses[row['address']] = {}

    # output addresses mentioned in the map

    print("\t".join(fields))

    # collect primary and parent addresses ..
    for path in glob('../address-data/data/address/*.tsv'):
        if 'parent-address' in row:
            addresses[row['parent-address']] = {}

        if 'primary-address' in row:
            addresses[row['primary-address']] = {}

    for path in glob('../address-data/data/address/*.tsv'):
        for row in csv.DictReader(open(path), delimiter='\t'):
            if (row['address'] in addresses):
                addresses[row['address']] = row

    for address in sorted(addresses):
        if 'address' not in addresses[address]:
            print("unknown address: ", address, file=sys.stderr)
        else:
            print("\t".join([addresses[address][field] for field in fields]))
