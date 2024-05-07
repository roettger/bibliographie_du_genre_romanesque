import numpy as np
from scipy.stats import chi2_contingency
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL-Abfrage definieren
sparql_query = """
#Distribution Formats
#title:Distribution formats of publications
#defaultView:BarChart
prefix mmd:<http://data.mimotext.uni-trier.de/entity/>
prefix mmdt:<http://data.mimotext.uni-trier.de/prop/direct/> 
SELECT (str(SAMPLE(year(?date))) as ?year) (count(?format) as ?count) ?format 
WHERE {
    ?item mmdt:P26 ?format.
    ?item mmdt:P9 ?date .
    FILTER(lang(?format) = "fr")
    BIND(str(year(?date)) as ?year)
    SERVICE wikibase:label {bd:serviceParam wikibase:language "en" .}
}
GROUP BY ?format ?year ?count
"""

# SPARQL-Wrapper initialisieren und Abfrage ausführen
sparql = SPARQLWrapper(" 	https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql")
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Liste von Tupeln (Jahr, Buchformat) aus den Ergebnissen extrahieren
sparql_output = [(result['year']['value'], result['format']['value']) for result in results['results']['bindings']]

# Dictionary zum Zählen der Häufigkeiten für jedes Jahr und Buchformat erstellen
frequency_dict = {}
for year, format_type in sparql_output:
    if year in frequency_dict:
        if format_type in frequency_dict[year]:
            frequency_dict[year][format_type] += 1
        else:
            frequency_dict[year][format_type] = 1
    else:
        frequency_dict[year] = {format_type: 1}

# Matrix der beobachteten Häufigkeiten erstellen
years = sorted(frequency_dict.keys())
formats = ['in-12', 'in-8', 'in-18']  # Buchformate
observed_frequencies = np.array([[frequency_dict.get(year, {}).get(format, 0) for format in formats] for year in years])

# Chi-Quadrat-Test durchführen
chi2, p, dof, expected = chi2_contingency(observed_frequencies)

# Ergebnisse ausgeben
print("Chi-Quadrat-Wert:", chi2)
print("p-Wert:", p)
print("Freiheitsgrade:", dof)
print("Erwartete Frequenzen:")
print(expected)
