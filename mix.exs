defmodule OrdinanceSurvey.Mixfile do
  use Mix.Project

  def project do
    [app: :school_data,
     version: "0.0.1",
     elixir: "~> 1.3",
     build_embedded: Mix.env == :prod,
     start_permanent: Mix.env == :prod,
     deps: deps]
  end

  def application do
    [applications: [
      :geocalc,
      :logger,
    ]]
  end

  defp deps do
    [
      {:data_morph, branch: 'stream-filter-take', git: "https://github.com/robmckinnon/data_morph.git"},
      {:floki, "~> 0.10"},
      {:geocalc, "~> 0.5"},
      {:poison, "~> 2.0"},
      {:tabula, "~> 2.0"},
    ]
  end
end
