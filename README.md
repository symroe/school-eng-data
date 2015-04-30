School Data
-------------

* The prinical source data for this register is retrieved from: http://www.education.gov.uk/edubase/edubase{date}.csv.

* For each school record we try to extract data for the following registers:
  * School
  * Address
  * Postcode
  * Posttown

If all runs well you'll end up with a tsv file for the registers in the data directory.

How to use all of this
----------------------

#### Prerequisites
* Python 3
* mongodb

#### Install dependencies
```
pip install -r requirements.txt
```

* Load address data into mongo (mongod needs to be running)
```
cd data 
cd tar -xvf raw_addresses.tar.gz
cd raw_addresses
mongoimport -d addressbase -c addresses --file=addresses.json
```

* Set environment variable for mongo uri
```
export MONGO_URI='mongodb://127.0.0.1:27017/addressbase'
```

* Run make
```
make
```
