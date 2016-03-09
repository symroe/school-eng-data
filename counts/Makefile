EDUBASE=../cache/edubase.csv
COUNT=../bin/count.sh

# "URN","LA (code)","LA (name)","EstablishmentNumber","EstablishmentName","TypeOfEstablishment (name)","EstablishmentStatus (name)","ReasonEstablishmentOpened (name)","OpenDate","ReasonEstablishmentClosed (name)","CloseDate","PhaseOfEducation (name)","StatutoryLowAge","StatutoryHighAge","Boarders (name)","OfficialSixthForm (name)","Gender (name)","ReligiousCharacter (name)","Diocese (name)","AdmissionsPolicy (name)","SchoolCapacity","SpecialClasses (name)","CensusDate","NumberOfPupils","NumberOfBoys","NumberOfGirls","PercentageFSM","TrustSchoolFlag (name)","Trusts (name)","SchoolSponsorFlag (name)","SchoolSponsors (name)","FederationFlag (name)","Federations (name)","UKPRN","FEHEIdentifier","FurtherEducationType (name)","OfstedLastInsp","OfstedSpecialMeasures (name)","LastChangedDate","Street","Locality","Address3","Town","County (name)","Postcode","SchoolWebsite","TelephoneNum","HeadTitle (name)","HeadFirstName","HeadLastName","HeadHonours","HeadPreferredJobTitle","TeenMoth (name)","TeenMothPlaces","CCF (name)","SENPRU (name)","EBD (name)","FTProv (name)","EdByOther (name)","Section41Approved (name)","SEN1 (name)","SEN2 (name)","SEN3 (name)","GOR (name)","AdministrativeWard (name)","ParliamentaryConstituency (name)","UrbanRural (name)","GSSLACode (name)","Easting","Northing","MSOA (name)","LSOA (name)","BoardingEstablishment (name)","PreviousLA (code)","PreviousLA (name)","PreviousEstablishmentNumber"

COUNTS=\
	TypeOfEstablishment-name.tsv

all:	$(COUNTS)

# RECORD-TYPE
TypeOfEstablishment-name.tsv:	$(EDUBASE) $(COUNT)
	$(COUNT) $(EDUBASE) "TypeOfEstablishment (name)" > $@


clean::
	rm -f *tsv
