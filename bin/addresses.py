#!/usr/bin/env python3

import csv
from glob import glob

fields = ['address', 'parent-address', 'primary-address', 'street', 'name', 'name-cy', 'point', 'end-date']

address = {}

if __name__ == '__main__':

    # load addresses from the map
    for row in csv.DictReader(open('maps/addresses.tsv'), delimiter='\t'):
        address[row['address']] = 1

    # output addresses mentioned in the map

    print("\t".join(fields))

    for path in glob('../address-data/data/address/*.tsv'):
        for row in csv.DictReader(open(path), delimiter='\t'):
            if (row['address'] in address):
                print("\t".join([row[field] for field in fields]))
