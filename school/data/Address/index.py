#! /usr/bin/env python3

import csv
import json

input_file = csv.DictReader(open("addresses.tsv"), delimiter='\t')
outfile = open("index.json", 'w')
records = []

for row in input_file:
    index = {"address": int(row['address']), "postcode": row['postcode']}
    records.append(index)


print(records)

outfile.write(json.dumps(records))
