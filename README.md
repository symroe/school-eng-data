# School register data

Data for the prototype [school register](http://school.openregister.org), 
a list of educational establishments in England and Wales taken from the
[Department for Education](https://www.gov.uk/government/organisations/department-for-education)'s
[EduBase public portal](http://www.education.gov.uk/edubase/).

# Data

## [school-phase](data/school-phase/school-phases.tsv)

http://school-phase.discovery.openregister.org

## [school-gender](data/school-gender/school-genders.tsv)

http://school-gender.discovery.openregister.org

## [school-type](data/school-type/school-types.tsv)

http://school-type.discovery.openregister.org

## [school-admissions-policy](data/school-admissions-policy/school-admissions-policies.tsv)

http://school-admissions-policy.discovery.openregister.org

## [school-federation](data/school-federation/school-federations.tsv)

http://school-federation.discovery.openregister.org

## [diocese](data/diocese/dioceses.tsv)

http://diocese.discovery.openregister.org

## [denomination](data/denomination/denominations.tsv)

http://denomination.discovery.openregister.org

## [school-authority](data/school-authority/school-authority.tsv)

http://school-authority.discovery.openregister.org

# Addresses

This repository also contains discovery data for the address and street registers, only for those addresses linked to by the school register.

## [Address](data/address/addresses.tsv)

- [address](http://field.alpha.openregister.org/field/address) — The UPRN encoded as three sets of three alphanumeric characters separated by hyphens using Douglas Crockford's [base32 encoding scheme](http://www.crockford.com/wrmg/base32.html).
- [parent-address](http://field.alpha.openregister.org/field/parent-address) — a reference to an address which contains this address
- [primary-address](http://field.alpha.openregister.org/field/primary-address) — a reference to the BS7666 primary addressable object
- [name](http://field.alpha.openregister.org/field/name) — the BS7666 secondary addressable object name as a single field in English
- [name-cy](http://field.alpha.openregister.org/field/name-cy) — the BS7666 secondary addressable object name as a single field in Welsh
- [street](http://field.alpha.openregister.org/field/street) — a reference to the street register
- [point](http://field.alpha.openregister.org/field/point) — the geographical location of the addressable object
- [start-date](http://field.alpha.openregister.org/field/start-date)
- [end-date](http://field.alpha.openregister.org/field/end-date)

## [Street](data/street/streets.tsv)

- [street](http://field.alpha.openregister.org/field/street) — the Unique Street Reference Number (USRN)
- [name](http://field.alpha.openregister.org/field/name) — the street name in English
- [name-cy](http://field.alpha.openregister.org/field/name-cy) — the street name in Welsh
- [place](http://field.alpha.openregister.org/field/place) — a reference to the place register
- [local-authority](http://field.alpha.openregister.org/field/local-authority) — a reference to the local-authority register for the address custodian
- [line](http://field.alpha.openregister.org/field/line) — an polyline describing the geography for the street
- [start-date](http://field.alpha.openregister.org/field/start-date)
- [end-date](http://field.alpha.openregister.org/field/end-date)

http://street.discovery.openregister.org

# Building

Use make to build register shaped data
— we recommend using a [Python virtual environment](http://virtualenvwrapper.readthedocs.org/en/latest/):

    $ mkvirtualenv -p python3 school-data
    $ workon school-data
    $ make init

    $ make

# Address matching

Matching a text address found in edubase to the register entry requires a local copy
of [address-data](https://github.com/openregister/address-data).

# Licence

The software in this project is covered by LICENSE file.

The data is [© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
