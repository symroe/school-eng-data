#!/usr/bin/env python3

"""Explode Edubase CSV into entries for schools"""

import sys
import os
import csv
import json

from pymongo import MongoClient

from gbgeo import osgb_to_wgs84

from entry import Entry
from entry.representations.tsv import Writer

# TODO fetch field names from register register.

school_fields = ['school', 'name', 'startDate', 'endDate',
                 'religiousCharacter', 'minAge', 'maxAge', 'headTeacher',
                 'telephone', 'website', 'address']

address_fields = ['address', 'streetAddress', 'postTown', 'county', 'postcode',
                  'country', 'latitude', 'longitude']

post_town_fields = ['postTown', 'startDate', 'endDate', 'text']

postcode_fields = ['postcode', 'polygon']

fieldnames = {'schools': school_fields,
              'addresses': address_fields,
              'posttowns': post_town_fields,
              'postcodes': postcode_fields}


posttowns = set([])
postcodes = set([])
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
        if address['presentation'].get('property'):
            property_name = "%s," % address['presentation']['property']
        else:
            property_name = ''

        if address['presentation'].get('street'):
            street_address = "%s %s" % (property_name,
                                        address['presentation']['street'])
        else:
            street_address = property_name

        entry.streetAddress = street_address.strip()
        entry.postTown = address['presentation']['town']
        entry.postcode = address['presentation']['postcode']
        entry.country = 'GB'
        entry.latitude = address['location']['lat']
        entry.longitude = address['location']['long']

        posttowns.add(address['presentation']['town'].title())
        postcodes.add(address['presentation']['postcode'].strip())

        address_writer.write(entry)
        uprns.add(address['uprn'])


def write_postcodes(writer):
    for postcode in sorted(postcodes):
        entry = Entry()
        entry.postcode = postcode
        writer.write(entry)


def write_posttowns(writer):
    for posttown in sorted(posttowns):
        entry = Entry()
        entry.postTown = posttown
        writer.write(entry)


def process_school(reader, addressbase):
    school_writer = get_writer(sys.argv[1], 'schools')
    address_writer = get_writer(sys.argv[2], 'addresses')
    post_town_writer = get_writer(sys.argv[3], 'posttowns')
    post_code_writer = get_writer(sys.argv[4], 'postcodes')

    for num, row in enumerate(reader):
        entry = Entry()
        # School
        entry.school = row['URN']
        entry.name = row['EstablishmentName']
        entry.startDate = row['OpenDate']
        entry.endDate = row['CloseDate']
        entry.religiousCharacter = row['ReligiousCharacter (name)']
        entry.minAge = row['ASCLowestAge']
        entry.maxAge = row['ASCHighestAge']
        entry.headTeacher = "%s %s %s" % (row['HeadTitle (name)'],
                                          row['HeadFirstName'],
                                          row['HeadLastName'])
        entry.telephone = row['TelephoneSTD'] + row['TelephoneNum']
        if row["WebsiteAddress"]:
            entry.website = http_url(row["WebsiteAddress"])

        address = get_address_match(row, addressbase)
        if address:
            entry.address = address['uprn']
            split_address(address, address_writer)
            school_writer.write(entry)

    write_postcodes(post_code_writer)
    write_posttowns(post_town_writer)

    school_writer.close()
    address_writer.close()
    post_code_writer.close()
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
