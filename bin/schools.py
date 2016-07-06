#!/usr/bin/env python3

import sys
import csv
from datetime import datetime
from base32_crockford import encode


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

address = {}

writer = Writer(sys.stdout, fieldnames=fieldnames)


def http_url(url):
    return url if url.startswith("http") else "http://" + url


if __name__ == '__main__':

    # load addresses
    reader = csv.DictReader(open('maps/addresses.tsv'), delimiter='\t')
    for row in reader:
        address[row['school']] = encode(row['address'])

    # read edubase
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

        if item.school in address:
            item.address = address[item.school]

        writer.write(item)
