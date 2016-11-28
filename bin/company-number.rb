require 'morph'

def load file, type
  Morph.from_tsv IO.read(file), type
end

academies = load('./tmp-academies-second-company-number.tsv', :school) ; nil

academies.each do |academy|
  if academy.company_no.present?
    academy.company = academy.company_no
    academy.company_no = nil
  end
end

puts ['URN','school-type','company','SchoolSponsors (name)'].join("\t")
academies.each do |a|
  puts [a.urn, a.school_type, a.company, a.schoolsponsors_name].join("\t")
end
