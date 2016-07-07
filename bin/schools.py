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
    "address",
    "local-authority",
    "minimum-age",
    "maximum-age",
    "headteacher",
    "website",
    "denomination",
    "school-type",
    "school-phase",
    "school-admissions-policy",
    "school-gender",
    "school-tags",
    "school-federation",
    "start-date",
    "end-date",
]

address = {}

writer = Writer(sys.stdout, fieldnames=fieldnames)


def log(s):
    print(s, file=sys.stderr)


def fix_age(n):
    if not n or n == '0':
        return ''
    if str(int(n)) != n:
        log("invalid age:", n)
        exit(1)

    return n


def fix_http_url(url):
    url = url.replace('http;//', 'http://')
    url = url.strip('/')
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

        item['denomination'] = row['ReligiousCharacter (name)']
        item['minimum-age'] = fix_age(row['StatutoryLowAge'])
        item['maximum-age'] = fix_age(row['StatutoryHighAge'])
        item.headteacher = "%s %s %s" % (
            row['HeadTitle (name)'], row['HeadFirstName'], row['HeadLastName'])

        if row["SchoolWebsite"]:
            item.website = fix_http_url(row["SchoolWebsite"])

        if item.school in address:
            item.address = address[item.school]

        writer.write(item)
