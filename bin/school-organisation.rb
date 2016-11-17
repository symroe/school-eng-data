require 'morph'

def load file, type
  Morph.from_tsv IO.read(file), type
end

def type_codes file, types
  type_names = IO.readlines(file).map(&:strip)
  types.select {|t| type_names.include?(t.name)}.map(&:school_type)
end

schools = load('./schools.tsv', :school) ; nil

types = load('./data/alpha/school-type/school-types.tsv', :type) ; nil

la_types = type_codes('./lists/la-maintained-types/types.txt', types)
academy_types = type_codes('./lists/academy-types/types.txt', types)

schools.each do |school|
  type = school.school_type
  school.organisation = if la_types.include? type
                          "la-maintained-school:#{school.school_eng}"
                        elsif academy_types.include? type
                          "academy-school:#{school.school_eng}"
                        else
                          "school-type:#{type}"
                        end
end

puts ['school-eng2','organisation'].join("\t")
schools.each do |school|
  puts [school.school_eng, school.organisation].join("\t")
end
