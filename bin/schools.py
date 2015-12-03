#!/usr/bin/env python3

import sys
import csv
from datetime import datetime

from locate import address_match
from gbgeo import osgb_to_wgs84

from openregister import Item
from openregister.representations.tsv import Writer

fieldnames = [
    "school",
    "name",
    "start-date", "end-date",
    "gender", "religious-character",
    "minimum-age", "maximum-age",
    "headteacher",
    "website",
    "address"]

writer = Writer(sys.stdout, fieldnames=fieldnames)


def http_url(url):
    return url if url.startswith("http") else "http://" + url


if __name__ == '__main__':

    reader = csv.DictReader(sys.stdin)

    for num, row in enumerate(reader):
        item = Item()
        item.school = row['URN']
        item.name = row['EstablishmentName']

        if row['OpenDate']:
            date = datetime.strptime(row['OpenDate'], "%d-%m-%Y").date()
            setattr(item, 'start-date', date.isoformat())

        if row['CloseDate']:
            date = datetime.strptime(row['CloseDate'], "%d-%m-%Y").date()
            setattr(item, 'end-date', date.isoformat())

        item['religious-character'] = row['ReligiousCharacter (name)']
        item['minimum-age'] = row['StatutoryLowAge']
        item['maximum-age'] = row['StatutoryHighAge']
        item.headteacher = "%s %s %s" % (
            row['HeadTitle (name)'], row['HeadFirstName'], row['HeadLastName'])

        if row["SchoolWebsite"]:
            item.website = http_url(row["SchoolWebsite"])

        postcode = row['Postcode']

        if row['Easting'] and row['Northing']:
            lon, lat = osgb_to_wgs84(row['Easting'], row['Northing'])

            address = address_match(postcode, lon, lat)
            if address:
                item.address = address['uprn']

        writer.write(item)
