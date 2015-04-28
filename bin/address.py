#!/usr/bin/env python3

"""Explode Edubase CSV into entries for addresses of schools"""

import sys
import csv

from entry import Entry
from entry.representations.tsv import Writer

# get uprn from https://preview-verification-locate-api.ertp.alphagov.co.uk


def process(reader, writer):
    for num, row in enumerate(reader):
        entry = Entry()
        entry.address = num
        entry.streetAddress = row['Street']
        entry.postTown = row['Town']
        entry.postcode = row['Postcode']
        entry.country = 'GB'
        entry.latitude = 50
        entry.longitude = -1
        writer.write(entry)


if __name__ == '__main__':
    reader = csv.DictReader(sys.stdin)
    out_file = '%s/%s' % (sys.argv[1], 'addresses.tsv')

    writer = Writer(open(out_file, 'w'), fieldnames=[
        'address',
        'streetAddress',
        'addressLocality',
        'postalCode',
        'addressCountry'])

    process(reader, writer)
    writer.close()
