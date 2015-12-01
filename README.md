# School register data

Data for the prototype [school register](http://school.openregister.org), 
a list of educational establishments in England and Wales taken from the
[Department for Education](https://www.gov.uk/government/organisations/department-for-education)'s
[EduBase public portal](http://www.education.gov.uk/edubase/).

# Building

Use make to build register shaped data
— we recommend using a [Python virtual environment](http://virtualenvwrapper.readthedocs.org/en/latest/):

    $ mkvirtualenv -p python3 school-data
    $ workon school-data
    $ make init

    $ make

# Address matching

Matching a text address found in edubase to the register entry requires a local copy
of the locate database as used by [address-data](https://github.com/openregister/address-data).

# Licence

The software in this project is covered by LICENSE file.

The data is [© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
