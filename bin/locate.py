import os
from pymongo import MongoClient

mongo_uri = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/locate')

client = MongoClient(mongo_uri)
locate = client.get_default_database().addresses


def near(value, target):
    # three decimal places ~ 110m
    return abs(value - target) < 0.001


def address_match(postcode, longitude, latitude):
    postcode = postcode.replace(' ', '').lower()
    addresses = locate.find({"postcode": postcode})

    for address in addresses:
        if address['details']['classification'].startswith('CE0'):
            return address

    return {}
