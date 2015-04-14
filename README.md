School Data
-------------

* The source data is retrieved from: http://www.education.gov.uk/edubase/edubase20150414.csv. The file gets updated from time to time and so the above url breaks. Check http://www.education.gov.uk/edubase/register/subscription.xhtml for the current file.

* The addresses are extracted from the school records and a fake UPRN is generated that is actually the line number of the record in the file.


Note: if you regenerate data with a new source file from edubase, do the same for the property register, as the line number in the file determines the fake UPRN that is used to link the property and school registers.
