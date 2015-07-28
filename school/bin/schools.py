#!/usr/bin/env python3

"""Explode Edubase CSV into entries for schools"""

import sys
import os
import csv
import json

from datetime import datetime

from pymongo import MongoClient

from gbgeo import osgb_to_wgs84
from entry import Entry
from entry.representations.tsv import Writer

# TODO fetch field names from register register.

school_fields = ["school", "name", "start-date", "end-date", "gender",
                 "religious-character", "minimum-age", "maximum-age",
                 "headteacher", "website", "address"]

address_fields = ["address", "property", "street", "locality", "town", "area",
                  "postcode", "country", "latitude", "longitude"]

post_town_fields = ['post-town', 'start-date', 'end-date', 'text']

fieldnames = {'schools': school_fields,
              'addresses': address_fields,
              'posttowns': post_town_fields}


posttowns = set([])
uprns = set([])


def http_url(url):
    "Force HTTP URL"
    return url if url.startswith("http") else "http://" + url


def get_writer(directory, file_name):
    out_file = '%s/%s' % (directory, file_name+'.tsv')
    writer = Writer(open(out_file, 'w'), fieldnames=fieldnames[file_name])
    return writer


def write_to_local_file(postcode, json_data):
    out_file = "data/raw_addresses/%s.json" % postcode
    with open(out_file, 'w') as file:
        file.write(json.dumps(json_data))


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
                print('\nSkip: Not a school', address, '\n')
                continue
            if latitude and longitude:
                addressbase_lat = address['location']['lat']
                addressbase_long = address['location']['long']
                lat_close = close_enough(latitude, addressbase_lat)
                long_close = close_enough(longitude, addressbase_long)
                if lat_close and long_close:
                    print('matched on lat and long', latitude,
                          longitude, address)
                    return address
        except Exception as e:
            print('Problem extracting address details', e)
    else:
        return {}


def get_address_match(row, addressbase):
    postcode = row['Postcode'].replace(' ', '').lower()
    address_records = addressbase.find({"postcode": postcode})
    return get_best_match(row, address_records)


def split_address(address, address_writer):
    if address['uprn'] not in uprns:
        entry = Entry()
        entry.address = address['uprn']
        for key, val in address['presentation'].items():
            setattr(entry, key, val)
        entry.country = 'GB'
        entry.latitude = address['location']['lat']
        entry.longitude = address['location']['long']

        posttowns.add(address['presentation']['town'].title())

        address_writer.write(entry)
        uprns.add(address['uprn'])


def write_posttowns(writer):
    for posttown in sorted(posttowns):
        entry = Entry()
        setattr(entry, 'post-town', posttown)
        writer.write(entry)


def process_school(reader, addressbase):
    school_writer = get_writer(sys.argv[1], 'schools')
    address_writer = get_writer(sys.argv[2], 'addresses')
    post_town_writer = get_writer(sys.argv[3], 'posttowns')

    for num, row in enumerate(reader):
        entry = Entry()
        # School
        entry.school = row['URN']
        entry.name = row['EstablishmentName']

        if row['OpenDate']:
            date = datetime.strptime(row['OpenDate'], "%d-%m-%Y").date()
            setattr(entry, 'start-date', date.isoformat())

        if row['CloseDate']:
            date = datetime.strptime(row['CloseDate'], "%d-%m-%Y").date()
            setattr(entry, 'end-date', date.isoformat())

        setattr(entry, 'religious-character', row['ReligiousCharacter (name)'])
        setattr(entry, 'minimum-age', row['ASCLowestAge'])
        setattr(entry, 'maximum-age', row['ASCHighestAge'])
        entry.headteacher = "%s %s %s" % (row['HeadTitle (name)'],
                                          row['HeadFirstName'],
                                          row['HeadLastName'])
        # entry.telephone = row['TelephoneSTD'] + row['TelephoneNum']
        if row["WebsiteAddress"]:
            entry.website = http_url(row["WebsiteAddress"])

        address = get_address_match(row, addressbase)
        if address:
            entry.address = address['uprn']
            entry.postcode = address['presentation']['postcode']

            split_address(address, address_writer)
            school_writer.write(entry)

    write_posttowns(post_town_writer)

    school_writer.close()
    address_writer.close()
    post_town_writer.close()

if __name__ == '__main__':

    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        print('You need to set enviroment variables for:')
        print('MONGO_URI')

    client = MongoClient(mongo_uri)
    addressbase = client.get_default_database().addresses

    reader = csv.DictReader(sys.stdin)
    process_school(reader, addressbase)
