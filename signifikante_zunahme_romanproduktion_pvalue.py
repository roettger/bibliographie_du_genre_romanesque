import numpy as np
from scipy.stats import linregress
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL-Abfrage definieren
sparql_query = """
# Count all novels by year of first Publication
# title: First publication dates of all French novels 1751-1800
# defaultView: BarChart
prefix mmd:<http://data.mimotext.uni-trier.de/entity/>
prefix mmdt:<http://data.mimotext.uni-trier.de/prop/direct/>
SELECT (str(SAMPLE(year(?date))) as ?year) (COUNT(*) AS ?count)
WHERE {
   ?item mmdt:P2 mmd:Q2.
   ?item mmdt:P9 ?date .
}
GROUP BY ?date
ORDER BY DESC(?date)
"""

# SPARQL-Wrapper initialisieren und Abfrage ausführen
sparql = SPARQLWrapper("https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql")
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Liste von Tupeln (Jahr, Anzahl der Romane) aus den Ergebnissen extrahieren
sparql_output = [(result['year']['value'], int(result['count']['value'])) for result in results['results']['bindings']]

# Extrahiere die Jahre und Anzahlen der Romane aus den Ergebnissen
years = [int(result[0]) for result in sparql_output]
counts = [result[1] for result in sparql_output]

# Führe eine lineare Regression durch, um den Anstieg der Romanproduktion zu untersuchen
slope, intercept, r_value, p_value, std_err = linregress(years, counts)

# Ergebnisse ausgeben
print("Anstieg der Romanproduktion pro Jahr:", slope)
print("p-Wert der linearen Regression:", p_value)

# Interpretiere das Ergebnis
if p_value < 0.05:  # Signifikanzniveau von 0.05
    print("Die Romanproduktion hat statistisch signifikant zugenommen.")
else:
    print("Es gibt keine statistisch signifikante Zunahme der Romanproduktion.")
