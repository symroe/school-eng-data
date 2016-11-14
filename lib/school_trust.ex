
defmodule SchoolTrust do

  def cache_files do
    {_, files} = File.ls('./cache/links/')
    files
    |> Stream.map(& "./cache/links/" <> &1)
  end

  def trust_htmls do
    cache_files
    |> Stream.filter(& File.stat!(&1).size >= 6750)
    |> Stream.map(& File.read!(&1))
    |> Stream.filter(& &1 |> String.contains?("Companies House"))
  end

  def trust_row html do
    trust = html
      |> Floki.find("table.est_links tbody tr td")
      |> Enum.slice(0,4)
      |> Enum.map(&Floki.text/1)
    urn = html
      |> Floki.find("h1.edUrnLeft")
      |> Enum.map(& &1 |> Floki.text |> String.replace_leading("URN ", ""))
    trust_join_date = html
      |> Floki.find("tr")
      |> Enum.filter(& &1 |> Floki.find("td.brdrL") |> Floki.text == (urn |> List.first))
      |> List.first
      |> Floki.find("td")
      |> List.last
      |> Floki.text
    trust ++ urn ++ [trust_join_date]
  end

  def trust_rows do
    trust_htmls
    |> Stream.map(&trust_row/1)
    |> Stream.reject(& (&1 |> Enum.at(3)) == "School sponsor" )
  end

  def trust_tsv do
    headers = ~w[school-trust name company type urn school-trust-join-date]
    trust_rows
    |> Stream.uniq
    |> Enum.sort_by(& &1 |> List.first)
    |> DataMorph.puts_tsv(headers)
  end

  def trust_data_tsv do
    :stdio
    |> IO.stream(:line)
    |> DataMorph.structs_from_tsv(:dfe, :school_trust)
    |> Stream.map(& [&1.school_trust, &1.name, "company:"<>&1.company])
    |> Enum.uniq
    |> DataMorph.puts_tsv(~w[edubase-school-trust name organisation])
  end

  defp suppress_name(["school-trust", "name", "organisation"]) do
    ["school-trust", "name", "organisation"]
  end
  defp suppress_name([key, name, ""]) do
    [key, name, ""]
  end
  defp suppress_name([key, _, organisation]) do
    [key, "", organisation]
  end

  def final_trust_tsv do
    :stdio
    |> IO.stream(:line)
    |> CSV.decode(headers: false)
    |> Stream.map(&suppress_name/1)
    |> DataMorph.puts_tsv
  end

end
