#!/usr/bin/env python3

import sys
import csv
import re
from datetime import datetime

fields = [
    "school",
    "name",
    "address",
    "school-authority",
    "minimum-age",
    "maximum-age",
    # "headteacher",
    # "website",
    "religious-characters",
    "dioceses",
    "school-type",
    "school-phase",
    "school-admissions-policy",
    "school-gender",
    "school-tags",
    # "school-federation",
    "school-trust",
    "school-umbrella-trust",
    "start-date",
    "end-date",
]

sep = "\t"
address = {}
names = {}


def log(s):
    print(s, file=sys.stderr)


# normalize a name
def n7e(s):
    if not s:
        return ''
    s = s.lower()
    s = re.sub('&', ' and ', s)
    s = re.sub('[^a-z]+', ' ', s)
    s = " ".join(s.split())
    s = s.strip()
    return s


def load_names(field, path, name_field='name'):
    if field not in names:
        names[field] = {}

    for row in csv.DictReader(open(path),
                              delimiter='\t', quoting=csv.QUOTE_NONE):
            name_key = n7e(row[name_field])
            if name_key == '':
                name_key = row[name_field]
            value = row[field]
            names[field][name_key] = value


def map_name(field, name):

    if not name:
        return ''
    _name = n7e(name)
    if _name == '':
        _name = name

    if _name in names[field]:
        return names[field][_name]
    if field != 'school-trust':
        if field != 'school-umbrella-trust':
            log("unknown %s value [%s]" % (field, name))
    return ''


def map_list(field, names):
    return ";".join([map_name(field, name) for name in names.split("/")])


def fix_age(n):
    if not n or n == '0':
        return ''
    if str(int(n)) != n:
        log("invalid age:", n)
        exit(1)

    return n


def fix_http_url(url):
    if 'office@' in url:
        return ""
    url = url.replace('http;//', 'http://')
    url = url.strip('/')
    return url if url.startswith("http") else "http://" + url


if __name__ == '__main__':

    # load map of addresses
    reader = csv.DictReader(open('maps/school-address.tsv'), delimiter='\t')
    for row in reader:
        address[row['school']] = row['address']

    # load other maps
    load_names('school-admissions-policy',
               'data/discovery/school-admissions-policy/school-admissions-policies.tsv')

    load_names('religious-character', 'data/discovery/religious-character/religious-characters.tsv')
    load_names('religious-character', 'maps/religious-character.tsv')

    load_names('diocese', 'data/discovery/diocese/dioceses.tsv')
    load_names('diocese', 'maps/diocese.tsv')

    # load_names('school-federation', 'data/discovery/school-federation/school-federations.tsv')

    load_names('school-gender', 'data/discovery/school-gender/school-genders.tsv')
    load_names('school-gender', 'maps/school-gender.tsv')

    load_names('school-phase', 'data/discovery/school-phase/school-phases.tsv')
    load_names('school-phase', 'maps/school-phase.tsv')

    load_names('school-trust', 'maps/school-trust.tsv', 'school')
    load_names('school-umbrella-trust', 'maps/school-umbrella-trust.tsv', 'school')

    load_names('school-type', 'data/discovery/school-type/school-types.tsv')
    load_names('school-type', 'maps/school-type.tsv')

    load_names('school-authority',
               'data/discovery/school-authority/school-authority.tsv', 'school-authority')

    # read edubase
    reader = csv.DictReader(sys.stdin)

    print(sep.join(fields))

    for num, row in enumerate(reader):
        item = {}
        item['school'] = row['URN']
        item['name'] = row['EstablishmentName']

        item['start-date'] = ''
        item['end-date'] = ''

        if row['OpenDate']:
            date = datetime.strptime(row['OpenDate'], "%d-%m-%Y").date()
            item['start-date'] = date.isoformat()

        if row['CloseDate']:
            date = datetime.strptime(row['CloseDate'], "%d-%m-%Y").date()
            item['end-date'] = date.isoformat()

        item['religious-characters'] = map_list('religious-character', row['ReligiousCharacter (name)'])
        item['dioceses'] = map_name('diocese', row['Diocese (name)'])
        # item['school-federation'] = map_name('school-federation', row['Federations (name)'])
        item['school-gender'] = map_name('school-gender', row['Gender (name)'])
        item['school-phase'] = map_name('school-phase', row['PhaseOfEducation (name)'])
        item['school-type'] = map_name('school-type', row['TypeOfEstablishment (name)'])

        item['school-trust'] = map_name('school-trust', row['URN'])
        item['school-umbrella-trust'] = map_name('school-umbrella-trust', row['URN'])

        item['school-admissions-policy'] = ''
        item['school-authority'] = row['LA (code)']
        item['school-tags'] = ''

        item['minimum-age'] = fix_age(row['StatutoryLowAge'])
        item['maximum-age'] = fix_age(row['StatutoryHighAge'])

        # item['headteacher'] = "%s %s %s" % (
        #     row['HeadTitle (name)'], row['HeadFirstName'], row['HeadLastName'])

        # if row["SchoolWebsite"]:
        #     item['website'] = fix_http_url(row["SchoolWebsite"])

        if item['school'] in address:
            item['address'] = address[item['school']]

        print(sep.join([item.get(field, "") for field in fields]))
