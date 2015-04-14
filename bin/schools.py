#!/usr/bin/env python3

"""Explode Edubase CSV into entries for schools"""

import sys
import csv

from gbgeo import osgb_to_wgs84

from entry import Entry
from entry.representations.tsv import Writer


def http_url(url):
    "Force HTTP URL"
    return url if url.startswith("http") else "http://" + url


fields = """
    Address3
    AdministrativeWard (name)
    AdmissionsPolicy (name)
    ApprovedNumberBoardersSpecial
    ASCHighestAge
    ASCLowestAge
    Boarders (name)
    Boys10
    Boys11
    Boys12
    Boys13
    Boys14
    Boys15
    Boys16
    Boys17
    Boys18
    Boys19plus
    Boys2
    Boys3
    Boys4a
    Boys4b
    Boys4c
    Boys5
    Boys6
    Boys7
    Boys8
    Boys9
    CCF (name)
    CensusDate
    CloseDate
    County (name)
    DateOfLastInspectionVisit
    Diocese (name)
    Easting
    EBD (name)
    EdByOther (name)
    EstablishmentName
    EstablishmentNumber
    EstablishmentStatus (name)
    EstablishmentTypeGroup (name)
    EYFSExemption (name)
    FederationFlag (name)
    Federations (name)
    FEHEIdentifier
    FreshStart (name)
    FTProv (name)
    FurtherEducationType (name)
  * Gender (name)
    Girls10
    Girls11
    Girls12
    Girls13
    Girls14
    Girls15
    Girls16
    Girls17
    Girls18
    Girls19plus
    Girls2andUnder
    Girls3
    Girls4a
    Girls4b
    Girls4c
    Girls5
    Girls6
    Girls7
    Girls8
    Girls9
    GOR (name)
    GSSLACode (name)
    HeadFirstName
    HeadHonours
    HeadLastName
    HeadPreferredJobTitle
    HeadTitle (name)
    HP_Leading_Option_1 (name)
    HP_Leading_Option_2 (name)
    HP_Leading_Option_3 (name)
    Inspectorate (name)
    InspectorateName (name)
    InspectorateReport
    InvestorInPeople (name)
    LA (name)
    LastChangedDate
    LeadershipIncentiveGrant (name)
    LLSC (name)
    Locality
    LSOA (name)
    MainSpecialism1 (name)
    MainSpecialism2 (name)
    MSOA (name)
    NextInspectionVisit
    Northing
    NumberOfBoys
    NumberOfGirls
    NumberOfPupils
    OfficialSixthForm (name)
    OfstedLastInsp
    OfstedSpecialMeasures (name)
    OpenDate
    ParliamentaryConstituency (name)
    PercentageFSM
    PFI (name)
    PhaseOfEducation (name)
  * Postcode
    PreviousEstablishmentNumber
    PropsLastName
    ReasonEstablishmentClosed (name)
    ReasonEstablishmentOpened (name)
    RegisteredEY (name)
  * ReligiousCharacter (name)
    ResourcedProvisionCapacity
    ResourcedProvisionOnRoll
    SchoolCapacity
    SchoolSponsorFlag (name)
    SchoolSponsors (name)
    SecondarySpecialism1 (name)
    SecondarySpecialism2 (name)
    Section41Approved (name)
    SEN1 (name)
    SEN2 (name)
    SEN3 (name)
    SEN4 (name)
    SENNoStat
    SENPRU (name)
    SENStat
    SenUnitCapacity
    SenUnitOnRoll
    SixthFormSchool
    SpecialClasses (name)
    SpecialPupils
    StatutoryHighAge
    StatutoryLowAge
    Street
    StudioSchoolIndicator (name)
    TeenMoth (name)
    TeenMothPlaces
  * TelephoneNum
  * TelephoneSTD
  * Town
    Trusts (name)
    TrustSchoolFlag (name)
  * TypeOfEstablishment (name)
    TypeOfReservedProvision (name)
    UKPRN
    UrbanRural (name)
  * URN
  * WebsiteAddress
"""


def process(reader, writer):
    for num, row in enumerate(reader):
        entry = Entry()
        # School
        entry.name = row['EstablishmentName']
        entry.type = row['TypeOfEstablishment (name)'].replace(' ', '')
        entry.type = entry.type.replace('-', '')
        entry.edubase = row['URN']
        entry.gender = row['Gender (name)']
        entry.telephone = row['TelephoneSTD'] + row['TelephoneNum']

        if row["WebsiteAddress"]:
            entry.sameAs = http_url(row["WebsiteAddress"])

        # PostalAddress. As we have generated address data from same
        # file for property.register, we use the line number as a fake
        # uprn - this is only until we have a proper address/property register
        # this allows us to create a link to property register.
        entry.address = 'property:uprn:%s' % num

        if row["WebsiteAddress"]:
            entry.sameAs = http_url(row["WebsiteAddress"])

        entry.easting = row['Easting']
        entry.northing = row['Northing']
        if (entry.easting and entry.northing):
            entry.longitude, entry.latitude = osgb_to_wgs84(
                entry.easting, entry.northing)

        # keep head teacher with school entry for the moment
        entry.headTeacher = "%s %s %s" % (row['HeadTitle (name)'],
                                          row['HeadFirstName'],
                                          row['HeadLastName'])

        writer.write(entry)


if __name__ == '__main__':
    reader = csv.DictReader(sys.stdin)
    out_file = '%s/%s' % (sys.argv[1], 'schools.tsv')

    writer = Writer(open(out_file, 'w'), fieldnames=[
        'name',
        'edubase',
        'gender',
        'telephone',
        'sameAs',
        'easting',
        'northing',
        'latitude',
        'longitude',
        'headTeacher',
        'type',
        'address'])

    process(reader, writer)
    writer.close()
