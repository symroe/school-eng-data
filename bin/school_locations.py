#!/usr/bin/env python3

import sys
import csv

from gbgeo import osgb_to_wgs84

from openregister import Item
from openregister.representations.tsv import Writer

fieldnames = [
    "location",
    "point"
]

writer = Writer(sys.stdout, fieldnames=fieldnames)

if __name__ == '__main__':

    reader = csv.DictReader(sys.stdin)

    for num, row in enumerate(reader):
        if row['Easting'] and row['Northing']:
            item = Item()
            item.location = 'school:' + row['URN']

            lat, lon = osgb_to_wgs84(row['Easting'], row['Northing'])
            item.point = "[%.5f,%.5f]" % (lon, lat)

            writer.write(item)
