require 'morph'

umbrella = (ENV["UMBRELLA"] == "true")

csv = `csvcut -c 'URN,Trusts (name)' ./cache/edubase.csv | awk NF \
| sed 's/St Hildas Catholic Academy Trust/St Hilda’s Catholic Academy Trust/' \
| sed 's/Ridings Federation of Academies Trust, The/Ridings’ Federation of Academies Trust, The/' \
| sed 's/The Helston and Lizard Peninsula Trust~The Helston and Lizard Peninsula Education Trust/The Helston and Lizard Peninsula Education Trust/' \
| sed 's/The Helston and Lizard Peninsula Trust/The Helston and Lizard Peninsula Education Trust/' \
| sed 's/South Cheshire Catholic Multi-academy Trust, The~South Cheshire Catholic Multi-Academy Trust/South Cheshire Catholic Multi-academy Trust, The/' \
| sed 's/created in error-//' \
| sed 's/Co_Operative/Co Operative/'` ; nil

urn_to_trust_name = Morph.
  from_csv(csv, :urn_trust_name).
  select{|x| x.trusts_name != nil} ; nil
# @urn="100188", @trusts_name="Eltham Green School Trust"

trusts_with_company = Morph.
  from_csv(IO.read('./lists/edubase-school-trust/trusts-with-matched-company.csv'), :trust) ; nil
# @school_trust="1", @name="Eltham Green School Trust", @type="trust", @is_umbrella=nil, @organisation=nil, @edubase_school_trust=nil, @company=nil, @company_name=nil

edubase_trust_to_company = Morph.
  from_tsv(IO.read('./lists/edubase-multi-academy-trust/trusts.tsv'), :edubase_trust).
  group_by(&:edubase_school_trust) ; nil
# @edubase_school_trust="15710", @name="Activate Learning Education Trust", @organisation="company:08707909"

urn_to_edubase_trust_and_join_date = Morph.
  from_tsv(IO.read('./maps/school-to-edubase-school-trust.tsv'), :school_edubase_trust).
  group_by(&:school) ; nil
# @school="101857", @edubase_school_trust="15885, @school_trust_join_date="2016-01-03"

def edubase_trust_match urn, urn_to_edubase_trust_and_join_date, edubase_trust_to_company, trusts_with_company
  if edubase_trust_id = urn_to_edubase_trust_and_join_date[urn].try(:first).try(:edubase_school_trust)
    if company_no = edubase_trust_to_company[edubase_trust_id].try(:first).try(:organisation)
      if trusts = trusts_with_company.select{|x| x.organisation == company_no}
        if trusts.size == 1
          trusts.first.school_trust
        else
          raise "multiple trusts found for company: #{company_no} | urn: #{urn}"
        end
      else
        raise "no trust found for company: #{company_no} | urn: #{urn}"
      end
    else
      raise "no company found for edubase_trust_id: #{edubase_trust_id} | urn: #{urn}"
    end
  end
end

def trust_names_match names, trusts_with_company, use_umbrella=nil
  n1, n2 = names.split('~')
  m1 = trust_name_match n1, trusts_with_company
  m2 = trust_name_match n2, trusts_with_company
  match = [m1, m2].select{|x| x.is_umbrella == use_umbrella }
  if match.size == 1
    match.first
  elsif match.size > 1
    raise "multiple matches for trusts: #{names}"
  else
    raise "no match for trusts: #{names}"
  end
end

def trust_name_match name, trusts_with_company
  if name.include?('~')
    trust_names_match name, trusts_with_company
  else
    matches = trusts_with_company.select{|x| x.name == name}
    if matches.size > 1
      raise "multiple matches for trust: #{name}"
    elsif matches.size == 1
      matches.first
    else
      raise "no match for trust: #{name}"
    end
  end
end

def school_trust_id school, urn_to_edubase_trust_and_join_date, edubase_trust_to_company, trusts_with_company
  if trust_id = edubase_trust_match(school.urn, urn_to_edubase_trust_and_join_date, edubase_trust_to_company, trusts_with_company)
    trust_id
  else
    trust_name_match(school.trusts_name, trusts_with_company).try(:school_trust)
  end
end

def add_school_trust! urn_to_trust_name, urn_to_edubase_trust_and_join_date, edubase_trust_to_company, trusts_with_company
  urn_to_trust_name.each do |school|
    begin
      school.school_trust = school_trust_id(school,
        urn_to_edubase_trust_and_join_date, edubase_trust_to_company, trusts_with_company)
      school.school_trust_join_date = urn_to_edubase_trust_and_join_date[school.urn].try(:first).try(:school_trust_join_date)
    rescue Exception => e
      puts e.to_s
      puts e.backtrace
      raise " school: #{school.try(:urn).to_s}"
    end
  end ; nil
end

def add_school_umbrella_trust! urn_to_trust_name, trusts_with_company
  urn_to_trust_name.each do |school|
    begin
      school.school_umbrella_trust = trust_names_match(school.trusts_name,
          trusts_with_company, use_umbrella='yes').school_trust
    rescue Exception => e
      puts e.to_s
      raise " school: #{school.try(:urn).to_s}"
    end
  end ; nil
end

if !umbrella
  add_school_trust! urn_to_trust_name, urn_to_edubase_trust_and_join_date, edubase_trust_to_company, trusts_with_company

  puts ["school", "school-trust", "school-trust-join-date"].join("\t") ; nil
  urn_to_trust_name.each do |school|
    puts [school.urn, school.school_trust, school.try(:school_trust_join_date)].join("\t")
  end ; nil
else
  urn_to_trust_name = urn_to_trust_name.select{|x| x.trusts_name.include?('~') }

  add_school_umbrella_trust! urn_to_trust_name, trusts_with_company
  puts ["school", "school-umbrella-trust"].join("\t") ; nil

  urn_to_trust_name.each do |school|
    puts [school.urn, school.school_umbrella_trust].join("\t")
  end ; nil
end
