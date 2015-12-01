#!/usr/bin/env python3

import sys
import os
import csv

from datetime import datetime

from pymongo import MongoClient

from gbgeo import osgb_to_wgs84
from openregister import Item
from openregister.representations.tsv import Writer

mongo_uri = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/locate')

fieldnames = ["school", "name", "start-date", "end-date", "gender",
              "religious-character", "minimum-age", "maximum-age",
              "headteacher", "website", "address"]

writer = Writer(sys.stdout, fieldnames=fieldnames)
uprns = set([])


def http_url(url):
    "Force HTTP URL"
    return url if url.startswith("http") else "http://" + url


def close_enough(value, target):
    return abs(value - target) < 0.001


def get_best_match(row, addresses):
    easting = row['Easting']
    northing = row['Northing']
    if (easting and northing):
        longitude, latitude = osgb_to_wgs84(easting, northing)

    for address in addresses:
        try:
            if not address['details']['classification'].startswith('CE0'):
                continue

            if latitude and longitude:
                locate_lat = address['location']['lat']
                locate_long = address['location']['long']
                lat_close = close_enough(latitude, locate_lat)
                long_close = close_enough(longitude, locate_long)
                if lat_close and long_close:
                    return address
        except Exception as e:
            print('Problem extracting address details', e)
    else:
        return {}


def get_address_match(row, locate):
    postcode = row['Postcode'].replace(' ', '').lower()
    address_records = locate.find({"postcode": postcode})
    return get_best_match(row, address_records)


if __name__ == '__main__':

    client = MongoClient(mongo_uri)
    locate = client.get_default_database().addresses

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

        address = get_address_match(row, locate)
        if address:
            item.address = address['uprn']
            item.postcode = address['presentation']['postcode']
            writer.write(item)
