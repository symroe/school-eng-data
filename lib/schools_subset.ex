
defmodule SchoolSubset do

  def schools_in_local_authority code do
    :stdio
    |> IO.stream(:line)
    |> CSV.decode(headers: true, separator: ?\t)
    |> Stream.filter(& &1["school-authority"] == code)
    |> Stream.map(& &1["school"])
    |> Enum.each(&IO.puts/1)
  end

  def school_tsv keys_file do
    regex = key_regex(keys_file)
    :stdio
    |> IO.stream(:line)
    |> Stream.filter(& &1 |> match(regex))
    |> Enum.each(&IO.write/1)
  end

  defp match line, regex do
    String.match?(line, regex) || String.starts_with?(line, "school\t")
  end

  defp key_regex keys_file do
    keys = File.stream!(keys_file) |> Stream.map(&String.strip/1) |> Enum.join("|")
    {:ok, regexp} = Regex.compile "^(" <> keys <> ")\t"
    regexp
  end
end
