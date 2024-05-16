import numpy as np
from scipy.stats import chi2_contingency
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL-Abfrage definieren
sparql_query = """
# Thema Analyse
#title:Häufigkeit der Themen in Veröffentlichungen
#defaultView:BarChart
SELECT (YEAR(?date) as ?year) ?themeLabel 
WHERE {
  ?item wdt:P36 ?theme.
  ?item wdt:P9 ?date.
  FILTER(?theme IN (wd:Q2776, wd:Q3085, wd:Q2907))  # love, sentimentalism, family
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?year
"""

# SPARQL-Wrapper initialisieren und Abfrage ausführen
sparql = SPARQLWrapper("https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql")
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Liste von Tupeln (Jahr, Thema) aus den Ergebnissen extrahieren
sparql_output = [(result['year']['value'], result['themeLabel']['value']) for result in results['results']['bindings']]

# Dictionary zum Zählen der Häufigkeiten für jedes Jahr und Thema erstellen
frequency_dict = {}
for year, theme in sparql_output:
    if year in frequency_dict:
        if theme in frequency_dict[year]:
            frequency_dict[year][theme] += 1
        else:
            frequency_dict[year][theme] = 1
    else:
        frequency_dict[year] = {theme: 1}

# Themen
themes = ['love', 'sentimentalism', 'family']

# Matrix der beobachteten Häufigkeiten erstellen
years = sorted(frequency_dict.keys())
observed_frequencies = np.array([[frequency_dict.get(year, {}).get(theme, 0) for theme in themes] for year in years])

# Chi-Quadrat-Test durchführen
chi2, p, dof, expected = chi2_contingency(observed_frequencies)

# Ergebnisse ausgeben
print("Chi-Quadrat-Wert:", chi2)
print("p-Wert:", p)
print("Freiheitsgrade:", dof)
print("Erwartete Frequenzen:")
print(expected)

# Welches Thema hat zugenommen?
if p < 0.05:  # Signifikanzniveau von 0.05
    if observed_frequencies[0][0] < expected[0][0]:
        print("Das Thema 'love' hat signifikant zugenommen.")
    elif observed_frequencies[0][1] < expected[0][1]:
        print("Das Thema 'sentimentalism' hat signifikant zugenommen.")
    else:
        print("Das Thema 'family' hat signifikant zugenommen.")
else:
    print("Es gibt keine signifikante Zunahme eines bestimmten Themas.")
