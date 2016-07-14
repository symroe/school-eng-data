#!/usr/bin/env python3

import csv
import sys
import re

# about a place
place = {}

# places by their name
place_name = {}

# map of local-custodian to local-authority
custodian = {}

# map of os code to local-authority
os = {}


def tsv(file):
    return csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)


# normalize a name
def n7e(s):
    s = s.lower()
    s = re.sub('&', ' and ', s)
    s = re.sub('[^a-z]+', ' ', s)
    s = " ".join(s.split())
    s = s.strip()
    return s


#
#  load maps
#
def add_place_name(ss, p):
    s = n7e(ss)
    if not s:
        return
    if s not in place_name:
        place_name[s] = []
    place_name[s].append(p)


# load local-custodian map
for row in tsv(open('../../local-authority-data/maps/local-custodian.tsv')):
    custodian[row['local-custodian']] = row['local-authority']

# load os map
for row in tsv(open('../../local-authority-data/maps/os.tsv')):
    os[row['os']] = row['local-authority']

# load place register data
# place	name	name-cy	name-gd	uk	point
for row in tsv(open('../../place-data/data/place/places.tsv')):
    place[row['place']] = row
    add_place_name(row['name'], row['place'])
    add_place_name(row['name-cy'], row['place'])
    add_place_name(row['name-gd'], row['place'])

# load place name map
# name	local-authority	place
for row in tsv(open('../../place-data/maps/name.tsv')):
    add_place_name(row['name'], row['place'])

# add place map data
# place	county	district	postcode-district	bounding-box
for row in tsv(open('../../place-data/lists/os-open-names/places.tsv')):
    row['district-local-authority'] = ''
    row['county-local-authority'] = ''

    if row['district']:
        row['district-local-authority'] = os[row['district']]

    if row['county']:
        row['county-local-authority'] = os[row['county']]

    place[row['place']].update(row)


def debug(s=''):
    # print(s)
    return

def debug_search(la, name):
    debug()
    debug(" %s    '%s' %s" % ('?', la, name))

def debug_match(e, la, p):
    debug(" %s    '%s' %s %s %s" % (e, la, place[p]['county-local-authority'], place[p]['district-local-authority'], p))


#
#  matching ..
#
def match_place_name(name, la='*', area='*'):
    debug_search(la, name)
    name = n7e(name)
    if name not in place_name:
        return

    plist = []

    for p in place_name[name]:
        if area == '*':
            pla = ''
        else:
            pla = place[p][area + '-local-authority']

        if la == '*' or la == pla:
            debug_match('+', la, p)
            plist.append(p)
        else:
            debug_match('-', la, p)

    if len(plist) > 1:
        debug("<%s>	%s	%s	%d" % (area, la, name, len(plist)))

    if len(plist) == 1:
        debug_match('*', la, p)
        return plist[0]


# map
fields = [
    'local-authority',
    'town',
    'locality',
    'place',
    'name']

print("	".join([field for field in fields]))

nrows = nmatched = 0
for row in tsv(sys.stdin):
    debug()

    if not row['local-authority']:
        row['local-authority'] = custodian[row['local-custodian']]

    la = row['local-authority']
    town = row['town']
    locality = row['locality']

    # sieves ..
    row['place'] = row['place'] or match_place_name(locality, la, 'district')
    # =14%

    row['place'] = row['place'] or match_place_name(locality, la, 'county')
    # =28%

    # possibly ambiguous, should be validated ..
    row['place'] = row['place'] or match_place_name(locality)
    # =30%

    if locality == '':
        row['place'] = row['place'] or match_place_name(town, la, 'district')
        # =52%

        row['place'] = row['place'] or match_place_name(town, la, 'county')
        # =65%

        row['place'] = row['place'] or match_place_name(town)
        # =68%

    # trumping an unmatched locality with the town, this is quite aggressive
    row['place'] = row['place'] or match_place_name(town, la, 'district')
    # =77%

    row['place'] = row['place'] or match_place_name(town, la, 'county')
    # =87%

    row['place'] = row['place'] or match_place_name(town)
    # =88%

    nrows = nrows + 1
    if row['place']:
        row['name'] = place[row['place']]['name']
        nmatched = nmatched + 1

    if re.match(r"KINGSTON UPON THAMES", row['town']):
        print(row, file=sys.stderr)

    if row['place']:
        print("	".join([row[field] or "" for field in fields]))
    else:
        debug("# " + "	".join([row[field] or "" for field in fields]))

print("%d rows %d matched (%d%%) %d unmatched" %(nrows, nmatched, (100 * nmatched / nrows), (nrows-nmatched)), file=sys.stderr)
