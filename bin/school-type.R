# Purpose:
# Populate the school-type field of school-eng.tsv.  This had been done
# before by linking to a school-type register, but that register no longer has
# priority, so for now the school-type field will stand alone.  The school-type
# data is still available in the GitHub repo.

# Author:
# Duncan Garmonsway

# * Entries with a CURIE type beginning ‘academy-school….’ will become ‘Academy’
# * Entries with a CURIE type beginning ‘la-maintained…’ will become ‘Local authority maintained’
# * Entries that link to the ‘school-type’ register should take the value from that register (e.g. ‘school-type:10’ will become whatever entry had a unique key of ’10’)

library(tidyverse)
library(stringr)

school_eng <- read_tsv("./data/alpha/school-eng/schools.tsv")
school_eng_old <- read_tsv("./data/alpha/school-eng/schoolsOld.tsv")

# Be super-careful to filter for only the latest record per school-type
school_type <- read_tsv("./data/alpha/school-type/school-types.tsv") %>%
  arrange(`school-type`, desc(`end-date`)) %>%
  group_by(`school-type`) %>%
  slice(1) %>%
  ungroup %>%
  select(`school-type`, `school-type-name` = name)

school_eng_new <-
  school_eng %>%
  left_join(school_eng_old %>% select(`school-eng`, organisation),
            by = "school-eng") %>%
  mutate(`school-type` = as.integer(str_extract(.$organisation,
                                                "(?<=school-type:)[0-9]+"))) %>%
  left_join(school_type, by = "school-type") %>%
  mutate(`school-type` = case_when(str_detect(.$organisation, "^academy-school") ~ "Academy",
                                   str_detect(.$organisation, "^la-maintained") ~ "Local authority maintained",
                                   TRUE ~ .$`school-type-name`)) %>%
  select(-organisation, -`school-type-name`)

# Check for any missing values
anyNA(school_eng_new$`school-type`)

# Save the new file.
write_tsv(school_eng_new, "./data/alpha/school-eng/schools.tsv")
